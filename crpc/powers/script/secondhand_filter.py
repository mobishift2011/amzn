#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ethan <ethan@favbuy.com>
from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
from settings import MASTIFF_HOST
from crawlers.common.stash import *
from crawlers.common.routine import get_site_module
from mongoengine import Q
import slumber
import requests
import traceback
from datetime import datetime
import sys


results = []

def extract_secondhand(product, text_list):
    second_hand = False; updated = False

    text = '\n'.join(text_list).lower()
    filter_set = [
        # 'Antique',
        'pre-own',
        'pre own'
        'preown'
        'previously own',
        'previously-own',
        'previous own',
        'previous-own'
        'Final sale item',
        'archive product',
    ]

    for  filter_key in filter_set:
        key = filter_key.lower() 
        if key in text:
            second_hand = True
            break
        # elif product.shipping and key in product.shipping.lower():
        #     second_hand = True
        #     break
        # elif product.returned and key in product.returned.lower():
        #     second_hand = True
        #     break

    # if product.returned:
    #     pattern = r'non?[-|\s]*returnable[/|\s]+non?[-|\s]*returns'
    #     if re.search(pattern, product.returned):
    #         second_hand = True
    
    if second_hand != product.second_hand:
        product.second_hand = second_hand
        product.update_history['second_hand'] = datetime.utcnow()
        updated = True

    return updated


def pipe(product):
    text_list = []
    text_list.append(product.title or u'')
    text_list.extend(product.list_info or [])
    text_list.append(product.summary or u'')
    text_list.append(product.short_desc or u'')
    text_list.extend(product.tagline or [])

    if extract_secondhand(product, text_list):
        results.append(product)
        # product.save()
        # print product.title; print product.combine_url; print product.list_info; print product.shipping; print product.returned; print


def filter():
    sites = [sys.argv[1]] if len(sys.argv) > 1 else picked_crawlers
    with open('secondhands.txt', 'w') as f:
        for site in sites:
            m = get_site_module(site)
            pool = Pool(10)
            products = m.Product.objects(Q(products_end__gt=datetime.utcnow()) | Q(products_end__exists=False) | Q(soldout=False))

            print 'site: ', site
            print 'total products: ', len(products)

            global results
            results = []
            for product in products:
                pool.spawn(pipe, product)
            pool.join()
            products = None

            total_secondhands = len(results)
            print 'secondhand products: ', total_secondhands
            
            # f.write('sie: {0}, total: {1}\n'.format(site, total_secondhands))
            for product in results:
                title = product.title.encode('utf-8') if product.title else ''
                combine_url = product.combine_url.encode('utf-8') if product.combine_url else ''
                f.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(product.key, title, combine_url, product.second_hand, product.list_info, site))
            f.write('\n')

            print


if __name__ == '__main__':
    filter()
