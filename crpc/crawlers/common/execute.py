#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

"""
import crawllog -> from events import * -> from helpers.signals import Signal -> p = Processer()
    -> gevent.spawn a listener(from settings import *) -> listen from REDIS_HOST[SIGNALS]
    import crawllog # from routine import *, we already bind the signal, and have a gevent.spawned listener,
"""
from rpcserver import RPCServer
from routine import *
import sys
import time

def run(site, rpc):
    begin = time.time()

    new_category(site, rpc)
    category_cost = time.time() - begin
    print '\n\n--++ {0} ++--\n\n'.format(category_cost)

    new_listing(site, rpc)
    list_cost = time.time() - begin
    print '\n\n--++ {0} ++--\n\n'.format(list_cost)

    new_product(site, rpc)
    product_cost = time.time() - begin
    print '\n\n--++ {0} ++--\n\n'.format(product_cost)

    update_listing(site, rpc)

if __name__ == '__main__':
    rpc = RPCServer()
#    rpc.call('myhabit', 'crawl_category', (), {'ctx':'haha'})
    if sys.argv[1]:
        if sys.argv[1] == 'myhabit' or 'zulily' or 'hautelook' or 'onekingslane' or 'ruelala':
            run(sys.argv[1], rpc)
    else:
        update_category('ruelala', rpc)
