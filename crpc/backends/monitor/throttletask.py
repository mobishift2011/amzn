#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
backends.monitor.throttletask
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Avoid two task run simutanously

site:           name of the crawler's directory
method:         name of the crawler's function
"""

from .setting import SCHEDULE_STATE
from gevent.coros import Semaphore

lock = Semaphore(1)

def task_already_running(site, method):
    """ return whether task is already running

    a set is used to keep task running info 
    """
    key = '{0}.{1}'.format(site, method.split('_')[0])
    with lock:
        if key in SCHEDULE_STATE:
            print 'The Task of {0} is already running.'.format(key)
            return True
        SCHEDULE_STATE.add(key)
        return False

def task_completed(greenlet, site, method):
    """ removes state info from set """
    key = '{0}.{1}'.format(site, method.split('_')[0])
    with lock:
        if key in SCHEDULE_STATE:
            SCHEDULE_STATE.remove(key) 
