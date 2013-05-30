#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

"""
import crawllog -> from events import * -> from helpers.signals import Signal -> p = Processer()
    -> gevent.spawn a listener(from settings import *) -> listen from REDIS_HOST[SIGNALS]
    import crawllog # from routine import *, we already bind the signal, and have a gevent.spawned listener,
"""
from crawlerserver import CrawlerServer
from routine import *
import sys
import time

def run(site, rpc):
    begin = time.time()

    new_category(site, rpc, concurrency=1)
    category_cost = time.time() - begin
    print '\n\n--++ category {0} ++--\n\n'.format(category_cost)

    new_listing(site, rpc, concurrency=1)
    list_cost = time.time() - begin
    print '\n\n--++ listing {0} ++--\n\n'.format(list_cost)

    new_product(site, rpc, concurrency=1)
    product_cost = time.time() - begin
    print '\n\n--++ product {0} ++--\n\n'.format(product_cost)

#    update_listing(site, rpc, concurrency=1)

if __name__ == '__main__':
    rpc = CrawlerServer()
#    rpc.call('myhabit', 'crawl_category', (), {'ctx':'asdf'})
#    exit(0)
    if sys.argv[1]:
        # Attention: the following is not working as we want.
        if sys.argv[1] == 'myhabit' or 'zulily' or 'hautelook' or 'onekingslane' or 'ruelala' or 'venteprivee' or 'nomorerack':
            run(sys.argv[1], rpc)
