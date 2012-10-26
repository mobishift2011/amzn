#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from rpcserver import RPCServer
from routine import *
import crawllog
import sys
import time

if __name__ == '__main__':
    rpc = RPCServer()
    begin = time.time()
    if sys.argv[1] and sys.argv[1] == 'myhabit':
#        update_category('myhabit', rpc)
        category_cost = time.time() - begin
        print '\n\n--++ {0} ++--\n\n'.format(category_cost)
        update_product('myhabit', rpc)
        product_cost = time.time() - begin
        print '\n\n--++ {0} ++--\n\n'.format(product_cost)
    else:
        update_category('ruelala', rpc)
