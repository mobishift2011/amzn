#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Myhabit's crawling using API """
from gevent import monkey; monkey.patch_all()
import gevent.pool

import requests
import json
import re
import lxml.html
from pprint import pprint
from datetime import datetime, timedelta

from models import Product, Event
from crawlers.common.events import common_saved
from crawlers.common.stash import *

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Ubuntu/12.10 Chromium/22.0.1229.94 Chrome/22.0.1229.94 Safari/537.4',
    'Cookie': 'session-id=187-2590046-5168141; session-id-time=1981953112l; session-token="Du3P0R8YKirRoBoLUW7vGfb+S4AxLHVDHugauuoNNbe7GL7+HdYVbj4R6E0qd0kOYZP1p08iLRS4ifjAM9g3q++7Lnin99mUIyiifqkyaVyFlYZgMzNQRFPtBch2NtU6zsVHt7E0ZipCJzZCBR9wa0RcALAyoWXh3O3XQ2LqcmilYQDqvGwRruHKDHBMFGrsJ8m23uWs+OU9tEn4C9p0IO9kl6t0xjv/0im28qSEE+s="; ct-main=dggZr9fLGRQ6nJUa9lswPE8VamKEexge; ubid-main=180-1581204-1041538',
    'x-amzn-auth': '187-2590046-5168141',
}
req = requests.Session(prefetch=False, timeout=30, config=config, headers=header)

def time2utc(t):
    """ convert myhabit time format (json) to utc """
    return datetime.utcfromtimestamp(t['time']//1000)
   

class Server(object):
    def __init__(self):
        self.rooturl = 'http://www.myhabit.com/request/getAllPrivateSales'

    def crawl_category(self, ctx='', **kwargs):
        r = req.get(self.rooturl)
        data = json.loads(r.text)

        for event_data in data['sales']:
            self._parse_event(event_data, ctx)

    def _parse_event(self, event_data, ctx):
        """.. :py:method::
            get product detail page by {asin: {url: url_str}},
            update soldout info by {casin: {soldout: 1/0, }}, can update them when crawl_listing
        """
        event_id = event_data['id']
        info = event_data['saleProps']

        is_new, is_updated = False, False
        event = Event.objects(event_id=event_id).first()
        if not event:
            is_new = True
            event = Event(event_id=event_id)
            event.urgent = True
            event.combine_url = 'http://www.myhabit.com/homepage#page=b&sale={0}'.format(event_id)
            event.sale_title = info['primary']['title']
            if 'desc' in info['primary']:
                event.sale_description = lxml.html.fromstring(info['primary']['desc']).text_content()
            event.image_urls = [ info['prefix']+val for key, val in info['primary']['imgs'].items() if key == 'hero']
            event.image_urls.extend( [ info['prefix']+val for key, val in info['primary']['imgs'].items() if key in ['desc', 'sale']] )
            if 'brandUrl' in info['primary']:
                event.brand_link = info['primary']['brandUrl']

        event.listing_url = event_data['prefix'] + event_data['url']
        # updating fields
        event.events_begin = time2utc(event_data['start'])
        event.events_end = time2utc(event_data['end'])
        [event.dept.append(dept) for dept in event_data['departments'] if dept not in event.dept]
        event.soldout = True if 'soldOut' in event_data and event_data['soldOut'] == 1 else False
        event.update_time = datetime.utcnow()

        # event_data['dataType'] == 'upcoming' don't have products
        if 'asins' in event_data: event.asin_detail_page = event_data['asins']
        if 'cAsins' in event_data: event.casin_soldout_info = event_data['cAsins']
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)


    def crawl_listing(self, url, ctx='', **kwargs):
        prefix_url = url.rsplit('/', 1)[0] + '/'
        r = req.get(url)
        event_id, data = re.compile(r'parse_sale_(\w+)\((.*)\);$').search(r.text).groups()
        data = json.loads(data)
        event = Event.objects(event_id=event_id).first()
        if not event: event = Event(event_id=event_id)

        for product_data in data['asins']: # ensure we download the complete data once
            if 'cAsin' not in product_data:
                r = req.get(url)
                event_id, data = re.compile(r'parse_sale_(\w+)\((.*)\);$').search(r.text).groups()
                data = json.loads(data)

        for product_data in data['asins']:
            self._parse_product(event_id, event.asin_detail_page, event.casin_soldout_info, prefix_url, product_data, ctx)

        if event.urgent == True:
            event.urgent = False
            event.update_time = datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event_id, is_new=False, is_updated=False, ready=True)


    def _parse_product(self, event_id, asins, cAsins, prefix_url, product_data, ctx):
        """ no video info, list_info, summary

        :param event_id: this product belongs to the event's id
        :param asins: all asins info in this event
        :param cAsins: all casins info in this event
        :param prefix_url: image and js prefix_url, probably 'http://z-ecx.images-amazon.com/images/I/'
        :param product_data: product data in this product
        """
        asin = product_data['asin']
        casin = product_data['cAsin']
        title = product_data['title'] # color is in title
        image_urls = [product_data['image']] + product_data['altImages'] # one picture, altImages is []
        if 'listPrice' in product_data:
            listprice = product_data['listPrice']['display'] # or 'amount', if isRange: True, don't know what 'amount' will be
        else: listprice = ''
        price = product_data['ourPrice']['display']
        sizes = []
        if product_data['teenagers']: # no size it is {}
            for k, v in product_data['teenagers'].iteritems():
                if v['size'] not in sizes: sizes.append(v['size'])
        # tag is not precision. e.g. a bag is in shoes
        # tag = product_data['productGL'] if 'productGL' in product_data else '' # 'apparel', 'home', 'jewelry', ''
        if casin in cAsins and 'soldOut' in cAsins[casin] and cAsins[casin]['soldOut'] == 1:
            soldout = True
        else: soldout = False
        jslink = prefix_url + asins[asin]['url'] if asin in asins else ''

        is_new, is_updated = False, False
        product = Product.objects(key=casin).first()
        if not product:
            is_new = True
            product = Product(key=casin)
            product.combine_url = 'http://www.myhabit.com/homepage#page=d&sale={0}&asin={1}&cAsin={2}'.format(event_id, asin, casin)
            product.asin = asin
            product.title = title
            product.image_urls = image_urls
            product.listprice = listprice
            product.price = price
            product.sizes = sizes
            product.soldout = soldout
            product.updated = False
        else:
            if soldout and product.soldout != soldout:
                product.soldout = True
                is_updated = True
                product.update_history.update({ 'soldout': datetime.utcnow() })
        if event_id not in product.event_id: product.event_id.append(event_id)
        product.jslink = jslink
        product.list_update_time = datetime.utcnow()
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=casin, url=product.combine_url, is_new=is_new, is_updated=is_updated)


    def crawl_product(self, url, casin, ctx='', **kwargs):
        r = req.get(url)
        data = re.compile(r'parse_asin_\w+\((.*)\);$').search(r.text).group(1)
        data = json.loads(data)

        asin = data['detailJSON']['asin']
        summary = data['productDescription']['shortProdDesc']
        list_info = [i.replace('&quot;', '"').replace('&#39;', '\'') for i in data['productDescription']['bullets'][0]['bulletsList']]
        brand = data['detailJSON']['brand']
        returned = data['detailJSON']['returnPolicy']
        if 'intlShippable' in data['detailJSON']:
            shipping = 'international shipping' if data['detailJSON']['intlShippable'] == 1 else 'no international shipping'
        elif 'choices' in data['detailJSON']:
            for i in data['detailJSON']['choices']:
                if i['asin'] == casin:
                    shipping = 'international shipping' if i['intlShippable'] == 1 else 'no international shipping'
                    break
        shipping = shipping if shipping else ''

        video = ''
        for p in data['detailJSON']['asins']:
            if p['asin'] == casin:
                video = p['videos'][0]['url'] if p['videos'] else ''
                break

        is_new, is_updated = False, False
        product = Product.objects(key=casin).first()
        if not product:
            is_new = True
            product = Product(key=casin)
        product.summary = summary
        product.list_info = list_info
        product.brand = brand
        product.shipping = shipping
        product.returned = returned
        product.video = video
        product.full_update_time = datetime.utcnow()

        if product.updated == False:
            product.updated = True
            ready = True
        else: ready = False
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=casin, url=url, is_new=is_new, is_updated=is_updated, ready=ready)


if __name__ == '__main__':
    import zerorpc
    from settings import CRAWLER_PORT
    server = zerorpc.Server(Server())
    server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
    server.run()
