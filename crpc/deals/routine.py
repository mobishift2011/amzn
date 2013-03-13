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
from crawlers.common.routine import callrpc, UpdateContext
from gevent.pool import Pool
import random
from datetime import datetime, timedelta
import time

from itertools import chain
from functools import partial

from helpers.log import getlogger
logger = getlogger('routine', filename='/tmp/deals.log')

mod = {}
def get_site_module(site):
    if not mod.get(site):
        mod[site] = __import__('crawlers.'+site+'.models', fromlist=['Category', 'Product'])

    return mod.get(site)


def spout_listing(site, updated=False):
    m = get_site_module(site)
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    try:
        categories = m.Category.objects(hit_time__gt=today)
    except AttributeError:
        return

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
            category['ctx'] = ctx
            rpc = random.choice(rpcs)
            pool.spawn(callrpc, rpc, site, 'crawl_listing', **category)
        pool.join()


def update_product(site, rpc, method='update_product', concurrency=5, **kwargs):
    with UpdateContext(site=site, method=method) as ctx:
        rpcs = [rpc] if not isinstance(rpc, list) else rpc
        pool = Pool(len(rpcs)*concurrency)
        for product in spout_product(site):
            product['ctx'] = ctx
            rpc = random.choice(rpcs)
            pool.spawn(callrpc, rpc, site, 'crawl_product', **product)
        pool.join()


# parent task of update
def update(site, rpc, method='update', concurrency=5):
    update_category(site, rpc, '{0}_category'.format(method), concurrency)
    update_listing(site, rpc, '{0}_listing'.format(method), concurrency)
    update_product(site, rpc, '{0}_product'.format(method), concurrency)