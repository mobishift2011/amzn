#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from rpcserver import CrawlerServer
from routine import *
import crawllog
import sys
import time


if __name__ == '__main__':
    rpc = CrawlerServer()
    site = sys.argv[1]
    fun = sys.argv[2]  or 1
    fun = int(fun)
    if fun == 1:
        print '>> update category'
        update_category(site, rpc)
    elif fun == 2:
        print '>> update listing'
        update_listing(site,rpc)
    elif fun == 3:
        print '>> update product'
        update_product(site,rpc)
