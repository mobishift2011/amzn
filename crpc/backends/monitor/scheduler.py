#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Scheduler: runs crawlers in background
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from gevent import monkey; monkey.patch_all()
import gevent
import zerorpc
from datetime import datetime, timedelta

from backends.monitor.models import Schedule, Task
from backends.monitor.throttletask import task_broke_completed
from backends.monitor.autoschedule import execute
from backends.monitor.setting import EXPIRE_MINUTES


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
            for s in self.get_schedules():
                if s.timematch():
                    execute(s.site, s.method)

            # assume this for loop can be finished in less than one minute
            delete_expire_task()
            gevent.sleep(60 - datetime.utcnow().second)

if __name__ == '__main__':
    Scheduler().run()
