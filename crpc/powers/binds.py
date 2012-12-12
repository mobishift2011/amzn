#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
from crawlers.common.events import common_saved
from powers.events import *
from powers.routine import scan_images, brand_extract, propagate
from powers.models import EventProgress, ProductProgress

from datetime import datetime

import gevent
import gevent.coros

from settings import POWER_PEERS

from helpers.log import getlogger
from helpers.rpc import get_rpcs

from powers.routine import crawl_images

logger = getlogger("powers.bind")

import gevent.pool
process_image_pool = gevent.pool.Pool(500)

@common_saved.bind
def single_process_image(sender, **kwargs):
    logger.warning('single_process_image enter:{0} -> {1}'.format(sender, kwargs.items()))
    key = kwargs.get('key', None)
    ready = kwargs.get('ready', None)   # Event or Product
    obj_type = kwargs.get('obj_type', '')
    site, method, dummy = sender.split('.')

    if not ready:
        return

    if site and key and obj_type.capitalize() in ('Event', 'Product'):
        logger.warning('%s %s %s queries for crawling images' % (site, obj_type, key))
        process_image_pool.spawn(crawl_images, site, obj_type, key)
    else:
        logger.warning('%s failed to start crawling image', sender)
        # TODO send a process_message error signal.


@ready_for_batch.bind
def ready_for_batch_image_crawling(sender, **kwargs):
    logger.warning("{0} finish is listened, start to ready for batch {1} image crawl".format(sender, kwargs.get('doctype')))
    site = kwargs.get('site')
    doctype = kwargs.get('doctype')

    if site and doctype:
        logger.info('start to get rpc resource for %s.%s' % (site, doctype))
        gevent.spawn(scan_images, site, doctype, get_rpcs(POWER_PEERS), 10) 


@ready_for_batch.bind
def ready_for_extract(sender, **kwargs):
    doctype = kwargs.get('doctype')
    if doctype.capitalize() == 'Product':
        site = kwargs.get('site')
        logger.info('start to extract site products brand: %s', site)
        job = gevent.spawn(brand_extract, site, get_rpcs(POWER_PEERS), 10)
        job.join()
        
        ready_for_publish.send(sender, **kwargs)
        

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
    # try:
    #     m = __import__("crawlers."+site+'.models', fromlist=['Event', 'Product'])
    #     entity = None
    #     if model == 'Event':
    #         EventProgress.objects(site=site, key=key).update(set__image_complete=True,
    #                                                          set__num_image=num,
    #                                                          set__updated_at=datetime.utcnow(),
    #                                                          upsert=True)
    #         m.Event.objects(event_id=key).update(set__image_complete=True)
            
    #     elif model == 'Product':
    #         ProductProgress.objects(site=site, key=key).update(set__image_complete=True,
    #                                                            set__num_image=num,
    #                                                            set__updated_at=datetime.utcnow(),
    #                                                            upsert=True)
    #         m.Product.objects(key=key).update(set__image_complete=True)
            
    # except Exception as e:
    #     logger.exception(e.message)


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djCatalog.djCatalog.settings")
from djCatalog.catalogs.models import BrandTask

@brand_extracted.bind
def brand_stat_save(sender, **kwargs):
    kwargs['brand_complete'] = True
    brand_stat(sender, **kwargs)

@brand_extracted_failed.bind
def brand_stat_failed(sender, **kwargs):
    kwargs['brand_complete'] = False
    brand_stat(sender, **kwargs)

def brand_stat(sender, **kwargs):
    site = kwargs.get('site', '')
    key = kwargs.get('key', '')
    title = kwargs.get('title', '')
    brand = kwargs.get('brand', '')
    doctype = kwargs.get('doctype', '')
    url = kwargs.get('combine_url', '')
    brand_complete = kwargs.get('brand_complete', False)
    favbuy_brand = kwargs.get('favbuy_brand', '')
    
    BrandTask.objects(site=site, key=key, doctype=doctype).update(
        set__title = title,
        set__brand = brand,
        set__site = site,
        set__doctype = doctype,
        set__key = key,
        set__favbuy_brand = favbuy_brand,
        set__url=url,
        set__brand_complete=brand_complete,
        upsert = True
    )
