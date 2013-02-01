#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import gevent

from crawlers.common.events import common_saved
from powers.events import *
from powers.routine import crawl_images, scan_images, text_extract, debug_logger, run_fd
from settings import POWER_PEERS, TEXT_PEERS

from helpers.rpc import get_rpcs
from helpers.log import getlogger
logger = getlogger("powersignals", '/tmp/powersignals.log')

import traceback
import gevent.pool
process_image_pool = gevent.pool.Pool(500)

@common_saved.bind
def single_image_crawling(sender, **kwargs):
    ready = kwargs.get('ready', False)
    if not ready:
        return

    logger.info('single image crawling listens: {0} -> {1}'.format(sender, kwargs.items()))
    key = kwargs.get('key') or ''
    doctype = kwargs.get('obj_type') or ''
    site, method, dummy = sender.split('.')

    if site and key and doctype.capitalize() in ('Event', 'Product'):
        debug_logger.info('Single image begin[{0}], fd number: {1}'.format(sender, run_fd()))
        try:
            process_image_pool.spawn(crawl_images, site, doctype, key)
        except Exception as e:
            debug_logger.error('Error single image: {0}. {1}'.format(e, traceback.format_exc()))
        debug_logger.info('Single image end[{0}], fd number: {1}'.format(sender, run_fd()))
    else:
        logger.error('{0} failed to single image crawling: {1} {2} {3}'.format(sender, site, doctype, key))


@ready_for_batch.bind
def batch_image_crawling(sender, **kwargs):
    logger.info('batch image crawling listens: {0} -> {1}'.format(sender, kwargs.items()))
    site = kwargs.get('site')
    doctype = kwargs.get('doctype')

    if site and doctype:
        debug_logger.info('Batch image begin[{0}], fd number: {1}'.format(sender, run_fd()))
        try:
            scan_images(site, doctype, 10)
        except Exception as e:
            debug_logger.error('Error batch image: {0}. {1}'.format(e, traceback.format_exc()))
        debug_logger.info('Batch image end[{0}], fd number: {1}'.format(sender, run_fd()))
    else:
        logger.error('{0} failed to batch image crawling: {1} {2}'.format(sender, site, doctype))


@ready_for_batch.bind
def batch_text_extract(sender, **kwargs):
    site, method, dummy = sender.split('.')
    if method.startswith('update'):
        ready_for_publish.send(None, **{'site': site})
        return

    doctype = kwargs.get('doctype') or ''
    if doctype.capitalize() != 'Product':
        return

    if not hasattr(batch_text_extract, 'run_flag'):
        setattr(batch_text_extract, 'run_flag', {})

    try:
        if site in batch_text_extract.run_flag and batch_text_extract.run_flag[site] == True:
            return
        elif site not in batch_text_extract.run_flag or batch_text_extract.run_flag[site] == False:
            batch_text_extract.run_flag[site] = True

        text_extract(site, 15)
        ready_for_publish.send(None, **{'site': site})
    except Exception as e:
        debug_logger.error('Error text: {0}. {1}'.format(e, traceback.format_exc()))
    finally:
        batch_text_extract.run_flag[site] = False


#@pre_image_crawl.bind
def stat_pre_general_update(sender, **kwargs):
    pass


#@post_image_crawl.bind
def stat_post_general_update(sender, **kwargs):
    pass


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == '-si':
            site = sys.argv[2]
            doctype = sys.argv[3]
            key = sys.argv[4]
            sender = '{0}.{1}.{2}'.format(site, doctype, key)
            common_saved.send(sender=sender, doctype=doctype, key=key)

        elif sys.argv[1] == '-bi':
            site = sys.argv[2]
            doctype = sys.argv[3]
            ready_for_batch.send(sender=None, doctype=doctype, site=site)

        elif sys.argv[1] == '-be':
            site = sys.argv[2]
            doctype = sys.argv[3]
            ready_for_batch.send(sender=None, doctype=doctype, site=site)
