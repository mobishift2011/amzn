#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ethan <ethan@favbuy.com>
from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
import gevent
from settings import MASTIFF_HOST
from crawlers.common.stash import *
from crawlers.common.routine import get_site_module
from powers.pipelines import ProductPipeline
from mongoengine import Q
import slumber
import requests
import traceback
from datetime import datetime

api = slumber.API(MASTIFF_HOST)
results = []

def pipe(site, product):
    text_list = []
    text_list.append(product.title or u'')
    text_list.extend(product.list_info or [])
    text_list.append(product.summary or u'')
    text_list.append(product.short_desc or u'')
    text_list.extend(product.tagline or [])

    pp = ProductPipeline(site, product)
    pp.extract_secondhand(text_list)

    if product.second_hand:
        results.append(product)
        # print product.title; print product.combine_url; print product.list_info; print product.shipping; print product.returned; print

if __name__ == '__main__':
    import sys
    sites = [sys.argv[1]] if len(sys.argv) > 1 else picked_crawlers

    with open('secondhands.txt', 'w') as f:
        for site in sites:
            m = get_site_module(site)
            pool = Pool(10)
            products = m.Product.objects(Q(products_end__gt=datetime.utcnow()) | Q(products_end__exists=False))

            print 'site: ', site
            print 'total products: ', len(products)

            results = []
            for product in products:
                pool.spawn(pipe, site, product)
            pool.join()
            products = None

            total_secondhands = len(results)
            print 'secondhand products: ', total_secondhands
            
            f.write('sie: {0}, total: {1}\n'.format(site, total_secondhands))
            for product in results:
                title = product.title.encode('utf-8') if product.title else ''
                combine_url = product.combine_url.encode('utf-8') if product.combine_url else ''
                f.write('{0}\t{1}\t{2}\t{3}\n'.format(title, combine_url, product.second_hand, product.list_info))
            f.write('\n')

            print
