#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from rpcserver import RPCServer
from routine import *
import crawllog
import sys
import time

def run(rpc, site):
    begin = time.time()

    update_category(site, rpc)
    category_cost = time.time() - begin
    print '\n\n--++ {0} ++--\n\n'.format(category_cost)

    update_listing(site, rpc)
    list_cost = time.time() - begin
    print '\n\n--++ {0} ++--\n\n'.format(list_cost)

    update_product(site, rpc)
    product_cost = time.time() - begin
    print '\n\n--++ {0} ++--\n\n'.format(product_cost)


if __name__ == '__main__':
    rpc = RPCServer()
    site = sys.argv[1]
    fun = sys.argv[2]  or 1
    fun = int(fun)
    if fun == 1:
        print '>> update category'
        update_category(site, rpc)
    elif fun == 2:
        print '>> update listing'
        update_listing(site,rpc)
    else:
        print '>> update product'
        update_product(site,rpc)
