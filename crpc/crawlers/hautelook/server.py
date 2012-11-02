#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.hautelook.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""
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

config = { 
    'max_retries': 3,
    'pool_connections': 10, 
    'pool_maxsize': 10, 
}

request = requests.Session(prefetch=True, timeout=17, config=config, headers=headers)


class Server(object):
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    def __init__(self):
        self.siteurl = 'http://www.hautelook.com'
        self.event_url = 'http://www.hautelook.com/v3/events?upcoming_soon_days=7'

    def convert_time(date_str):
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
            is_updated = False

            event, is_new = Event.objects.get_or_create(event_id=event_id)
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
            else:
                print is_new
                if info['sort_order'] != event.sort_order:
                    is_updated = True
                    event.sort_order = info['sort_order']
            event.update_time = datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, key=event_id, url='{0}/event/{1}'.format(self.siteurl, event_id), is_new=is_new, is_updated=is_updated)

        debug_info.send(sender=DB + '.category.end')


    def crawl_listing(self, url, ctx):
        """.. :py:method::
            not useful
        :param url: event_id actually
        """
        resp = request.get(url)
        data = json.loads(resp.text)
        for item in data['availabilities']:
            info = item['availability']
            info['inventory_id']
            info['color']
            info['']

        common_saved.send(sender=ctx, key=url, url=url, is_new=is_new, is_updated=is_updated)

    def crawl_product(self, url, ctx):
        """.. :py:method::
            Got all the product information and save into the database

            http://www.hautelook.com/v2/product/5446548
        :param url: product url
        """
        product, is_new = Product.objects.get_or_create(pk=casin)
        if is_new:
            product.dept = dept
            product.sale_id = [sale_id]
            product.brand = sale_title
            product.asin = asin
            product.title = title
        else:
            if sale_id not in product.sale_id: product.sale_id.append(sale_id)
        product.updated = False
        product.list_update_time = datetime.utcnow()
        product.save()
        product.updated = True
        product.full_update_time = datetime.utcnow()
        product.save()
        

        

if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
    server.run()
