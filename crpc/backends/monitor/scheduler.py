#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Scheduler: runs crawlers in background
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from gevent import monkey; monkey.patch_all()
import gevent

from crawlers.common.routine import update_category, update_listing, update_product
from .models import Schedule

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

class Scheduler(object):
    """ make schedules easy """
    def get_schedules(self):
        return Schedule.objects(enabled=True) 

    def run(self):
        while True:
            for s in get_schedules():
                if s.timematch():
                    gevent.spawn(globals()[s.method], s.site, get_rpcs())
            gevent.sleep(60)