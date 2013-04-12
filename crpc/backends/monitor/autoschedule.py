#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import gevent

from datetime import datetime, timedelta
from crawlers.common.stash import luxury_crawlers

from backends.monitor.throttletask import can_task_run, task_completed, is_task_already_running
from backends.monitor.organizetask import detect_upcoming_new_schedule, arrange_new_schedule, arrange_update_schedule, smethod_time, arrange_deals_schedule, deals_method_time
from backends.monitor.setting import SCHEDULE_STATE
from backends.monitor.executor import execute
from backends.monitor.ghub import GHub

from helpers.log import getlogger


autoscheduler_logger = getlogger('autoscheduler', '/tmp/autoscheduler.log')

def avoid_cold_start():
    """.. :py:method::
        1. If all the system is no ever running, we need run them when the system started.
        2. If this process is broke, nothing in the memory kept, maybe the new upcoming all lost,
            we don't know whether the site have new events or products on sale.
        Need to crawl all the system first.
    
    Sets a list of Greenlet that it envokes    
    """
    j1 = gevent.spawn(detect_upcoming_new_schedule)
    j2 = gevent.spawn(arrange_new_schedule)
    j3 = gevent.spawn(arrange_update_schedule)
    j4 = gevent.spawn(arrange_deals_schedule)

    GHub().extend('acs', [j1, j2, j3, j4])
    # gevent need a 'block' to run spawn.Or we can say gevent will execute spawn until meet a 'block'
    gevent.sleep(1)

    crawlers = list(luxury_crawlers)
    if 'zulily' in crawlers:
        crawlers.remove('zulily')
    for crawler_name in crawlers:
        execute(crawler_name, 'new_thrice')

def auto_schedule():
    """.. :py:method::
        According to the order, execute 'new_thrice' method first, 'update' maybe blocked for some turns.
        This way looks like 'new_thrice' have higher priority than 'update'.

        If 'new' or 'update' already running, all the expire task will try to execute, but failed,
        then removed from the smethod_time. This can avoid too long set() in smethod_time.
    """
    _utcnow = datetime.utcnow()
    autoscheduler_logger.debug(smethod_time)
    autoscheduler_logger.debug(SCHEDULE_STATE)

    for k, v in smethod_time.iteritems():
        site, method = k.split('.')
        if method == 'new_thrice':
            for new_time in sorted(v):
                if new_time + timedelta(minutes=1) <= _utcnow: # new need to plus 1 minute
                    execute(site, method)
                    smethod_time[k].remove(new_time)
                else: break

    for k, v in smethod_time.iteritems():
        site, method = k.split('.')
        for run_time in sorted(v):
            if run_time <= _utcnow:
                if method == 'update':
                    if not is_task_already_running(site, 'new'):
                        execute(site, method)
                        smethod_time[k].remove(run_time)
                elif method == 'new':
                    execute(site, method)
                    smethod_time[k].remove(run_time)
            else: break



def auto_schedule_deals():
    autoscheduler_logger.debug(deals_method_time)
    _utcnow = datetime.utcnow()

    for k, v in deals_method_time.iteritems():
        site, method = k.split('.')
        for run_time in sorted(v):
            if run_time <= _utcnow:
                if method == 'new':
                    execute(site, method)
                    deals_method_time[k].remove(run_time)
                elif method == 'update':
                    if not is_task_already_running(site, 'new'):
                        execute(site, method)
                        deals_method_time[k].remove(run_time)
            else: break
            
