# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
import gevent
from mongoengine import Q

from settings import POWER_PEERS, TEXT_PEERS
from events import *
from helpers.rpc import get_rpcs

import uuid
import random
import traceback
from datetime import datetime

from helpers.log import getlogger
imglogger = getlogger('powerroutine', filename='/tmp/powerserver.log')


debug_logger = getlogger('debug_power_text', '/tmp/debug_power_text.log')
def run_fd():
    import subprocess, os
    pid = subprocess.Popen('ps aux | grep run.py | grep -v grep | grep -v dtach', shell=True, stdout=subprocess.PIPE).communicate()[0].split()[1]
    ret = os.listdir('/proc/{0}/fd'.format(pid))
    return len(ret)


from crawlers.common.stash import picked_crawlers
def get_site_module(site):
    if not hasattr(get_site_module, 'mod'):
        setattr(get_site_module, 'mod', {})

    if not get_site_module.mod:
        for crawler in picked_crawlers:
            get_site_module.mod[crawler] = __import__('crawlers.'+ crawler +'.models', fromlist=['Category', 'Event', 'Product'])
    return get_site_module.mod[site]

def call_rpc(rpc, method, *args, **kwargs):
    try:
        return getattr(rpc, method)(args, kwargs)
    except Exception:
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
    try:
        instances = getattr(m, docparam['name']).objects(**docparam['kwargs']).timeout(False)
    except AttributeError:
        instances = []

    for instance in instances:
        yield {
            'site': site,
            'doctype': doctype,
            docparam['key']: getattr(instance, docparam['key']),
            'image_urls': instance.image_urls,
        }

def spout_extracted_products(site):
    m = get_site_module(site)
    now = datetime.utcnow()
    products = m.Product.objects((Q(brand_complete = False) | \
                Q(tag_complete = False) | Q(dept_complete = False)) & \
                    (Q(products_begin__lte=now) | Q(products_begin__exists=False)) & \
                        (Q(products_end__gt=now) | Q(products_end__exists=False))).timeout(False)

    # products = m.Product.objects(Q(dept_complete = False) & \
    #                 (Q(products_begin__lte=now) | Q(products_begin__exists=False)) & \
    #                     (Q(products_end__gt=now) | Q(products_end__exists=False)))

    for product in products:
        yield {
            'site': site,
            'key': product.key,
        }

def spout_propagate_events(site, complete=False):
    m = __import__('crawlers.{0}.models'.format(site), fromlist=['Event'])
    now = datetime.utcnow()
    try:
        events = m.Event.objects(Q(propagation_complete = complete) & \
            (Q(events_begin__lte=now) | Q(events_begin__exists=False)) & \
                (Q(events_end__gt=now) | Q(events_end__exists=False)) )
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
    if not hasattr(scan_images, 'run_flag'):
        setattr(scan_images, 'run_flag', {})

    if site in scan_images.run_flag and scan_images.run_flag[site] == True:
        return
    elif site not in scan_images.run_flag or scan_images.run_flag[site] == False:
        scan_images.run_flag[site] = True

    try:
        rpcs = get_rpcs(POWER_PEERS)
        pool = Pool(len(rpcs)*concurrency)
        for kwargs in spout_images(site, doctype):
            rpc = random.choice(rpcs)
            pool.spawn(call_rpc, rpc, 'process_image', **kwargs)
        pool.join()
    except Exception as e:
        imglogger.error('scan_images {0}.{1} error: {2}'.format(site, doctype, e.message))
    finally:
        scan_images.run_flag[site] = False


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

def update_propation(site, concurrency=3):
    rpcs = get_rpcs(TEXT_PEERS)
    pool = Pool(len(rpcs)*concurrency)
    events = spout_propagate_events(site, complete=True)
    
    for event in events:
        rpc = random.choice(rpcs)
        pool.spawn(call_rpc, rpc, 'update_propation', **event)
    pool.join()

def text_extract(site, concurrency=3):
    """
    * Product brand extraction.
    """
    rpcs = get_rpcs(TEXT_PEERS)
    pool = Pool(len(rpcs)*concurrency)
    debug_logger.info('Extract text begin[{0}], fd number: {1}'.format(site, run_fd()))
    products = spout_extracted_products(site)
    
    for product in products:
        rpc = random.choice(rpcs)
        pool.spawn(call_rpc, rpc, 'extract_text', **product)
    pool.join()
    debug_logger.info('Extract text end[{0}], fd number: {1}'.format(site, run_fd()))

    # If site has event model, it should update and new the event propagation
    # jobs = [gevent.spawn(update_propation, event_dict, site), \
    #             gevent.spawn(propagate, site, concurrency)]
    # gevent.joinall(jobs)
    debug_logger.info('Propagation begin[{0}], fd number: {1}'.format(site, run_fd()))
    update_propation(site, concurrency)
    propagate(site, concurrency)
    debug_logger.info('Propagation end[{0}], fd number: {1}'.format(site, run_fd()))


if __name__ == '__main__':
    pass
