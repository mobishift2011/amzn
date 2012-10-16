#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.common.routine
~~~~~~~~~~~~~~~~~~~~~~~

a routine library abstracts daily jobs for every crawler

the following functions are supposed to be called from other module

- update_category(site, rpc, concurrency)
- update_listing(site, rpc, concurrency)
- update_product(site, rpc, concurrency)

site:           name of the crawler's directory
rpc:            an RPCServer instance 
concurrency:    how much concurrency should be achieved 

"""
from settings import *
from gevent.pool import Pool

import time
import random

from itertools import chain

from crawlers.common.events import category_failed, product_failed, pre_general_update, post_general_update
from datetime import datetime, timedelta
    
MAX_PAGE = 400

def get_site_module(site):
    return __import__('crawlers.'+site+'.models', fromlist=['Category', 'Product'])

def spout_listing(site):
    """ return a generator spouting listing pages """
    m = get_site_module(site)
    return m.Category.objects(is_leaf=True).order_by('-update_time').timeout(False)

def spout_category(category):
    """ return a generator spouting category url """
    c = category
    if c.spout_time and c.spout_time > datetime.utcnow()-timedelta(hours=12):
        return

    pages = (c.num-1)/c.pagesize+10
    for p in range(1, min(pages+1,MAX_PAGE+1)):
        url = c.url().format(p)
        yield url

def spout_product(site):
    """ return a generator spouting product url """
    m = get_site_module(site)
    p1 = m.Product.objects.filter(updated = False).timeout(False)
    p2 = m.Product.objects.filter(updated = True, 
            full_update_time__lt = datetime.utcnow()-timedelta(hours=24)).timeout(False)
    for p in chain(p1, p2):
        yield p.url()

class UpdateContext(object):
    """ the context manager for monitoring 
        
    wraps tedious signals passing inside the context manager
    
    Usage:

    >>> with MonitorContext(site='amazon', method='update_category'):
    ...     pass # do something related to site and method

    """
    def __init__(self, site, method):
        self.sender = "commonupdate"
        self.site = site
        self.method = method

    def __enter__(self):
        pre_general_update.send(sender = self.sender,
                                    site = self.site,
                                    method = self.method) 

    def __exit__(self, exc_type, exc_value, traceback):
        complete = True
        reason = ''
        if exc_type:
            complete = False
            reason = repr(exc_value)

        post_general_update.send(sender = self.sender,
                                    site = self.site,
                                    method = self.method,
                                    complete = False,
                                    reason = reason)
            

def update_category(site, rpc, concurrency=30):
    with UpdateContext(site=site, method='update_category'):
        rpc.call(site, 'crawl_category')
                                

def update_listing(site, rpc, concurrency=30):
    with UpdateContext(site=site, method='update_listing'):
        for category in spout_listing(site):
            for url in spout_category(category):
                try:
                    rpc.call(site, 'crawl_listing', url) 
                except Exception as e:
                    category_failed.send(sender="common.update_listing",
                                        site = site,
                                        url = url,
                                        reason = e.message)

def update_product(site, rpc, concurrency=30):
    with UpdateContext(site=site, method='update_product'):
        for url in spout_product(site):
            try:
                rpc.call(site, 'crawl_product', url)
            except Exception as e: 
                product_failed.send(sender="common.update_product",
                                    site = site,
                                    url = url,
                                    reason = e.message)
                

if __name__ == '__main__':
    from rpcserver import RPCServer
    rpc = RPCServer() 
    update_category('amazon', rpc) 
    #update_listing('amazon', rpc)
    #update_product('amazon', rpc)
