#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
from helpers.log import getlogger
import gevent
import resource
resource.setrlimit(resource.RLIMIT_NOFILE, (4096, 4096))

from backends.monitor.logstat import *
from backends.monitor.scheduler import Scheduler, execute
from backends.monitor.events import run_command


@run_command.bind
def execute_cmd(sender, **kwargs):
    site = kwargs.get('site')
    method = kwargs.get('method')
    logger.warning('site.method: {0}.{1}'.format(site, method))
    execute(site, method)

gevent.spawn(Scheduler().run)

logger = getlogger("monitor")

while True:
#    logger.warning("looping")
    gevent.sleep(10)
    
