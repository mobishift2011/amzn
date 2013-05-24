#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import gevent

from backends.matching.mechanic_classifier import classify_product_department, guess_event_dept

from crawlers.common.events import common_saved
from crawlers.common.stash import deal_crawlers
from powers.events import *
from powers.routine import crawl_images, scan_images, propagate, get_site_module
from settings import POWER_PEERS, TEXT_PEERS

from helpers.rpc import get_rpcs
from helpers.log import getlogger
logger = getlogger("powersignals", '/tmp/powersignals.log')

import traceback
import gevent.pool
process_image_pool = gevent.pool.Pool(500)

try:
    from deals.routine import clean_product
except ImportError:
    logger.error(traceback.format_exc())

@common_saved.bind
def single_image_crawling(sender, **kwargs):
    ready = kwargs.get('ready', False)
    if not ready:
        return

    logger.info('single image crawling listens: {0} -> {1}'.format(sender, kwargs.items()))
    key = kwargs.get('key')
    doctype = kwargs.get('obj_type') or ''
    site, method, dummy = sender.split('.')

    if site and key and doctype.capitalize() in ('Event', 'Product'):
        try:
            process_image_pool.spawn(crawl_images, site, doctype, key)
        except Exception as e:
            logger.error('single image crawling error: {0} -> {1}'.format(sender, traceback.format_exc()))
    else:
        logger.error('single image crawling failed: {0}'.format(sender))


@ready_for_batch.bind
def batch_image_crawling(sender, **kwargs):
    logger.info('batch image crawling listens: {0} -> {1}'.format(sender, kwargs.items()))
    site = kwargs.get('site')
    doctype = kwargs.get('doctype') or ''

    if site and doctype.capitalize() in ('Event', 'Product'):
        if not hasattr(batch_image_crawling, 'run_flag'):
            setattr(batch_image_crawling, 'run_flag', {})

        key = '{0}.{1}'.format(site, doctype.capitalize())
        try:
            if key not in batch_image_crawling.run_flag or batch_image_crawling.run_flag[key] == False:
                batch_image_crawling.run_flag[key] = True
                scan_images(site, doctype, 10)
        except Exception as e:
            logger.error('batch image crawling error: {0} -> {1}'.format(sender, traceback.format_exc()))
        finally:
            batch_image_crawling.run_flag[key] = False
    else:
        logger.error('batch image crawling failed: {0}'.format(sender))


@ready_for_batch.bind
def batch_text_extract(sender, **kwargs):
    from datetime import datetime
    utcnow = datetime.utcnow()
    logger.info('batch text extract listens: {0} -> {1}'.format(sender, kwargs.items()))
    site, method, dummy = sender.split('.')
    doctype = kwargs.get('doctype') or ''

    if doctype.capitalize() == 'Event':
        # if there's an upcoming event in a site, try recognize the departments
        m = get_site_module(site)
        if hasattr(m, 'Event'):
            for event in m.Event.objects(events_begin__gt=utcnow, favbuy_dept=[]):
                try:
                    event.favbuy_dept = guess_event_dept(site, event)
                    event.save()
                except:
                    import traceback
                    traceback.print_exc()
                    pass
    elif doctype.capitalize() != 'Product':
        return
    
    if method.startswith('update'):
        ready_for_publish.send(None, **{'site': site})
        return

    if site in deal_crawlers:
        clean_product(site)
        ready_for_publish.send(None, **{'site': site})
        return

    if not hasattr(batch_text_extract, 'run_flag'):
        setattr(batch_text_extract, 'run_flag', {})

    try:
        if site in batch_text_extract.run_flag and batch_text_extract.run_flag[site] == True:
            logger.error('batch text extract failed: {0}'.format(sender))
            return
        elif site not in batch_text_extract.run_flag or batch_text_extract.run_flag[site] == False:
            batch_text_extract.run_flag[site] = True

        propagate(site, 15)
        logger.info('batch text extracted: {0}'.format(sender))
    except Exception as e:
        logger.error('batch text extract error: {0} -> {1}'.format(sender, traceback.format_exc()))
    finally:
        batch_text_extract.run_flag[site] = False
        ready_for_publish.send(None, **{'site': site})


if __name__ == '__main__':
    batch_text_extract('myhabit.update_listing.haha', doctype='Event')
