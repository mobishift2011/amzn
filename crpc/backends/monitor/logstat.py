#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crawlers.common.events import *

from helpers.log import getlogger
import traceback

from backends.monitor.models import Task, Fail, fail
from datetime import datetime, timedelta
from gevent.event import Event

logger = getlogger("crawlerlog")

def get_or_create_task(ctx):
    t = Task.objects(ctx=ctx).first()
    if not t:
        t = Task(ctx=ctx)
        t.site, t.method, dummy = ctx.split('.')
        t.started_at = datetime.utcnow()
        t.save()
    else:
        t.update(set__status=Task.RUNNING)
    return t

@pre_general_update.bind
def stat_pre_general_update(sender, **kwargs):
    try:
        site, method, dummy = sender.split('.')
        t = get_or_create_task(sender)
        t.save()
    except Exception as e:
        logger.exception(e.message)
        fail(site, method, kwargs.get('key',''), kwargs.get('url',''), traceback.format_exc())
        

@post_general_update.bind
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

@common_saved.bind
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
    
        t.update(set__num_new=t.num_new, set__num_update=t.num_update, set__num_finish=t.num_finish, updated_at=datetime.utcnow())
    except Exception as e:
        logger.exception(e.message)
        fail(site, method, key, url, traceback.format_exc())

@common_failed.bind
def stat_failed(sender, **kwargs):
    logger.error('{0} -> {1}'.format(sender,kwargs.items()))
    key  = kwargs.get('key', '')
    url  = kwargs.get('url', '')
    reason = kwargs.get('reason', 'undefined')

    try:
        site, method, dummy = sender.split('.')
        t = get_or_create_task(sender)
        t.update(push__fails=fail(site, method, key, url, reason), inc__num_fails=1, updated_at=datetime.utcnow())
    except Exception as e:
        logger.exception(e.message)
        fail(site, method, key, url, traceback.format_exc())

if __name__ == '__main__':
    print task_all_tasks()
