# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
import gevent
from mongoengine import Q

from settings import POWER_PEERS, TEXT_PEERS
from events import *
from helpers.rpc import get_rpcs
from crawlers.common.stash import picked_crawlers

import uuid
import random
import traceback
from datetime import datetime

from helpers.log import getlogger
logger = getlogger('powerroutine', filename='/tmp/powerroutine.log')


def get_site_module(site):
    if not hasattr(get_site_module, 'mod'):
        setattr(get_site_module, 'mod', {})

    if not get_site_module.mod:
        for crawler in picked_crawlers:
            get_site_module.mod[crawler] = __import__('crawlers.'+ crawler +'.models', fromlist=['Category', 'Event', 'Product'])
    
    if site not in get_site_module.mod:
        get_site_module.mod[site] = __import__('crawlers.'+ site +'.models', fromlist=['Category', 'Event', 'Product'])
    
    return get_site_module.mod[site]


def call_rpc(rpc, method, *args, **kwargs):
    try:
        return getattr(rpc, method)(args, kwargs)
    except Exception as e:
        logger.error('call rpc error: {0}'.format(traceback.format_exc()))
        print traceback.format_exc()


def spout_images(site, doctype):
    m = get_site_module(site)
    docdict = {
        'event': {
            'key': 'event_id',
            'name': 'Event',
         }, 
        'product': {
            'key': 'key',
            'name': 'Product',
        },
    }
    
    try:
        now = datetime.utcnow()
        if doctype.lower() == 'event':
            instances = m.Event.objects(Q(events_end__gt=now) | \
                Q(events_end__exists=False)).timeout(False)
        elif doctype.lower() == 'product':
            instances = m.Product.objects.where(" (this.image_complete == false) || \
                    ( (this.products_begin == undefined || this.products_begin <= ISODate()) && (this.products_end == undefined || this.products_end >= ISODate()) && (this.update_history.image_urls != undefined && this.update_history.image_path != undefined && this.update_history.image_urls > this.update_history.image_path) ) ").timeout(False)

#            instances = m.Product.objects( \
#                (Q(products_begin__lte=now) | Q(products_begin__exists=False)) & \
#                    (Q(products_end__gt=now) | Q(products_end__exists=False))).timeout(False)
    except AttributeError:
        instances = []

    docparam = docdict[doctype.lower()]
    for instance in instances:
#        update_flag = bool( instance.update_history.get('image_urls') and instance.update_history.get('image_path') and \
#                instance.update_history.get('image_urls') > instance.update_history.get('image_path') )
#        if instance.image_complete and not update_flag:
#            continue
        
        yield {
            'site': site,
            'doctype': doctype,
            docparam['key']: getattr(instance, docparam['key']),
        }


def spout_extracted_products(site):
    m = get_site_module(site)

    if not hasattr(m, 'Category'):
        return

    now = datetime.utcnow()
    # products = m.Product.objects((Q(brand_complete = False) | \
    #             Q(tag_complete = False) | Q(dept_complete = False)) & \
    #                 (Q(products_begin__lte=now) | Q(products_begin__exists=False)) & \
    #                     (Q(products_end__gt=now) | Q(products_end__exists=False))).timeout(False)

    products = m.Product.objects( \
        (Q(products_begin__lte=now) | Q(products_begin__exists=False)) & \
            (Q(products_end__gt=now) | Q(products_end__exists=False)))

    for product in products:
        yield {
            'site': site,
            'key': product.key,
        }


def spout_propagate_events(site, complete=False):
    m = get_site_module(site)

    if not hasattr(m, 'Event'):
        return

    try:
        logger.debug('spout {0} events to propagate and update propagate'.format(site))
        now = datetime.utcnow()
        events = m.Event.objects(Q(events_end__gt=now) | \
            Q(events_end__exists=False)).timeout(False)
        logger.debug('{0} events spouted'.format(site))
    except AttributeError:
        events = []

    for event in events:
        yield {
            'event_id': event.event_id,
            'site': site,
        }


def scan_images(site, doctype, concurrency=3):
    """ If one site is already been scanning, not scan it this time
    """
    try:
        rpcs = get_rpcs(POWER_PEERS)
        pool = Pool(len(rpcs)*concurrency)
        for kwargs in spout_images(site, doctype):
            rpc = random.choice(rpcs)
            pool.spawn(call_rpc, rpc, 'process_image', **kwargs)
        pool.join()
    except Exception as e:
        logger.error('scan images {0}.{1} error: {2}'.format(site, doctype, traceback.format_exc()))


def crawl_images(site, doctype, key, *args, **kwargs):
    newargs = {}
    m = get_site_module(site)
    model = doctype.capitalize()
    if model == 'Event':
        event = m.Event.objects.get(event_id=key)
        if event and not event.image_complete:
            newargs.__setitem__('site', site)
            newargs.__setitem__('event_id', event.event_id)
            newargs.__setitem__('doctype', 'event')
    elif model == 'Product':
        product = m.Product.objects.get(key=key)
        if product and not product.image_complete:
            newargs.__setitem__('site', site)
            newargs.__setitem__('key', product.key)
            newargs.__setitem__('doctype', 'product')

    if newargs:
        rpcs = get_rpcs(POWER_PEERS)
        rpc = random.choice(rpcs)
        call_rpc(rpc, 'process_image', **newargs)


def propagate(site, concurrency=3):
    rpcs = get_rpcs(TEXT_PEERS)
    pool = Pool(len(rpcs)*concurrency)
    events = spout_propagate_events(site)

    if events:
        logger.debug('{0} events to call rpc'.format(site))
        for event in events:
            rpc = random.choice(rpcs)
            pool.spawn(call_rpc, rpc, 'propagate', **event)
        pool.join()

    # The site has no events(maybe just has category) to propagate, so call the rpc to process products.
    extract_product(site, concurrency)


def extract_product(site, concurrency=3):
    rpcs = get_rpcs(TEXT_PEERS)
    pool = Pool(len(rpcs)*concurrency)
    products = spout_extracted_products(site)

    if products:
        logger.debug('{0} products to call rpc'.format(site))
        for product in products:
            rpc = random.choice(rpcs)
            pool.spawn(call_rpc, rpc, 'process_product', **product)
        pool.join()


if __name__ == '__main__':
    import sys
    extract_product(sys.argv[1]) 
