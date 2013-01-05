#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
from helpers.log import getlogger
import gevent
from datetime import datetime

from backends.monitor.scheduler import Scheduler
from backends.monitor.autoschedule import execute, avoid_cold_start, auto_schedule
from backends.monitor.events import run_command # spawn listener to listen webui signal
from backends.monitor.events import auto_scheduling # manual evoking schedules

from ghub import GHub

# bind listeners
from backends.monitor.logstat import *
import powers.binds

@run_command.bind
def execute_cmd(sender, **kwargs):
    site = kwargs.get('site')
    method = kwargs.get('method')
    logger.warning('site.method: {0}.{1}'.format(site, method))
    execute(site, method)

@auto_scheduling.bind
def toggle_auto_scheduling(sender, **kwargs):
    """ toggle whether we should do auto scheduling """
    auto = kwargs.get('auto')
    if auto and (not GHub.acs_exists()):
        # we should spawn acs by invoking ``avoid_cold_start``
        avoid_cold_start() 
    elif (not auto):
        # we should stop all the ``tasks`` and ``acs``
        GHub.stop('tasks')
        GHub.stop('acs')

# end binding

gevent.spawn(Scheduler().run)

logger = getlogger("monitor")

while True:
    try:
        auto_schedule()
        gevent.sleep(60 - datetime.utcnow().second)
    except Exception as e:
        with open('/tmp/schedule.log', 'a') as fd:
            fd.write(str(e) + '\n\n\n')

