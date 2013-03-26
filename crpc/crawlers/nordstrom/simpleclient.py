#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ethan <ethan@favbuy.com>
from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
import gevent
from settings import MASTIFF_HOST
from crawlers.common.stash import *
from models import Category, Product
from mongoengine import Q
import slumber
import requests
import lxml.html
import traceback
from datetime import datetime

api = slumber.API(MASTIFF_HOST)


def offsale_update(product):
    utcnow = datetime.utcnow()
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

        res = requests.get(product.combine_url)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)

        if tree.cssselect('div#unavailableStyleMessage'):
            offsale_update(product)


    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

if __name__ == '__main__':
    from crawlers.common.onoff_routine import spout_obj
    import os, sys
    
    method = sys.argv[1] if len(sys.argv) > 1 else 'check_onsale_product'
    pool = Pool(10)
    for product in spout_obj(os.path.split(os.path.abspath(__file__+'/../'))[-1], method):
        pool.spawn(CheckServer().getattr(method), product)
    pool.join()
