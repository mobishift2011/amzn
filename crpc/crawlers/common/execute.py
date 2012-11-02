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

#    update_category(site, rpc)
#    category_cost = time.time() - begin
#    print '\n\n--++ {0} ++--\n\n'.format(category_cost)
#
#    update_listing(site, rpc)
#    list_cost = time.time() - begin
#    print '\n\n--++ {0} ++--\n\n'.format(list_cost)

    update_product(site, rpc)
    product_cost = time.time() - begin
    print '\n\n--++ {0} ++--\n\n'.format(product_cost)


if __name__ == '__main__':
    rpc = RPCServer()
    if sys.argv[1]:
        if sys.argv[1] == 'myhabit' or 'zulily' or 'hautelook':
            run(rpc, sys.argv[1])
    else:
        update_category('ruelala', rpc)
