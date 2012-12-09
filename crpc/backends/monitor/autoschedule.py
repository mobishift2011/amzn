#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from gevent import monkey; monkey.patch_all()
import random
import pymongo
import collections
from datetime import datetime, timedelta

from settings import MONGODB_HOST
from .setting import UPCOMING_EVENTS_DETECT_INTERVAL, UPDATE_ALL_SITES_INTERVAL
from crawlers.common.stash import get_ordinary_crawlers
from backends.monitor.scheduler import execute
from backends.monitor.throttletask import task_already_running


smethod_time = collections.defaultdict(set)
conn = pymongo.Connection(host=MONGODB_HOST)

def detect_upcoming_new_schedule():
    """.. :py:method::
        upcoming to new event, schedule
    """
    dbs = conn.database_names()
    for crawler_name in get_ordinary_crawlers():
        if crawler_name in dbs:
            collections = conn.crawler_name.collection_names()
            if 'event' in collections:
                upcoming_events = conn.crawler_name.event.find({'events_begin': {'$gte': datetime.utcnow()}}, fields=['events_begin'])
                events_begin = set( [e['events_begin'] for e in upcoming_events] )
                for begin in events_begin:
                    smethod_time['{0}.new'.format(crawler_name)].add(begin)

def arrange_update_schedule():
    """.. :py:method::
        update schedule
    """
    crawlers = get_ordinary_crawlers()
    random.shuffle(crawlers)
    one_interval = timedelta(seconds =  UPDATE_ALL_SITES_INTERVAL * 1.0 / len(crawlers) * 60)
    _utcnow = datetime.utcnow()
    for crawler in crawlers:
        smethod_time['{0}.update'.format(crawler)].add(_utcnow)
        _utcnow += one_interval

def schedule_auto_new_task():
    """.. :py:method::
    """
    while True:
        detect_upcoming_new_schedule()
        gevent.sleep(UPCOMING_EVENTS_DETECT_INTERVAL * 60)

def schedule_auto_update_task():
    """.. :py:method::
    """
    while True:
        arrange_update_schedule()
        gevent.sleep(UPDATE_ALL_SITES_INTERVAL * 60)

def autotask():
    """.. :py:method::
        According to the order of demand, execute 'new' method first, 'update' maybe blocked for some turns.
        This way looks like 'new' have higher priority than 'update'.

        If 'new' or 'update' already running, all the expire task will try to execute, but failed,
        then removed from the smethod_time. This can avoid too long set() in smethod_time.
    """
    _utcnow = datetine.utcnow()

    #To find a sort way: if the list is already sorted, it do nearly nothing.
    for k, v in smethod_time.iteritems():
        site, method = k.split('.')
        if method == 'new':
            smethod_time[k] = set(sorted(v))
            for new_time in smethod_time[k]:
                if new_time <= _utcnow:
                    execute(site, 'new_thrice')
                    smethod_time[k].remove(new_time)
                else: break

    for k, v in smethod_time.iteritems():
        site, method = k.split('.')
        if method == 'update':
            smethod_time[k] = set(sorted(smethod_time[k]))
            for update_time in smethod_time[k]:
                if update_time <= _utcnow:
                    if not task_already_running(site, 'new'):
                        execute(site, method)
                        smethod_time[k].remove(update_time)
                else: break

def avoid_cold_start():
    """.. :py:method::
        1. If all the system is no ever running, we need run them when the system started.
        2. If this process is broke, nothing in the memory kept, maybe the new upcoming all lost,
            we don't know whether the site have new events or products on sale.
        Need to crawl all the system first.
    """
    crawlers = get_ordinary_crawlers()
    for crawler_name in crawlers:
        execute(crawler_name, 'new')
