#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from gevent import monkey; monkey.patch_all()
import gevent
from functools import partial
from datetime import datetime

from helpers.rpc import get_rpcs
from settings import CRAWLER_PEERS, CRAWLER_PORT
from crawlers.common.routine import new, new_thrice, update, new_category, new_listing, new_product, update_category, update_listing, update_product
from backends.monitor.throttletask import can_task_run, task_completed, is_task_already_running

from crawlers.common.stash import get_ordinary_crawlers
from backends.monitor.organizetask import smethod_time
from backends.monitor.setting import EXPIRE_MINUTES

def execute(site, method):
    """ execute CrawlerServer function

    :rtype: True, successfully to execute this method;
            False, task already running, this method is not executed
    """
    if can_task_run(site, method):
        gevent.spawn(globals()[method], site, get_rpcs(CRAWLER_PEERS, CRAWLER_PORT), concurrency=10) \
                .rawlink(partial(task_completed, site=site, method=method))
        return True
    else:
        return False

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
        gevent.sleep(EXPIRE_MINUTES * 60)

def auto_schedule():
    """.. :py:method::
        According to the order of demand, execute 'new' method first, 'update' maybe blocked for some turns.
        This way looks like 'new' have higher priority than 'update'.

        If 'new' or 'update' already running, all the expire task will try to execute, but failed,
        then removed from the smethod_time. This can avoid too long set() in smethod_time.
    """
    _utcnow = datetime.utcnow()
    # open('/tmp/sche.debug', 'a').write('[{0}]: {1} \n'.format(_utcnow, smethod_time))

    for k, v in smethod_time.iteritems():
        site, method = k.split('.')
        if method == 'new':
            for new_time in sorted(v):
                if new_time <= _utcnow:
                    if execute(site, 'new_thrice'):
                        smethod_time[k].remove(new_time)
                else: break

    for k, v in smethod_time.iteritems():
        site, method = k.split('.')
        if method == 'update':
            for update_time in sorted(v):
                if update_time <= _utcnow:
                    if not is_task_already_running(site, 'new'):
                        if execute(site, method):
                            smethod_time[k].remove(update_time)
                else: break

