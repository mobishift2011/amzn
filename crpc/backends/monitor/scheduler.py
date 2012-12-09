#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Scheduler: runs crawlers in background
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from gevent import monkey; monkey.patch_all()
import gevent
import zerorpc
from functools import partial
from datetime import datetime, timedelta

from crawlers.common.routine import new, new_thrice, update, new_category, new_listing, new_product, update_category, update_listing, update_product
from helpers.rpc import get_rpcs
from settings import CRAWLER_PEERS, CRAWLER_PORT
from backends.monitor.models import Schedule, Task
from backends.monitor.throttletask import task_already_running, task_completed, task_broke_completed
from backends.monitor.autoschedule import schedule_auto_new_task, schedule_auto_update_task, auto_schedule, avoid_cold_start
from .setting import EXPIRE_MINUTES


def execute(site, method):
    """ execute CrawlerServer function
    """
    if not task_already_running(site, method):
        gevent.spawn(globals()[method], site, get_rpcs(CRAWLER_PEERS, CRAWLER_PORT), concurrency=10) \
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
        gevent.spawn(avoid_cold_start)
        gevent.spawn(schedule_auto_new_task)
        gevent.spawn(schedule_auto_update_task)

        while True:
            try:
                auto_schedule()

                # keep the old crond system
                for s in self.get_schedules():
                    if s.timematch():
                        execute(s.site, s.method)

                # assume this for loop can be finished in less than one minute
                gevent.sleep(60 - datetime.utcnow().second)
                gevent.spawn(delete_expire_task)
            except Exception as e:
                with open('/tmp/schedule.log', 'a') as fd:
                    fd.write(str(e) + '\n\n\n')

