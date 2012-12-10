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
from backends.monitor.autoschedule import execute, avoid_cold_start, auto_schedule
from backends.monitor.organizetask import organize_new_task, organize_update_task
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
        # gevent.spawn(avoid_cold_start)
        # gevent.spawn(organize_new_task)
        # gevent.spawn(organize_update_task)
        # TODO I have already monkey.patch_all(), why need a sleep
        gevent.sleep(60)

        while True:
            try:
                # auto_schedule()

                # keep the old crond system
                for s in self.get_schedules():
                    if s.timematch():
                        execute(s.site, s.method)

                # assume this for loop can be finished in less than one minute
                print datetime.utcnow().second
                gevent.sleep(60 - datetime.utcnow().second)
                gevent.spawn(delete_expire_task)
            except Exception as e:
                with open('/tmp/schedule.log', 'a') as fd:
                    fd.write(str(e) + '\n\n\n')

if __name__ == '__main__':
    Scheduler().run()
