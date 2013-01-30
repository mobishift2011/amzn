#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    spawn one listener to listen crawlers' signal -- pre_general_update, post_general_update
"""
from gevent import monkey; monkey.patch_all()
import gevent
import time
import collections
import traceback
from datetime import datetime, timedelta
from gevent.coros import Semaphore

from helpers.log import getlogger
from crawlers.common.events import *
from backends.monitor.models import Task, fail, Stat
from backends.monitor.setting import EXPIRE_MINUTES, DUMP_INTERVAL

logger = getlogger('monitor', '/tmp/monitor.log')
monitor_task = collections.defaultdict(dict)
task_lock = Semaphore(1)


@pre_general_update.bind('sync')
def stat_pre_general_update(sender, **kwargs):
    site, method, dummy = sender.split('.')
    with task_lock:
        if 'status' not in monitor_task[sender]:
            monitor_task[sender].update( {'site': site,
                                          'method': method,
                                          'status': Task.RUNNING,
                                          'started_at': datetime.utcnow()} )

@post_general_update.bind('sync')
def stat_post_general_update(sender, **kwargs):
    complete = kwargs.get('complete', False)
    reason = repr(kwargs.get('reason', 'undefined'))
    key = kwargs.get('key','')
    url = kwargs.get('url','')
    site, method, dummy = sender.split('.')
    utcnow = datetime.utcnow()

    with task_lock:
        if 'started_at' not in monitor_task[sender]: # 'post-' before 'pre-'
            monitor_task[sender].update({'started_at': utcnow})

        if not complete:
            if 'num_fails' in monitor_task[sender]:
                monitor_task[sender]['num_fails'] += 1
            else:
                monitor_task[sender]['num_fails'] = 1
            if 'fails' in monitor_task[sender]:
                monitor_task[sender]['fails'].append( (site, method, key, url, reason, utcnow) )
            else:
                monitor_task[sender]['fails'] = [ (site, method, key, url, reason, utcnow) ]

            monitor_task[sender].update({ 'site': site, 'method': method, 'status': Task.FAILED, 'ended_at': utcnow })
        else:
            monitor_task[sender].update({ 'site': site,
                                          'method': method,
                                          'status': Task.FINISHED,
                                          'ended_at': utcnow, })

@common_saved.bind('sync')
def stat_save(sender, **kwargs):
    key = kwargs.get('key','')
    url = kwargs.get('url','')
    is_new = kwargs.get('is_new', False)
    is_updated = kwargs.get('is_updated', False)
    site, method, dummy = sender.split('.')
    utcnow = datetime.utcnow()

    with task_lock:
        if 'num_new' in monitor_task[sender]:
            monitor_task[sender]['num_new'] += 1 if is_new else 0
        else:
            monitor_task[sender]['num_new'] = 1 if is_new else 0
        if 'num_update' in monitor_task[sender]:
            monitor_task[sender]['num_update'] += 1 if is_updated else 0
        else:
            monitor_task[sender]['num_update'] = 1 if is_updated else 0
        if 'num_finish' in monitor_task[sender]:
            monitor_task[sender]['num_finish'] += 1
        else:
            monitor_task[sender]['num_finish'] = 1

        monitor_task[sender].update({ 'site': site,
                                      'method': method,
                                      'updated_at': utcnow, })

    if is_new:
        doctype = kwargs.get('obj_type')
        interval = utcnow.replace(second=0, microsecond=0)
        Stat.objects(site=site, doctype=doctype.lower(), interval=interval).update(inc__crawl_num=1, upsert=True)


@common_failed.bind('sync')
def stat_failed(sender, **kwargs):
    key  = kwargs.get('key', '')
    url  = kwargs.get('url', '')
    reason = repr(kwargs.get('reason', 'undefined'))
    site, method, dummy = sender.split('.')
    utcnow = datetime.utcnow()

    with task_lock:
        if 'num_fails' in monitor_task[sender]:
            monitor_task[sender]['num_fails'] += 1
        else:
            monitor_task[sender]['num_fails'] = 1
        if 'fails' in monitor_task[sender]:
            monitor_task[sender]['fails'].append( (site, method, key, url, reason, utcnow) )
        else:
            monitor_task[sender]['fails'] = [ (site, method, key, url, reason, utcnow) ]

        monitor_task[sender].update({ 'site': site,
                                      'method': method,
                                      'updated_at': utcnow, })

def dump_monitor_task_to_db():
    """.. :py:method::
        dump monitor_task to mongodb,
        delete task which are finished.
        delete task which are expired.
    """
    utcnow = datetime.utcnow()
    pop_keys = []

    with task_lock:
        try:
            for sender, task in monitor_task.iteritems():

                # add finished task that can be delete from monitor_task in Memory
                if 'ended_at' in task: # if bind is not 'sync': and 'updated_at' in task and task['ended_at'] - task['updated_at'] > timedelta(minutes=5):
                    pop_keys.append(sender)
                elif 'updated_at' in task and utcnow - task['updated_at'] >= timedelta(minutes=EXPIRE_MINUTES):
                    task.update({'ended_at': utcnow})
                    pop_keys.append(sender)
                else:
                    pass

                # dump Memory to mongodb
                Task.objects(ctx=sender).update_one(set__site=task['site'],
                                                    set__method=task['method'],
                                                    set__status=task['status'] if 'status' in task else None,
                                                    set__started_at=task['started_at'] if 'started_at' in task else utcnow,
                                                    set__updated_at=task['updated_at'] if 'updated_at' in task else utcnow,
                                                    set__ended_at=task['ended_at'] if 'ended_at' in task else None,
                                                    set__num_finish=task['num_finish'] if 'num_finish' in task else 0,
                                                    set__num_update=task['num_update'] if 'num_update' in task else 0,
                                                    set__num_new=task['num_new'] if 'num_new' in task else 0,
                                                    set__num_fails=task['num_fails'] if 'num_fails' in task else 0,
                                                    set__fails=[fail(*i) for i in task['fails']] if 'fails' in task else [],
                                                    upsert=True)

            # delete finished task in monitor_task
            for key in pop_keys: monitor_task.pop(key)
        except Exception as e:
            logger.exception(e.message)
        

def buffer_task_dump_to_db_loop():
    while True:
        try:
            logger.info(monitor_task)
            time.sleep(60 * DUMP_INTERVAL)
            dump_monitor_task_to_db()
        except Exception as e:
            logger.exception(e.message)

# from logstat import * can execute this co-routine
gevent.spawn(buffer_task_dump_to_db_loop)


if __name__ == '__main__':
    print 'logstat'
