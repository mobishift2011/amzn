#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import gevent

import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (4096, 4096))

from datetime import datetime
import collections

from backends.monitor.executor import execute
from backends.monitor.scheduler import Scheduler
from backends.monitor.autoschedule import avoid_cold_start, auto_schedule
from backends.monitor.events import run_command # spawn listener to listen webui signal
from backends.monitor.events import auto_scheduling # manual evoking schedules
from backends.monitor.ghub import GHub


# bind listeners
from backends.monitor.logstat import *
import powers.binds

@run_command.bind
def execute_cmd(sender, **kwargs):
    site = kwargs.get('site')
    method = kwargs.get('method')
    logger.warning('site.method: {0}.{1}'.format(site, method))
    execute(site, method)

def wait(seconds=60):
    import time
    while seconds>0:
        print 'sleeping'
        time.sleep(1)
        seconds -= 1

@auto_scheduling.bind('sync')
def toggle_auto_scheduling(sender, **kwargs):
    """ toggle whether we should do auto scheduling """
    from backends.monitor.organizetask import smethod_time
    auto = kwargs.get('auto')
    if auto:
        if (not GHub().acs_exists()):
            # we should spawn acs by invoking ``avoid_cold_start``
            logger.info("starting auto schedules")
            avoid_cold_start() 
    elif (not auto):
        # we should stop all the ``tasks`` and ``acs``
        logger.info("stopping auto schedules")
        logger.info(repr(smethod_time))
        smethod_time = collections.defaultdict(set)
        GHub().stop('tasks')
        GHub().stop('acs')

# end binding

gevent.spawn(Scheduler().run)
gevent.spawn_later(5, toggle_auto_scheduling, 'webui', auto=True)


while True:
    try:
        auto_schedule()
        gevent.sleep(60 - datetime.utcnow().second)
    except Exception as e:
        with open('/tmp/schedule.log', 'a') as fd:
            fd.write(str(e) + '\n\n\n')

