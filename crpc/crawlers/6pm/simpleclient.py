#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ethan <ethan@favbuy.com>
from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
import gevent
from settings import MASTIFF_HOST
from crawlers.common.stash import *
from models import Category, Product
from deals.picks import Picker
from mongoengine import Q
import slumber
import requests
import lxml.html
import traceback
from datetime import datetime

api = slumber.API(MASTIFF_HOST)


def offsale_update(product):
    utcnow = datetime.utcnow()
    if product.muri:
        print api.product(product.muri.split("/")[-2]).patch({'ends_at': utcnow.isoformat()}); print
    product.products_end = utcnow
    product.save()

class CheckServer(object):
    def __init__(self):
        pass

    def check_onsale_product(self, id, url):
        product = Product.objects(key=id).first()

        if product is None:
            print '\n\nnordstrom has no product -> {0}, {1}\n\n'.format(id, url)
            return

        request_count = 1
        while True:
            res = requests.get(product.combine_url)
            if res.status_code == 404:
                if request_count < 4:
                    request_count += 1 
                    continue
                print '404 not found -> %s' % product.combine_url
                offsale_update(product)
                return
            else:
                res.raise_for_status()
            tree = lxml.html.fromstring(res.content)
            break

        if tree.cssselect('div.searchNone'):
            offsale_update(product)

        price_node = tree.cssselect('div#theater div#productForm form#prForm ul li#priceSlot')[0]
        listprice = price_node.cssselect('.oldPrice')[0].text.strip()
        price = price_node.cssselect('.price')[0].text.strip()

        # update product
        if price and price != product.price:
            product.price = price

        if listprice and not product.listprice and listprice != product.listprice:
            product.listprice = listprice

        # To pick the product which fit our needs, such as a certain discount, brand, dept etc.
        selected = Picker(site='6pm').pick(product)
        if not selected:
            offsale_update(product)


    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

if __name__ == '__main__':
    try:
        from crawlers.common.onoff_routine import spout_obj
        import os, sys

        method = sys.argv[1] if len(sys.argv) > 1 else 'check_onsale_product'
        pool = Pool(10)
        for product in spout_obj(os.path.split(os.path.abspath(__file__+'/../'))[-1], method):
            pool.spawn(getattr(CheckServer(), method), product.get('id'), product.get('url'))
        pool.join()
    except:
        print traceback.format_exc()
