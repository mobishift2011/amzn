#!/usr/bin/env python
# -*- coding: utf-8 -*-
from crawlers.common.events import *

from helpers.log import getlogger
import traceback

from backends.monitor.models import Task, Fail
from datetime import datetime, timedelta
from gevent.event import Event

log_event =  Event()

logger = getlogger("crawlerlog")

def fail(site, method, key='', url='', message="undefined"):
    f = Fail(site=site, method=method, key=key, url=url, message=message)
    f.save()
    return f

def get_or_create_task(ctx):
    t = Task.objects(ctx=ctx).first()
    if not t:
        t = Task(ctx=ctx)
        t.site, t.method, dummy = ctx.split('.')
        t.started_at = datetime.utcnow()
    else:
        t.status = Task.RUNNING
    t.save()
    return t

def mark_all_failed():
    for t in Task.objects():
        if t.status == Task.RUNNING:
            t.update(set__status=Task.FAILED, push__fails=fail(t.site, t.method, '', '', 'Monitor Restart'))

def task_all_tasks():
    tasks = Task.objects().select_related()
    return {"tasks":[t.to_json() for t in tasks]}

def task_updates():
    tasks = Task.objects(updated_at__gt=datetime.utcnow()-timedelta(seconds=60)).select_related()
    return {"tasks":[t.to_json() for t in tasks]}

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
    reason = kwargs.get('reason', 'undefined')
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
    
        t.save() 
        log_event.set()
        log_event.clear()
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
        t.update(push__fails=fail(site, method, key, url, reason))

        log_event.set()
        log_event.clear()
    except Exception as e:
        logger.exception(e.message)
        fail(site, method, key, url, traceback.format_exc())

if __name__ == '__main__':
    print task_updates()
