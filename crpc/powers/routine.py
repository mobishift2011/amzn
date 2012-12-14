# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
from mongoengine import Q

from settings import POWER_PEERS, TEXT_PEERS
from events import *
from helpers.rpc import get_rpcs

import uuid
import random
import traceback
from datetime import datetime

def get_site_module(site):
    return __import__('crawlers.'+site+'.models', fromlist=['Category', 'Event', 'Product'])

def call_rpc(rpc, method, *args, **kwargs):
    if True:
    # try:
        getattr(rpc, method)(args, kwargs)
    # except Exception:
        print traceback.format_exc()

def spout_images(site, doctype):
    m = get_site_module(site)
    docdict = {
        'event': {
            'kwargs': {'image_complete':False},
            'key': 'event_id',
            'name': 'Event',
         }, 
        'product': {
            'kwargs': {'updated':True, 'image_complete':False},
            'key': 'key',
            'name': 'Product',
        }, 
    }
    
    docparam = docdict[doctype.lower()]
    instances = getattr(m, docparam['name']).objects(**docparam['kwargs'])

    for instance in instances:
        yield {
            'site': site,
            'doctype': doctype,
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

def scan_images(site, doctype, concurrency=3):
    rpcs = get_rpcs(POWER_PEERS)
    pool = Pool(len(rpcs)*concurrency)
    for kwargs in spout_images(site, doctype):
        rpc = random.choice(rpcs)
        pool.spawn(call_rpc, rpc, 'process_image', **kwargs)

def crawl_images(site, doctype, key, *args, **kwargs):
    newargs = {}
    m = __import__("crawlers."+site+'.models', fromlist=['Event', 'Product'])
    model = doctype.capitalize()
    if model == 'Event':
        event = m.Event.objects.get(event_id=key)
        if event and not event.image_complete:
            newargs.__setitem__('site', site)
            newargs.__setitem__('event_id', event.event_id)
            newargs.__setitem__('image_urls', event.image_urls)
            newargs.__setitem__('doctype', 'event')
    elif model == 'Product':
        product = m.Product.objects.get(key=key)
        if product and not product.image_complete:
            newargs.__setitem__('site', site)
            newargs.__setitem__('key', product.key)
            newargs.__setitem__('image_urls', product.image_urls)
            newargs.__setitem__('doctype', 'product')

    if newargs:
        rpcs = get_rpcs(POWER_PEERS)
        rpc = random.choice(rpcs)
        call_rpc(rpc, 'process_image', **newargs)

def propagate(site, concurrency=3):
    """
    * Event brand propagation
    * Event (lowest, highest) discount, (lowest, highest) price propagation
    * Event & product begin_date, end_date
    * Event soldout
    * tag, dept extraction
    """
    rpcs = get_rpcs(TEXT_PEERS)
    pool = Pool(len(rpcs)*concurrency)
    events = spout_propagate_events(site)

    for event in events:
        rpc = random.choice(rpcs)
        pool.spawn(call_rpc, rpc, 'propagate', **event)
    pool.join()

    ready_for_publish.send(None, **{'site': site})

def brand_extract(site, concurrency=3):
    """
    * Product brand extraction.
    """
    rpcs = get_rpcs(TEXT_PEERS)
    pool = Pool(len(rpcs)*concurrency)
    products = spout_brands(site, 'product')

    for product in products:
        rpc = random.choice(rpcs)
        pool.spawn(call_rpc, rpc, 'extract_brand', **product)
    pool.join()
    
    propagate(site, concurrency)


if __name__ == '__main__':
    pass
