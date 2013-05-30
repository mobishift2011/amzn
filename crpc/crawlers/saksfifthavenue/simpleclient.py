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
        api.product(product.muri.split("/")[-2]).patch({'ends_at': utcnow.isoformat()})
    product.products_end = utcnow
    product.save()

class CheckServer(object):
    def __init__(self):
        pass

    def check_onsale_product(self, id, url):
        product = Product.objects(key=id).first()

        if product is None:
            print '\n\nsaksfifthavenue has no product -> {0}, {1}\n\n'.format(id, url)
            return

        res = requests.get(product.combine_url)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)

        product_node = tree.cssselect('div.pdp-item-container')
        if not product_node:
            offsale_update(product)
            print 'product {0} is unavailable now, muri: {1} -> {2}'.format(product.key, product.muri, product.combine_url)
            return

        listprice_node = product_node[0].cssselect('.product-price')
        listprice = listprice_node[0].text if listprice_node else None
        price_node = product_node[0].cssselect('.product-sale-price')
        price = price_node[0].text if price_node else None

        if not price or not listprice:
            offsale_update(product)
            print 'product {0} is unavailable for the price, muri: {1} -> {2}'.format(product.key, product.muri, product.combine_url)
            return

        # update product
        if price and price != product.price:
            product.price = price

        if listprice and listprice != product.listprice:
            product.listprice = listprice

        # To pick the product which fit our needs, such as a certain discount, brand, dept etc.
        selected = Picker(site='saksfifthavenue').pick(product)
        if not selected:
            offsale_update(product)
            print 'product {0} is not selected now, muri: {1} -> {2}'.format(product.key, product.muri, product.combine_url)
            return

        update_history = product.update_history or {}
        if product.publish_time and ((update_history.get('favbuy_price') and update_history.get('favbuy_price') > product.publish_time)
            or (update_history.get('favbuy_listprice') and update_history.get('favbuy_listprice') > product.publish_time)): 
            product.save()
            print 'product {0} price changed, muri: {1} -> {2}'.format(product.key, product.muri, product.combine_url)


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
