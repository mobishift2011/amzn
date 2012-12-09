#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from gevent import monkey; monkey.patch_all()
import gevent
from functools import partial

from helpers.rpc import get_rpcs
from settings import CRAWLER_PEERS, CRAWLER_PORT
from crawlers.common.routine import new, new_thrice, update, new_category, new_listing, new_product, update_category, update_listing, update_product
from backends.monitor.throttletask import task_already_running, task_completed

from crawlers.common.stash import get_ordinary_crawlers
from backends.monitor.organizetask import smethod_time

def execute(site, method):
    """ execute CrawlerServer function
    """
    if not task_already_running(site, method):
        gevent.spawn(globals()[method], site, get_rpcs(CRAWLER_PEERS, CRAWLER_PORT), concurrency=10) \
                .rawlink(partial(task_completed, site=site, method=method))


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


def auto_schedule():
    """.. :py:method::
        According to the order of demand, execute 'new' method first, 'update' maybe blocked for some turns.
        This way looks like 'new' have higher priority than 'update'.

        If 'new' or 'update' already running, all the expire task will try to execute, but failed,
        then removed from the smethod_time. This can avoid too long set() in smethod_time.
    """
    _utcnow = datetine.utcnow()

    for k, v in smethod_time.iteritems():
        site, method = k.split('.')
        if method == 'new':
            for new_time in sorted(v):
                if new_time <= _utcnow:
                    execute(site, 'new_thrice')
                    smethod_time[k].remove(new_time)
                else: break

    for k, v in smethod_time.iteritems():
        site, method = k.split('.')
        if method == 'update':
            for update_time in sorted(v):
                if update_time <= _utcnow:
                    if not task_already_running(site, 'new'):
                        execute(site, method)
                        smethod_time[k].remove(update_time)
                else: break

avoid_cold_start()
