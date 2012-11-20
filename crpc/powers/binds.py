# -*- coding: utf-8 -*-
from powers.events import *
from powers.routine import get_rpcs, update_event_images, update_product_images

from gevent import monkey; monkey.patch_all()
import gevent

from helpers.log import getlogger
logger = getlogger("crawlerImageLog")

@run_image_crawl.bind
def image_crawl(sender, **kwargs):
    site = kwargs.get('site')
    method = kwargs.get('method')
    
    print 'get rpc resource to %s.%s' % (site, method)
    if site and method:
        gevent.spawn(globals()[method], site, get_rpcs(), 10) #.rawlink(partial(task_completed, site=site, method=method))

@pre_image_crawl.bind
def stat_pre_general_update(sender, **kwargs):
    try:
        site, method, dummy = sender.split('.')
        t = get_or_create_task(sender)
        t.save()
    except Exception as e:
        logger.exception(e.message)
        fail(site, method, kwargs.get('key',''), kwargs.get('url',''), traceback.format_exc())

@post_image_crawl.bind
def stat_post_general_update(sender, **kwargs):
    complete = kwargs.get('complete', False)
    reason = repr(kwargs.get('reason', 'undefined'))
    key = kwargs.get('key','')
    url = kwargs.get('url','')
    try:
        site, method, dummy = sender.split('.')
        t = get_or_create_task(sender)
        t.status = Task.FINISHED if complete else Task.FAILED
        if not complete:
            t.fails.append( fail(site, method, key, url, reason) )
        t.save()
    except Exception as e:
        logger.exception(e.message)
        fail(site, method, key, url, traceback.format_exc())

@image_crawled_failed.bind
def stat_failed(sender, **kwargs):
    logger.error('{0} -> {1}'.format(sender,kwargs.items()))
    key  = kwargs.get('key', '')
    url  = kwargs.get('url', '')
    reason = repr(kwargs.get('reason', 'undefined'))

    try:
        site, method, dummy = sender.split('.')
        t = get_or_create_task(sender)
        t.update(push__fails=fail(site, method, key, url, reason), inc__num_fails=1)
    except Exception as e:
        logger.exception(e.message)
        t.update(push__fails=fail(site, method, key, url, traceback.format_exc()), inc__num_fails=1)

@image_crawled.bind
def stat_save(sender, **kwargs):
    logger.debug('{0} -> {1}'.format(sender,kwargs.items()))
    key = kwargs.get('key','')
    url = kwargs.get('url','')
    is_new = kwargs.get('is_new', False)
    is_updated = kwargs.get('is_updated', False)

    try:
        site, method, dummy = sender.split('.')
        t = get_or_create_task(sender)

        if is_new:
            t.num_new += 1
        if is_updated:
            t.num_update += 1
        t.num_finish += 1
    
        t.update(set__num_new=t.num_new, set__num_update=t.num_update, set__num_finish=t.num_finish)
    except Exception as e:
        logger.exception(e.message)
        t.update(push__fails=fail(site, method, key, url, traceback.format_exc()), inc__num_fails=1)