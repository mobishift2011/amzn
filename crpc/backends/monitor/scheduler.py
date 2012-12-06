#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Scheduler: runs crawlers in background
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from gevent import monkey; monkey.patch_all()
import gevent

from backends.monitor.models import Schedule, Task
from crawlers.common.routine import new, update, new_category, new_listing, new_product, update_category, update_listing, update_product #update_category, update_listing, update_product, update_listing_update

import zerorpc
from datetime import datetime, timedelta
from settings import CRAWLER_PEERS, CRAWLER_PORT
from throttletask import task_already_running, task_completed, task_broke_completed
from functools import partial
from .setting import EXPIRE_MINUTES

from helpers.rpc import get_rpcs

def execute(site, method):
    """ execute CrawlerServer function
    """
    if not task_already_running(site, method):
        gevent.spawn(globals()[method], site, get_rpcs(CRAWLER_PEERS, CRAWLER_PORT), 10) \
                .rawlink(partial(task_completed, site=site, method=method))


def delete_expire_task(expire_minutes=EXPIRE_MINUTES):
    """ delete the expire RUNNING Task, expire_minutes is in settings
        TODO: expire_minutes be set on the web page

    :param expire_minutes: set the expire running task in hours
    """
    expire_datetime = datetime.utcnow() - timedelta(minutes=expire_minutes)
    for t in Task.objects(status=Task.RUNNING, updated_at__lt=expire_datetime):
        t.status = Task.FAILED
        t.save()
        task_broke_completed(t.site, t.method)


class Scheduler(object):
    """ make schedules easy """
    def get_schedules(self):
        return Schedule.objects(enabled=True) 

    def run(self):
        while True:
            try:
                for s in self.get_schedules():
                    if s.timematch():
                        execute(s.site, s.method)
                gevent.sleep(60)
                gevent.spawn(delete_expire_task)
            except Exception as e:
                with open('/tmp/schedule.log', 'a') as fd:
                    fd.write(str(e) + '\n\n\n')

