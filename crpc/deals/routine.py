#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
deals.routine
~~~~~~~~~~~~~~~~~~~~~~~

a routine library abstracts daily jobs for every crawler for deals

the following functions are supposed to be called from other module

- update_category(site, rpc, concurrency)
- update_listing(site, rpc, concurrency)
- update_product(site, rpc, concurrency)

site:           name of the crawler's directory
rpc:            an CrawlerServer instance
concurrency:    how much concurrency should be achieved

"""
from settings import *
from crawlers.common.events import pre_general_update, post_general_update, common_failed
from gevent.pool import Pool
import traceback
import uuid
import random
from datetime import datetime, timedelta
import time

from itertools import chain
from functools import partial
from mongoengine import Q

from helpers.log import getlogger
logger = getlogger('routine', filename='/tmp/deals.log')

mod = {}
def get_site_module(site):
    if not mod.get(site):
        mod[site] = __import__('crawlers.'+site+'.models', fromlist=['Category', 'Product'])

    return mod.get(site)


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
        logger.error('callrpc error: %s\n%s\n%s\n%s\n%s\n' % (site, method, args, kwargs, traceback.format_exc()))


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
        self.sender = "{0}.{1}.{2}".format(self.site, self.method, uuid.uuid1().hex + uuid.uuid4().hex)

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


def spout_listing(site, updated=False):
    m = get_site_module(site)
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    categories = m.Category.objects(hit_time__gt=today)

    for category in categories:
        yield {
            'url': category.combine_url,
        }


def spout_product(site, updated=False):
    m = get_site_module(site)
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    products = m.Product.objects(hit_time__gt=today, updated=updated)

    for product in products:
        yield {
            'key': product.key,
            'url': product.combine_url,
        }


def update_category(site, rpc, method='update_category', concurrency=5, **kwargs):
    print 'update_category'
    with UpdateContext(site=site, method=method) as ctx:
        rpcs = [rpc] if not isinstance(rpc, list) else rpc
        rpc = random.choice(rpcs)
        callrpc(rpc, site, 'crawl_category', ctx=ctx)


def update_listing(site, rpc, method='update_listing', concurrency=5, **kwargs):
    with UpdateContext(site=site, method=method) as ctx:
        rpcs = [rpc] if not isinstance(rpc, list) else rpc
        pool = Pool(len(rpcs)*concurrency)
        for category in spout_listing(site):
            kwargs['ctx'] = ctx
            rpc = random.choice(rpcs)
            pool.spawn(callrpc, rpc, site, 'crawl_listing', **kwargs)
        pool.join()


def update_product(site, rpc, method='update_product', concurrency=5, **wargs):
    with UpdateContext(site=site, method=method) as ctx:
        rpcs = [rpc] if not isinstance(rpc, list) else rpc
        pool = Pool(len(rpcs)*concurrency)
        for kwargs in spout_product(site):
            kwargs['ctx'] = ctx
            rpc = random.choice(rpcs)
            pool.spawn(callrpc, rpc, site, 'crawl_product', **kwargs)
        pool.join()


# parent task of update
def update(site, rpc, method='update', concurrency=5):
    update_category(site, rpc, '{0}_category'.format(method), concurrency)
    update_listing(site, rpc, '{0}_listing'.format(method), concurrency)
    update_product(site, rpc, '{0}_product'.format(method), concurrency)