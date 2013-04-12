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
from crawlers.common.stash import luxury_crawlers

luxury_crawler = list(luxury_crawlers)
if 'zulily' in luxury_crawler: luxury_crawler.remove('zulily')

smethod_time = collections.defaultdict(set)
deals_method_time = collections.defaultdict(set)
conn = pymongo.Connection(host=MONGODB_HOST)

def detect_upcoming_new_schedule():
    """.. :py:method::
        upcoming new event, schedule
    """
    while True:
        dbs = conn.database_names()
        for crawler_name in luxury_crawler:
            if crawler_name in dbs:
                collections = conn[crawler_name].collection_names()
                if 'event' in collections:
                    upcoming_events = conn[crawler_name].event.find({'events_begin': {'$gte': datetime.utcnow()}}, fields=['events_begin'])
                    events_begin = set( [e['events_begin'] for e in upcoming_events] )
                    for begin in events_begin:
                        smethod_time['{0}.new_thrice'.format(crawler_name)].add(begin)

        add_noupcoming_onsale()
        gevent.sleep(UPCOMING_EVENTS_DETECT_INTERVAL * 60)

def add_noupcoming_onsale():
    """.. :py:method::
        nomorerack has no upcoming events, utc17:00 lunch
        ideeli has no upcoming events, utc15:00, 16:00, 21:00 lunch
    """
    _utcnow = datetime.utcnow()
    if _utcnow.hour < 17: # nomorerack
        smethod_time['nomorerack.new_thrice'].add(datetime(_utcnow.year, _utcnow.month, _utcnow.day, 17))
    if _utcnow.hour < 15: # ideeli
        smethod_time['ideeli.new_thrice'].add(datetime(_utcnow.year, _utcnow.month, _utcnow.day, 15))
        smethod_time['ideeli.new_thrice'].add(datetime(_utcnow.year, _utcnow.month, _utcnow.day, 16))
        smethod_time['ideeli.new_thrice'].add(datetime(_utcnow.year, _utcnow.month, _utcnow.day, 21))
    if _utcnow.hour < 16: # belleandclive
        smethod_time['belleandclive.new_thrice'].add(datetime(_utcnow.year, _utcnow.month, _utcnow.day, 16))
    else:
        smethod_time['belleandclive.new_thrice'].add(datetime(_utcnow.year, _utcnow.month, _utcnow.day) + timedelta(days=1))


def arrange_new_schedule():
    """.. :py:method::
        If the crawler have no upcoming events(like beyondtherack) or new events coming without upcoming notified.
        We need execute all the new process every several minutes!

        This is the 'in case' schedule
    """
    while True:
        crawlers = luxury_crawler
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
        crawlers = luxury_crawler
        one_interval = timedelta(seconds =  UPDATE_ALL_SITES_INTERVAL * 1.0 / len(crawlers) * 60)
        _utcnow = datetime.utcnow()
        for crawler in crawlers:
            smethod_time['{0}.update'.format(crawler)].add(_utcnow)
            _utcnow += one_interval

        gevent.sleep(UPDATE_ALL_SITES_INTERVAL * 60)


def arrange_deals_schedule():
    while True:
        crawlers = luxury_crawler
        one_interval = timedelta(seconds =  DEALS_SITES_INTERVAL * 1.0 / len(crawlers) * 60)
        _utcnow = datetime.utcnow()

        for crawler in crawlers:
            deals_method_time['{0}.new'.format(crawler)].add(_utcnow)
            _utcnow += one_interval
            deals_method_time['{0}.update'.format(crawler)].add(_utcnow - one_interval//2)
            
        gevent.sleep(DEALS_SITES_INTERVAL * 60)
