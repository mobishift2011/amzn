#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from gevent import monkey; monkey.patch_all()
import gevent
import pymongo
import collections
from datetime import datetime, timedelta

from settings import MONGODB_HOST
from backends.monitor.setting import UPCOMING_EVENTS_DETECT_INTERVAL, UPDATE_ALL_SITES_INTERVAL, NEW_ALL_SITES_INTERVAL
from crawlers.common.stash import get_ordinary_crawlers

smethod_time = collections.defaultdict(set)
conn = pymongo.Connection(host=MONGODB_HOST)

def detect_upcoming_new_schedule():
    """.. :py:method::
        upcoming new event, schedule
    """
    while True:
        dbs = conn.database_names()
        for crawler_name in get_ordinary_crawlers():
            if crawler_name in dbs:
                collections = conn[crawler_name].collection_names()
                if 'event' in collections:
                    upcoming_events = conn[crawler_name].event.find({'events_begin': {'$gte': datetime.utcnow()}}, fields=['events_begin'])
                    events_begin = set( [e['events_begin'] for e in upcoming_events] )
                    for begin in events_begin:
                        smethod_time['{0}.new_thrice'.format(crawler_name)].add(begin)

        gevent.sleep(UPCOMING_EVENTS_DETECT_INTERVAL * 60)

def arrange_new_schedule():
    """.. :py:method::
        If the crawler have no upcoming events(like beyondtherack) or new events coming without upcoming notified.
        We need execute all the new process every several minutes!

        This is the 'in case' schedule
    """
    while True:
        crawlers = get_ordinary_crawlers()
        one_interval = timedelta(seconds =  NEW_ALL_SITES_INTERVAL * 1.0 / len(crawlers) * 60)
        _utcnow = datetime.utcnow()
        for crawler in crawlers:
            smethod_time['{0}.new'.format(crawler)].add(_utcnow)
            _utcnow += one_interval

        gevent.sleep(NEW_ALL_SITES_INTERVAL * 60)


def arrange_update_schedule():
    """.. :py:method::
        update schedule, update sequence is always the same
    """
    while True:
        crawlers = get_ordinary_crawlers()
        one_interval = timedelta(seconds =  UPDATE_ALL_SITES_INTERVAL * 1.0 / len(crawlers) * 60)
        _utcnow = datetime.utcnow()
        for crawler in crawlers:
            smethod_time['{0}.update'.format(crawler)].add(_utcnow)
            _utcnow += one_interval

        gevent.sleep(UPDATE_ALL_SITES_INTERVAL * 60)

