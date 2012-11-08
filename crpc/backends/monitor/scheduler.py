#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Scheduler: runs crawlers in background
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from gevent import monkey; monkey.patch_all()
import gevent

from backends.monitor.models import Schedule
from crawlers.common.routine import update_category, update_listing, update_product

import zerorpc
from settings import PEERS, RPC_PORT

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
