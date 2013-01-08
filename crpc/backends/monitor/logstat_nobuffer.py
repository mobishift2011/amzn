#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    spawn one listener to listen crawlers' signal -- pre_general_update, post_general_update
"""
from crawlers.common.events import *

from helpers.log import getlogger
import traceback

from backends.monitor.models import Task, Fail, fail
from datetime import datetime, timedelta

logger = getlogger("crawlerlog")

def get_or_create_task(ctx):
    """
        Caution: This function should not update the status,
        or else, post_general_update will be override by common_saved.
    """
    t = Task.objects(ctx=ctx).first()
    if not t:
        t = Task(ctx=ctx)
        t.site, t.method, dummy = ctx.split('.')
        t.started_at = datetime.utcnow()
        t.save()
#    else:
#        t.update(set__status=Task.RUNNING, set__updated_at=datetime.utcnow())
    return t

@pre_general_update.bind('sync')
def stat_pre_general_update(sender, **kwargs):
    site, method, dummy = sender.split('.')
    try:
        Task.objects(ctx=sender, status__ne=Task.FINISHED).update_one(set__site=site,
                                            set__method=method,
                                            set__status=Task.RUNNING,
                                            set__started_at=datetime.utcnow(),
                                            upsert=True)
    except Exception as e:
        logger.exception(e.message)
        fail(site, method, kwargs.get('key',''), kwargs.get('url',''), traceback.format_exc())
        

@post_general_update.bind('sync')
def stat_post_general_update(sender, **kwargs):
    complete = kwargs.get('complete', False)
    reason = repr(kwargs.get('reason', 'undefined'))
    key = kwargs.get('key','')
    url = kwargs.get('url','')
    site, method, dummy = sender.split('.')

    try:
        utcnow = datetime.utcnow()
        if not complete:
            Task.objects(ctx=sender).update_one(set__site=site,
                                                set__method=method,
                                                set__status=Task.FAILED,
                                                push__fails=fail(site, method, key, url, reason),
                                                inc__num_fails=1,
                                                set__updated_at=utcnow,
                                                upsert=True)
        else:
            Task.objects(ctx=sender).update_one(set__site=site,
                                                set__method=method,
                                                set__status=Task.FINISHED,
                                                set__updated_at=utcnow,
                                                upsert=True)
        Task.objects(ctx=sender, started_at__exists=False).update_one(set__started_at=utcnow)
    except Exception as e:
        logger.exception(e.message)
        fail(site, method, key, url, traceback.format_exc())


@common_saved.bind('sync')
def stat_save(sender, **kwargs):
    logger.debug('{0} -> {1}'.format(sender,kwargs.items()))
    key = kwargs.get('key','')
    url = kwargs.get('url','')
    is_new = kwargs.get('is_new', False)
    is_updated = kwargs.get('is_updated', False)

    site, method, dummy = sender.split('.')
    num_new = 1 if is_new else 0
    num_update = 1 if is_updated else 0
    num_finish = 1

    try:
        Task.objects(ctx=sender).update_one(set__site=site,
                                            set__method=method,
                                            inc__num_new=num_new,
                                            inc__num_update=num_update,
                                            inc__num_finish=num_finish,
                                            set__updated_at=datetime.utcnow(),
                                            upsert=True)
    except Exception as e:
        logger.exception(e.message)
        Task.objects(ctx=sender).update_one(set__site=site,
                                            set__method=method,
                                            inc__num_fails=1,
                                            push__fails=fail(site, method, key, url, traceback.format_exc()),
                                            set__updated_at=datetime.utcnow(),
                                            upsert=True)


@common_failed.bind('sync')
def stat_failed(sender, **kwargs):
    logger.error('{0} -> {1}'.format(sender,kwargs.items()))
    key  = kwargs.get('key', '')
    url  = kwargs.get('url', '')
    reason = repr(kwargs.get('reason', 'undefined'))
    site, method, dummy = sender.split('.')

    try:
        Task.objects(ctx=sender).update_one(set__site=site,
                                            set__method=method,
                                            push__fails=fail(site, method, key, url, reason),
                                            inc__num_fails=1,
                                            set__updated_at=datetime.utcnow(),
                                            upsert=True)
    except Exception as e:
        logger.exception(e.message)
        Task.objects(ctx=sender).update_one(set__site=site,
                                            set__method=method,
                                            push__fails=fail(site, method, key, url, traceback.format_exc()),
                                            inc__num_fails=1,
                                            set__updated_at=datetime.utcnow(),
                                            upsert=True)

if __name__ == '__main__':
    print 'logstat_nobuffer'
