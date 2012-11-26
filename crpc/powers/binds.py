#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
from crawlers.common.events import common_saved
from powers.events import *
from powers.routine import scan_images
from powers.models import EventProgress, ProductProgress

from datetime import datetime

import gevent
import gevent.coros

from settings import POWER_PEERS, POWER_PORT

from helpers.log import getlogger
from helpers.rpc import get_rpcs

logger = getlogger("powers.bind")

#common_saved_lock = gevent.coros.Semaphore()

@common_saved.bind
def single_process_image(sender, **kwargs):
    logger.warning('single_process_image enter:{0} -> {1}'.format(sender, kwargs.items()))
    key = kwargs.get('key', None)
    ready = kwargs.get('ready', None)   # Event or Product
    site, method, dummy = sender.split('.')

    if not ready:
        return

    if site and key and ready in ('Event', 'Product'):
        logger.warning('%s %s %s queries for crawling images' % (site, ready, key))
        from powers.routine import crawl_images
        # with common_saved_lock:
        crawl_images(site, ready, key)
    else:
        logger.warning('%s failed to start crawling image', sender)
        # TODO send a process_message error signal.

@ready_for_batch_image_crawling.bind
def batch_image_crawl(sender, **kwargs):
    logger.warning("{0} finish is listened, start to ready for batch {1} image crawl".format(sender, kwargs.get('doctype')))
    site = kwargs.get('site')
    doctype = kwargs.get('doctype')

    if site and doctype:
        logger.info('start to get rpc resource for %s.%s' % (site, doctype))
        gevent.spawn(scan_images, site, doctype, get_rpcs(POWER_PEERS, POWER_PORT), 10) 

#@pre_image_crawl.bind
def stat_pre_general_update(sender, **kwargs):
    pass

#@post_image_crawl.bind
def stat_post_general_update(sender, **kwargs):
    pass

#@image_crawled_failed.bind
def stat_failed(sender, **kwargs):
    pass

@image_crawled.bind
def stat_save(sender, **kwargs):
    logger.debug('{0} -> {1}'.format(sender,kwargs.items()))
    site = kwargs.get('site', '')
    key = kwargs.get('key', '')
    model = kwargs.get('model', '')
    num = kwargs.get('num', '')
    
    print '{0}.{1}.{2}.crawled_image_num:{3}'.format(site, key, model, num)
    # to ensure the event or product flag is indicated after the progress has been done.
    try:
        m = __import__("crawlers."+site+'.models', fromlist=['Event', 'Product'])
        entity = None
        if model == 'Event':
            EventProgress.objects(site=site, key=key).update(set__image_complete=True,
                                                             set__num_image=num,
                                                             set__updated_at=datetime.utcnow(),
                                                             upsert=True)
            m.Event.objects(event_id=key).update(set__image_complete=True)
            
        elif model == 'Product':
            ProductProgress.objects(site=site, key=key).update(set__image_complete=True,
                                                               set__num_image=num,
                                                               set__updated_at=datetime.utcnow(),
                                                               upsert=True)
            m.Product.objects(key=key).update(set__image_complete=True)
            
    except Exception as e:
        logger.exception(e.message)
