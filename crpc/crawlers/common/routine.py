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

import uuid
import time
import random
import traceback

from itertools import chain

from crawlers.common.events import pre_general_update, post_general_update, common_failed
from datetime import datetime, timedelta

MAX_PAGE = 400

def get_site_module(site):
    return __import__('crawlers.'+site+'.models', fromlist=['Category', 'Event', 'Product'])

def spout_listing(site):
    """ return a generator spouting listing pages """
    m = get_site_module(site)
    classname = 'Event' if hasattr(m, 'Event') else 'Category'
    return getattr(m, classname).objects(is_leaf=True).order_by('-update_time').timeout(False)

def spout_category(site, category):
    """ return a generator spouting category parameters """
    c = category
    if c.spout_time and c.spout_time > datetime.utcnow()-timedelta(hours=12):
        return
    if site == 'ecost':
        if c.num: # not None or 0
            yield {'url': c.link, 'catstr': c.cat_str, 'num': c.num}
        else:
            yield {'url': c.link, 'catstr': c.cat_str}
    elif site == 'bluefly':
        yield {'url':c.url}
    elif site == 'amazon':
        pages = (c.num-1)/c.pagesize+10
        for p in range(1, min(pages+1,MAX_PAGE+1)):
            url = c.url().format(p)
            yield {'url': url}
    else:
        yield {'url': c.url()}

    c.spout_time = datetime.utcnow()
    c.save()

def spout_product(site):
    """ return a generator spouting product url """
    m = get_site_module(site)
    p1 = m.Product.objects.filter(updated = False).timeout(False)
    p2 = m.Product.objects.filter(updated = True, 
            full_update_time__lt = datetime.utcnow()-timedelta(hours=24)).timeout(False)
    for p in chain(p1, p2):
        if site == 'ecost':
            yield {'url': p.url(), 'ecost': p.key}
        elif site  in ['ruelala','bluefly']:
            yield {'url':p.url}
        elif site == 'myhabit':
            yield {'url': p.url(), 'casin': p.key}
        else:
            yield {'url': p.url()}

class UpdateContext(object):
    """ the context manager for monitoring 
        
    wraps tedious signals passing inside the context manager
    
    Usage:

    >>> with MonitorContext(site='amazon', method='update_category'):
    ...     pass # do something related to site and method

    """
    def __init__(self, site, method):
        self.site = site
        self.method = method
        self.sender = "{0}.{1}.{2}".format(self.site, self.method, uuid.uuid4().hex)

    def __enter__(self):
        pre_general_update.send(sender = self.sender,
                                    site = self.site,
                                    method = self.method)
        return self.sender

    def __exit__(self, exc_type, exc_value, exc_traceback):
        complete = True
        reason = ''
        if exc_type:
            complete = False
            reason = ''.join(traceback.format_tb(exc_traceback))+'{0!r}'.format(exc_value)

        post_general_update.send(sender = self.sender,
                                    site = self.site,
                                    method = self.method,
                                    complete = complete,
                                    reason = reason)

def callrpc(rpc, site, method, *args, **kwargs):
    """ rpc call with failure protection """
    try:
        rpc.call(site, method, args, kwargs)
    except Exception as e:
        common_failed.send(sender=kwargs['ctx'],
                            site = site,
                            key = kwargs.get('key'),
                            url = kwargs.get('url'),
                            reason = traceback.format_exc())

def gevent_exception_handler():
    pass

def update_category(site, rpc, concurrency=30):
    with UpdateContext(site=site, method='update_category') as ctx:
        rpcs = [rpc] if not isinstance(rpc, list) else rpc
        rpc = random.choice(rpcs)
        callrpc(rpc, site, 'crawl_category', ctx=ctx)

def update_listing(site, rpc, concurrency=30):
    with UpdateContext(site=site, method='update_listing') as ctx:
        rpcs = [rpc] if not isinstance(rpc, list) else rpc
        pool = Pool(len(rpcs)*concurrency)
        for category in spout_listing(site):
            for kwargs in spout_category(site, category):
                kwargs['ctx'] = ctx
                rpc = random.choice(rpcs)
                pool.spawn(callrpc, rpc, site, 'crawl_listing', **kwargs)
        pool.join()

def update_product(site, rpc, concurrency=30):
    with UpdateContext(site=site, method='update_product') as ctx:
        rpcs = [rpc] if not isinstance(rpc, list) else rpc
        pool = Pool(len(rpcs)*concurrency)
        for kwargs in spout_product(site):
            kwargs['ctx'] = ctx
            rpc = random.choice(rpcs)
            pool.spawn(callrpc, rpc, site, 'crawl_product', **kwargs)
        pool.join()


if __name__ == '__main__':
    from rpcserver import RPCServer
    site = 'amazon'
    rpc = RPCServer() 
    #update_category(site,rpc)
    #update_listing('amazon',rpc)
    update_product('amazon', rpc)
    #update_category('myhabit', rpc)
