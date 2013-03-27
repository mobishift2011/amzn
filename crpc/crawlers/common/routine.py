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
rpc:            an CrawlerServer instance
concurrency:    how much concurrency should be achieved

"""
from settings import *
from gevent.pool import Pool

import uuid
import time
import random
import traceback

from datetime import datetime, timedelta
from itertools import chain
from functools import partial
from mongoengine import Q

from crawlers.common.events import pre_general_update, post_general_update, common_failed
from crawlers.common.stash import get_login_email, deal_crawlers

from powers.events import ready_for_batch

MAX_PAGE = 400

def get_site_module(site):
    return __import__('crawlers.'+site+'.models', fromlist=['Category', 'Event', 'Product'])

def spout_listing(site):
    """ return a generator spouting listing pages

        spout event off sale then on sale again.
        now > events_begin > events_end, old spout will not spout them when on sale again.
    """
    m = get_site_module(site)
    now = datetime.utcnow()
    isonow = now.isoformat()
    if hasattr(m, 'Event'):
#        for event in m.Event.objects(Q(urgent=True) & (Q(events_begin__lte=now) | Q(events_begin__exists=False)) & (Q(events_end__gte=now) | Q(events_end__exists=False)) & (Q(is_leaf=True) | Q(is_leaf__exists=False))).timeout(False):
        for event in m.Event.objects.where("this.urgent==true && (this.is_leaf!=false) && (((this.events_begin==undefined || this.events_begin <= ISODate('{0}')) && (this.events_end==undefined || this.events_end >= ISODate('{0}'))) || (this.events_begin > this.events_end && this.events_begin < ISODate('{0}')))".format(isonow)).timeout(False):
            yield event
    if hasattr(m, 'Category'):
        for category in m.Category.objects(is_leaf=True).order_by('update_time').timeout(False):
            yield category

def spout_listing_update(site):
    """ return a generator spouting listing pages """
    m = get_site_module(site)
    now = datetime.utcnow()
    isonow = now.isoformat()
    if hasattr(m, 'Event'):
#        for event in m.Event.objects(Q(urgent=False) & (Q(events_begin__lte=now) | Q(events_begin__exists=False)) & (Q(events_end__gte=now) | Q(events_end__exists=False)) & (Q(is_leaf=True) | Q(is_leaf__exists=False))).timeout(False):
        for event in m.Event.objects.where("this.urgent==false && (this.is_leaf!=false) && (((this.events_begin==undefined || this.events_begin <= ISODate('{0}')) && (this.events_end==undefined || this.events_end >= ISODate('{0}'))) || (this.events_begin > this.events_end && this.events_begin < ISODate('{0}')))".format(isonow)).timeout(False):
            yield event
    if hasattr(m, 'Category'):
        for category in m.Category.objects(is_leaf=True).order_by('update_time').timeout(False):
            yield category


def spout_category(site, category):
    """ return a generator spouting category parameters """
    c = category
#    if c.spout_time and c.spout_time > datetime.utcnow()-timedelta(hours=12):
#        return
    if site == 'ecost':
        if c.num: # not None or 0
            yield {'url': c.link, 'catstr': c.cat_str, 'num': c.num}
        else:
            yield {'url': c.link, 'catstr': c.cat_str}
    elif site == 'amazon':
        pages = (c.num-1)/c.pagesize+10
        for p in range(1, min(pages+1,MAX_PAGE+1)):
            url = c.url().format(p)
            yield {'url': url}
    elif site == 'ebags':
        pages = (c.num - 1) / c.pagesize
        for p in xrange(1, pages+1):
            url = '{0}?items={1}?page={2}'.format(c.url(), c.pagesize, p)
            yield {'url': url}
    elif site in deal_crawlers:
        yield {'url': c.url(), 'key': c.key}
    else:
        yield {'url': c.url()}

    c.spout_time = datetime.utcnow()
    c.save()

def spout_product(site):
    """ return a generator spouting product url """
    m = get_site_module(site)
    now = datetime.utcnow()
    p1 = m.Product.objects(updated=False).timeout(False)
#    p2 = m.Product.objects.filter(updated = True, 
#            full_update_time__lt = datetime.utcnow()-timedelta(hours=24)).timeout(False)
    for p in chain(p1):
        if site == 'ecost':
            yield { 'url': p.url(), 'ecost': p.key }
        elif site == 'myhabit':
            yield { 'url': p.url(), 'casin': p.key }
        elif site in deal_crawlers:
            yield {'url': p.url(), 'key': p.key}
        else:
            yield { 'url': p.url() }

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


#
# new or update parent task with sevral sequential children tasks
#
def update_category(site, rpc, method='update_category', concurrency=5, **wargs):
    with UpdateContext(site=site, method=method) as ctx:
        rpcs = [rpc] if not isinstance(rpc, list) else rpc
        rpc = random.choice(rpcs)
        callrpc(rpc, site, 'crawl_category', ctx=ctx, login_email=wargs.get('login_email', ''))


def update_listing(site, rpc, method='update_listing', concurrency=5, **wargs):
    keep_ctx = None
    with UpdateContext(site=site, method=method) as ctx:
        keep_ctx = ctx
        rpcs = [rpc] if not isinstance(rpc, list) else rpc
        pool = Pool(len(rpcs)*concurrency)
        for category in spout_listing_update(site):
            for kwargs in spout_category(site, category):
                kwargs['ctx'] = ctx
                kwargs['login_email'] = wargs.get('login_email', '')
                rpc = random.choice(rpcs)
                pool.spawn(callrpc, rpc, site, 'crawl_listing', **kwargs)
        pool.join()

    ready_for_batch.send(sender=keep_ctx, site=site, doctype='event')

def update_product(site, rpc, method='update_product', concurrency=5, **wargs):
    keep_ctx = None
    with UpdateContext(site=site, method=method) as ctx:
        keep_ctx = ctx
        rpcs = [rpc] if not isinstance(rpc, list) else rpc
        pool = Pool(len(rpcs)*concurrency)
        for kwargs in spout_product(site):
            kwargs['ctx'] = ctx
            kwargs['login_email'] = wargs.get('login_email', '')
            rpc = random.choice(rpcs)
            pool.spawn(callrpc, rpc, site, 'crawl_product', **kwargs)
        pool.join()

    ready_for_batch.send(sender=keep_ctx, site=site, doctype='product')

def new_listing(site, rpc, method='new_listing', concurrency=5, **wargs):
    keep_ctx = None
    with UpdateContext(site=site, method=method) as ctx:
        keep_ctx = ctx
        rpcs = [rpc] if not isinstance(rpc, list) else rpc
        pool = Pool(len(rpcs)*concurrency)
        for category in spout_listing(site): # different spout
            for kwargs in spout_category(site, category):
                kwargs['ctx'] = ctx
                kwargs['login_email'] = wargs.get('login_email', '')
                rpc = random.choice(rpcs)
                pool.spawn(callrpc, rpc, site, 'crawl_listing', **kwargs)
        pool.join()

    ready_for_batch.send(sender=keep_ctx, site=site, doctype='event')

# alias for easily invoking by monitor
new_category = partial(update_category, method='new_category')
new_product = partial(update_product, method='new_product')


# parent task of update
def update(site, rpc, method='update', concurrency=5):
    login_email = get_login_email(site)
    update_category(site, rpc, '{0}_category'.format(method), concurrency, login_email=login_email)
    update_listing(site, rpc, '{0}_listing'.format(method), concurrency, login_email=login_email)
    update_product(site, rpc, '{0}_product'.format(method), concurrency, login_email=login_email)

# parent task of new
def new(site, rpc, method='new', concurrency=5):
    login_email = get_login_email(site)
    new_category(site, rpc, concurrency=concurrency, login_email=login_email)
    new_listing(site, rpc, concurrency=concurrency, login_email=login_email)
    new_product(site, rpc, concurrency=concurrency, login_email=login_email)

def new_thrice(site, rpc, method='new', concurrency=5):
    new(site, rpc, 'new', concurrency)
    new(site, rpc, 'new', concurrency)
    new(site, rpc, 'new', concurrency)


if __name__ == '__main__':
    from rpcserver import CrawlerServer
    site = 'amazon'
    rpc = CrawlerServer() 
    update_category(site,rpc)
    update_listing(site,rpc)
    update_product(site, rpc)
