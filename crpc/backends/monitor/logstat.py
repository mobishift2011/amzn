#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crawlers.common.events import *
from helpers.log import getlogger
from models import Task, Fail
from datetime import datetime, timedelta

logger = getlogger("crawlerlog")

def fail(site, method, key=None, message="undefined"):
    f = Fail(site=site, method=method, key=key, message=message)
    f.save()
    return f

def get_or_create_task(site, method):
    t = Task.objects(status=Task.RUNNING, site=site, method=method).first()
    if not t:
        t = Task.objects(status=Task.READY, site=site, method=method).first()
        if not t:
            t = Task(status=Task.READY, site=site, method=method)
        else:
            t.status = Task.RUNNING
            t.started_at = datetime.utcnow()
    return t

@pre_general_update.bind
def stat_pre_general_update(sender, **kwargs):
    site = kwargs.get('site')
    method = kwargs.get('method')
    assert site != None and method != None, u"argument error"

    t = get_or_create_task(site, method)
    t.save()

@post_general_update.bind
def stat_post_general_update(sender, **kwargs):
    site = kwargs.get('site')
    method = kwargs.get('method')
    complete = kwargs.get('complete', False)
    reason = kwargs.get('reason', 'undefined')
    assert site != None and method != None, u"argument error"

    t = get_or_create_task(site, method)
    t.status = Task.FINISHED if complete else Task.FAILED
    if not complete:
        t.fails.append( fail(site, methdo, None, reason) )
    t.save()

@category_saved.bind
def stat_category_save(sender, **kwargs):
    logger.debug('SECOND{0}'.format(kwargs.items()))
    site = kwargs.get('site')
    method = kwargs.get('method')
    key = kwargs.get('key')
    assert site is not None and method is not None and key is not None, u"argument error"

    is_new = kwargs.get('is_new', False)
    is_updated = kwargs.get('is_updated', False)
    t = get_or_create_task(site, method)

    if is_new:
        t.num_new += 1
    elif is_updated:
        t.num_update += 1
    else:
        t.num_finish += 1
    
    t.save()    

@product_saved.bind
def stat_product_save(sender, **kwargs):
    on_category_save(sender, **kwargs)

@category_failed.bind
def stat_category_failed(sender, **kwargs):
    logger.error('SECOND{0}'.format(kwargs.items()))
    site = kwargs.get('site')
    url  = kwargs.get('url')
    reason = kwargs.get('reason')
    assert site is not None and url is not None and reason is not None, u"argument error"

    t = Task.objects(status=Task.RUNNING, site=site).first()
    if t:
        t.update_one(push__fails=fail(site, None, url, reason))

@product_failed.bind
def stat_product_failed(sender, **kwargs):
    on_category_failed(sender, **kwargs)
