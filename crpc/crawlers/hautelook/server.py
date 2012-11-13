#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.hautelook.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""
from crawlers.common.events import *
from crawlers.common.stash import *
from models import *
from datetime import datetime, timedelta

import requests
import json
import itertools


headers = { 
    'Accept': 'application/json',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,en-US;q=0.8,en;q=0.6',
    'Auth': 'HWS a5a4d56c84b8d8cd0e0a0920edb8994c',
    'Connection': 'keep-alive',
    'Content-encoding': 'gzip,deflate',
    'Content-type': 'application/json',
    'Host': 'www.hautelook.com',
    'Referer': 'http://www.hautelook.com/events',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Ubuntu/12.10 Chromium/22.0.1229.94 Chrome/22.0.1229.94 Safari/537.4',
    'X-Requested-With': 'XMLHttpRequest',
}

request = requests.Session(prefetch=True, timeout=20, config=config, headers=headers)


class Server(object):
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    def __init__(self):
        self.siteurl = 'http://www.hautelook.com'
        self.event_url = 'http://www.hautelook.com/v3/events?upcoming_soon_days=7'

    def convert_time(self, date_str):
        """.. :py:method::
            covert time from the format into utcnow()
            '2012-10-31T08:00:00-07:00'
        """
        date, Time = date_str.split('T')
        time_str = date + '-' + Time.split('-')[0]
        fmt = "%Y-%m-%d-%X"
        hours, minutes = Time.split('-')[1].split(':')
        return datetime.strptime(time_str, fmt) - timedelta(hours=int(hours), minutes=int(minutes))

    def crawl_category(self, ctx):
        """.. :py:method::
            from self.event_url get all the events
        """
        debug_info.send(sender=DB + '.category.begin')

        resp = request.get(self.event_url)
        data = json.loads(resp.text)
        lay1 = data['events']
        lay2_upcoming, lay2_ending_soon, lay2_today = lay1['upcoming'], lay1['ending_soon'], lay1['today']

        for event in itertools.chain(lay2_upcoming, lay2_ending_soon, lay2_today):
            info = event['event']
            event_id = info['event_id']
            event_code = info['event_code']
            event, is_new = Event.objects.get_or_create(event_id=event_id)
            is_updated = False
            if is_new:
                event.sale_title = info['title']
                event.sale_description = requests.get(info['info']).text
                event.dept = [i['name'] for i in info['event_types']]
                event.events_begin = self.convert_time( info['start_date'] )
                event.events_end = self.convert_time( info['end_date'] )
                event.tagline = info['category']

                pop_img = 'http://www.hautelook.com/assets/{0}/pop-large.jpg'.format(event_code)
                grid_img = 'http://www.hautelook.com/assets/{0}/grid-large.jpg'.format(event_code)
                event.image_urls = [pop_img, grid_img]
                event.sort_order = info['sort_order']
                event.urgent = True
            else:
                if info['sort_order'] != event.sort_order:
                    event.sort_order = info['sort_order']
                    is_updated = True
            event.update_time = datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, key=event_id, url='{0}/event/{1}'.format(self.siteurl, event_id), is_new=is_new, is_updated=is_updated)
        debug_info.send(sender=DB + '.category.end')


    def crawl_listing(self, url, ctx):
        """.. :py:method::
            not useful
        :param url: event url with event_id 
        """
        resp = request.get(url)
        data = json.loads(resp.text)
        if data.keys()[0] != 'availabilities':
            resp = request.get(url)
            data = json.loads(resp.text)
        if data.keys()[0] != 'availabilities':
            common_failed.send(sender=ctx, key='get availabilities twice, both error', url=url, reason=data)
            return
        event_id = re.compile('http://www.hautelook.com/v3/catalog/(.+)/availability').match(url).group(1)
        event, is_new = Event.objects.get_or_create(event_id=event_id)
        if event.urgent == True:
            event.urgent = False
            event.save()

        for item in data['availabilities']:
            info = item['availability']
            key = info['inventory_id']
            color = '' if info['color'].lower() == 'no color' else info['color']
            product, is_new = Product.objects.get_or_create(pk=key)
            scarcity = str(info['sizes'][0]['size']['remaining'])
            is_updated = False
            if is_new:
                if color: product.color = color
                product.updated = False
            else:
                if product.scarcity != scarcity:
                    product.scarcity = scarcity
                    is_updated = True
            if event_id not in product.event_id: product.event_id.append(event_id)
            product.list_update_time = datetime.utcnow()
            product.save()
            common_saved.send(sender=ctx, key=key, url=url, is_new=is_new, is_updated=is_updated)


    def crawl_product(self, url, ctx):
        """.. :py:method::
            Got all the product information and save into the database
        :param url: product url, with product id
        """
        resp = request.get(url)
        if resp.text == '':
            resp = request.get(url)
            if resp.text == '':
                common_failed.send(sender=ctx, key='get product twice, url has nothing', url=url, reason='url has nothing')
                return
        data = json.loads(resp.text)['data']
        product, is_new = Product.objects.get_or_create(pk=url.split('/')[-1])

#        product.event_id = [str(data['event_id'])]
        product.title = data['title']
        if 'copy' in data and data['copy']:
            product.list_info = data['copy'].split('\n')

        if data['event_display_brand_name']:
            if data['event_title'] != data['brand_name']:
                product.brand = data['brand_name']

        product.sizes = [sz['name'] for sz in data['collections']['size']] # OS -- no size info

        color = ''
        # same product with different colors, all in the same product id
        price_flage = True
        for color_str,v in data['prices'].iteritems():
            if not price_flage: break
            if isinstance(v, list):
                for val in v:
                    if product.key == str(val['inventory_id']):
                        product.price = str(val['sale_price'])
                        product.listprice = str(val['retail_price'])
                        price_flage = False
                        color = color_str
                        break
            elif isinstance(v, dict):
                for size, val in v.iteritems():
                    if product.key == str(val['inventory_id']):
                        product.price = str(val['sale_price'])
                        product.listprice = str(val['retail_price'])
                        price_flage = False
                        color = color_str
                        break

        # color: find the color, associate it to get the right images
        for color_info in data['collections']['color']:
            if color_info['name'] == color:
                product.image_urls = data['collections']['images'][ color_info['image'] ]['large']
#        image_set = set()
#        for k,v in data['collections']['images'].iteritems():
#            for img in v['large']:
#                if 'noavail' not in img:
#                    image_set.add(img)
#        product.image_urls = list(image_set)

        if data['add_info']: product.additional_info = data['add_info'].split('\n')
        if data['care']: product.care_info = data['care']
        if data['fiber']: product.fiber = data['fiber']
        product.arrives = data['arrives']

        product.returned = str(int(data['returnable'])) # bool
        product.international_ship = str(int(data['international'])) # bool
        product.delivery_date = ' to '.join((data['estimated_delivery']['start_date'], data['estimated_delivery']['end_date']))
        product.choke_hazard = str(int(data['choke_hazard'])) # bool

        product.updated = True
        product.full_update_time = datetime.utcnow()
        product.save()
        common_saved.send(sender=ctx, key=url, url=url, is_new=is_new, is_updated=not is_new)


if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
    server.run()
