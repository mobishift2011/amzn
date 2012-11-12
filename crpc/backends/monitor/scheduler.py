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
from .setting import *


def get_rpcs():
    rpcs = []
    for peer in PEERS:
        host = peer[peer.find('@')+1:]
        c = zerorpc.Client('tcp://{0}:{1}'.format(host, RPC_PORT), timeout=None)
        if c:
            rpcs.append(c)
    return rpcs

def execute(site, method):
    gevent.spawn(globals()[method], site, get_rpcs(), 10)


def delete_expire_task(expire_hours=EXPIRE_HOURS):
    """ delete the expire RUNNING Task, expire_hours is in settings
        TODO: expire_hours be set on the web page

    :param expire_hours: set the expire running task in hours
    """
    expire_datetime = datetime.utcnow() - timedelta(hours=expire_hours)
    for t in Task.objects(status=102, updated_at__lt=expire_datetime):
        t.status = 105
        t.save()


class Scheduler(object):
    """ make schedules easy """
    def get_schedules(self):
        return Schedule.objects(enabled=True) 

    def run(self):
        counter = 0
        while True:
            if counter >= 60:
                counter = 0
                gevent.spawn(delete_expire_task())
            for s in self.get_schedules():
                if s.timematch():
                    execute(s.site, s.method)
            gevent.sleep(60)
            counter += 1
