# -*- coding: utf-8 -*-
"""
crawlers.common.rpcserver
~~~~~~~~~~~~~~~~~~~~~~~~~

Provides a image processed workflow for all callers

"""

from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
import zerorpc
import uuid
import random
import traceback
from datetime import datetime

from mongoengine import Q
from settings import POWER_PEERS
from configs import SITES
from events import *

from helpers.rpc import get_rpcs

def get_site_module(site):
    return __import__('crawlers.'+site+'.models', fromlist=['Category', 'Event', 'Product'])

def call_rpc(rpc, method, *args, **kwargs):
    try:
        # print 'using rpc', rpc, method, args, kwargs
        getattr(rpc, method)(args, kwargs)
    except Exception:
        print traceback.format_exc()
        # image_crawled_failed.send(sender=kwargs['ctx'],
        #                     site = kwargs['ctx'],
        #                     key = kwargs.get('key') or kwargs.get('event_id'),
        #                     url = kwargs.get('url'),
        #                     reason = traceback.format_exc()
        #                     )

def spout_images(site, doctype):
    m = get_site_module(site)
    docdict = {
        'event': {
            'kwargs': {'urgent':False, 'image_complete':False},
            'key': 'event_id',
            'name': 'Event',
         }, 
        'product': {
            'kwargs': {'updated':True, 'image_complete':False},
            'key': 'key',
            'name': 'Product',
        }, 
    }
    
    docparam = docdict[doctype]
    instances = getattr(m, docparam['name']).objects(**docparam['kwargs'])

    for instance in instances:
        yield {
            'site': site,
            docparam['key']: getattr(instance, docparam['key']),
            'image_urls': instance.image_urls,
        }

def spout_brands(site, doctype):
    docdict = {
        'Event': {
            'key': 'event_id',
            'title': 'sale_title',
            'kwargs': {'brand_complete': False}    # TODO determinate the flag indication.
        },
        'Product': {
            'key': 'key',
            'title': 'title',
            'kwargs': {'brand_complete': False}   # TODO determinate the flag indication.
        }
    }

    model = doctype.capitalize()
    m = __import__('crawlers.{0}.models'.format(site), fromlist=[model])
    instances = getattr(m, model).objects(**docdict[model]['kwargs'])

    for instance in instances:
        yield {
            'site': site,
            'key': getattr(instance, docdict.get(model)['key']),
            'title': getattr(instance, docdict.get(model)['title']),
            'brand': instance.brand,
            'doctype': model,
            'combine_url': instance.combine_url,
        }

def spout_propagate_events(site):
    m = __import__('crawlers.{0}.models'.format(site), fromlist=['Event'])
    now = datetime.utcnow()
    events = m.Event.objects(Q(propagation_complete = False) & \
        (Q(events_begin__lte=now) | Q(events_begin__exists=False)) & \
            (Q(events_end__gt=now) | Q(events_end__exists=False)) )

    for event in events:
        yield {
            'event_id': event.event_id,
            'site': site,
        }

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
        pre_image_crawl.send(sender = self.sender,
                                    site = self.site,
                                    method = self.method)
        return self.sender

    def __exit__(self, exc_type, exc_value, exc_traceback):
        complete = True
        reason = ''
        if exc_type:
            complete = False
            reason = ''.join(traceback.format_tb(exc_traceback))+'{0!r}'.format(exc_value)
        
        post_image_crawl.send(sender = self.sender,
                                    site = self.site,
                                    method = self.method,
                                    complete = complete,
                                    reason = reason)

def scan_images(site, doctype, rpc, concurrency=3):
    with UpdateContext(site, 'crawl_images') as ctx:
        rpcs = [rpc] if not isinstance(rpc, list) else rpc
        pool = Pool(len(rpcs)*concurrency)
        for kwargs in spout_images(site, doctype):
            kwargs['ctx'] = ctx
            kwargs['doctype'] = doctype
            rpc = random.choice(rpcs)
            pool.spawn(call_rpc, rpc, 'process_image', **kwargs)
        pool.join()

def crawl_images(site, model, key, rpc=None, *args, **kwargs):
    if rpc is None:
        rpc = get_rpcs(POWER_PEERS)
    
    method = 'process_image'
    
    with UpdateContext(site, method) as ctx:
        newargs = {}
        m = __import__("crawlers."+site+'.models', fromlist=['Event', 'Product'])
        if model == 'Event':
            event = m.Event.objects.get(event_id=key)
            if event and not event.image_complete:
                newargs.__setitem__('site', site)
                newargs.__setitem__('event_id', event.event_id)
                newargs.__setitem__('image_urls', event.image_urls)
                newargs.__setitem__('ctx', ctx)
                newargs.__setitem__('doctype', 'event')
        elif model == 'Product':
            product = m.Product.objects.get(key=key)
            if product and not product.image_complete:
                newargs.__setitem__('site', site)
                newargs.__setitem__('key', product.key)
                newargs.__setitem__('image_urls', product.image_urls)
                newargs.__setitem__('ctx', ctx)
                newargs.__setitem__('doctype', 'product')
        
        if newargs and method:
            rpcs = [rpc] if not isinstance(rpc, list) else rpc
            rpc = random.choice(rpcs)
            call_rpc(rpc, method, **newargs)

def brand_extract(site, rpc, concurrency=3):
    """
    * Product brand extraction.
    """
    rpcs = [rpc] if not isinstance(rpc, list) else rpc
    pool = Pool(len(rpcs)*concurrency)
    products = spout_brands(site, 'product')

    for product in products:
        rpc = random.choice(rpcs)
        pool.spawn(call_rpc, rpc, 'extract_brand', **product)
    pool.join()
    
    propagate(site, rpc, concurrency)

def propagate(site, rpc, concurrency=3):
    """
    * Event brand propagation
    * Event (lowest, highest) discount, (lowest, highest) price propagation
    * Event & product begin_date, end_date
    * Event soldout
    * tag, dept extraction
    """
    rpcs = [rpc] if not isinstance(rpc, list) else rpc
    pool = Pool(len(rpcs)*concurrency)
    events = spout_propagate_events(site)

    for event in events:
        rpc = random.choice(rpcs)
        pool.spawn(call_rpc, rpc, 'propagate', **event)
    pool.join()


def test_brand(site):
    import time
    from powers.powerserver import PowerServer
    products = spout_brands(site, 'product')
    for product in products:
        s = PowerServer()
        print product
        s.extract_brand((), product)

if __name__ == '__main__':
    # from powers.powerserver import PowerServer
    # rpc = PowerServer()
    # print  POWER_PEERS
    # scan_images('zulily', 'event', get_rpcs(POWER_PEERS) , 3)
    #crawl_images('zulily', 'Event', 'parade-of-toys-112212')
    #scan_images('zulily', 'product', get_rpcs(), 3)
    import sys
    if len(sys.argv)>1:
        test_brand(sys.argv[1])
    else:
        test_brand()
