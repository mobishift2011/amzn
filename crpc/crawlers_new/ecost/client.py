#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawler.ecost.client
~~~~~~~~~~~~~~~~~~~

This is the client part of zeroRPC module. Call by fabfile.py automatically, run on main ec2 instance.

"""
import gevent
import time
import random
import zerorpc
import requests
import sys
from settings import *
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()

sys.path.insert(0, os.path.abspath( os.path.dirname(__file__) ))
from common.stash import *


def crawl_category():
    """.. :py:method::

    this method crawl the category

    .. note::
        This method can not run concurrently, because I use a Queue to store category and url.
    """
    from server import Server
    ss = Server()
    ss.crawl_category()

def crawl_listing(addrs):
    """.. :py:method::

    this method crawl the listing pages based on the category pages we crawled before.

    :param addrs: the RPC server addresses do the actual work

    """
    pool = Pool(30*len(addrs))
    clients = [zerorpc.Client(addr) for addr in addrs]
    for item in col_cats.find({'leaf': 1}, fields=['url', 'catstr', 'num'], timeout=False):
        if u'num' in item:
            pool.spawn(random.choice(clients).crawl_listing, item['url'], item['catstr'], item['num'])
#            ss.crawl_listing(item['url'], item['catstr'], item['num'])
        else:
            pool.spawn(random.choice(clients).crawl_listing, item['url'], item['catstr'])
#            ss.crawl_listing(item['url'], item['catstr'])
        progress()
    pool.join()


def crawl_product(addrs):
    """.. :py:method::
    this method crawl the product pages based on the listing pages(leaf node) we crawled before.

    :param addrs: the RPC server addresses do the actual work
    """
    pool = Pool(30*len(addrs))
    clients = [zerorpc.Client(addr) for addr in addrs]
    count = 0
    t = time.time()
    # ecost for find, url for download
    for item in col_product.find({'updated': False}, fields=['ecost', 'link'], timeout=False):
        pool.spawn(random.choice(clients).crawl_product, item['link'], item['ecost'])
        progress()
        count += 1
        if count % 100 == 0:
            print 'qps', count/(time.time()-t)
    pool.join()


if __name__ == '__main__':
    pass
