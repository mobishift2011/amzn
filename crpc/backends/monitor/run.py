#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
from helpers.log import getlogger
import gevent
from datetime import datetime

from backends.monitor.scheduler import Scheduler
from backends.monitor.autoschedule import execute, avoid_cold_start, auto_schedule
from backends.monitor.events import run_command # spawn listener to listen webui signal


# bind listeners
from backends.monitor.logstat import *
import powers.binds
# end binding

@run_command.bind
def execute_cmd(sender, **kwargs):
    site = kwargs.get('site')
    method = kwargs.get('method')
    logger.warning('site.method: {0}.{1}'.format(site, method))
    execute(site, method)

gevent.spawn(Scheduler().run)
gevent.spawn(avoid_cold_start)

logger = getlogger("monitor")


while True:
    try:
        auto_schedule()
        gevent.sleep(60 - datetime.utcnow().second)
    except Exception as e:
        with open('/tmp/schedule.log', 'a') as fd:
            fd.write(str(e) + '\n\n\n')

