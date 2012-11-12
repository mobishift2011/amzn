#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Scheduler: runs crawlers in background
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from gevent import monkey; monkey.patch_all()
import gevent

from backends.monitor.models import Schedule, Task
from crawlers.common.routine import update_category, update_listing, update_product, update_listing_update

import zerorpc
from datetime import datetime, timedelta
from settings import PEERS, RPC_PORT
from onlytask import avoid_two_same_task_running
from .setting import EXPIRE_MINUTES

def get_rpcs():
    rpcs = []
    for peer in PEERS:
        host = peer[peer.find('@')+1:]
        c = zerorpc.Client('tcp://{0}:{1}'.format(host, RPC_PORT), timeout=None)
        if c:
            rpcs.append(c)
    return rpcs


def execute(site, method):
    """ execute RPCServer function
    """
    avoid_two_same_task_running(site, method)
    gevent.spawn(globals()[method], site, get_rpcs(), 10)


def delete_expire_task(expire_minutes=EXPIRE_MINUTES):
    """ delete the expire RUNNING Task, expire_minutes is in settings
        TODO: expire_minutes be set on the web page

    :param expire_minutes: set the expire running task in hours
    """
    expire_datetime = datetime.utcnow() - timedelta(minutes=expire_minutes)
    for t in Task.objects(status=102, updated_at__lt=expire_datetime):
        t.status = 104
        t.save()


class Scheduler(object):
    """ make schedules easy """
    def get_schedules(self):
        return Schedule.objects(enabled=True) 

    def run(self):
        while True:
            for s in self.get_schedules():
                if s.timematch():
                    execute(s.site, s.method)
            gevent.sleep(60)
            gevent.spawn(delete_expire_task)
