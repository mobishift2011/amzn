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

def is_task_already_running(site, method):
    """ return whether task is already running

    a set is used to keep task running info 
    Caution: But this method can not keep atomic
    """
    key = '{0}.{1}'.format(site, method.split('_')[0])
    if key in SCHEDULE_STATE:
        # print 'The Task of {0}:{1} is already running.'.format(key, method)
        # with open('/tmp/sche.debug', 'a') as fd:
        #     fd.write('The Task of {0}:{1} is already running.\n'.format(key, method))
        #     fd.write(str(SCHEDULE_STATE) + '\n\n')
        return True
    return False


def can_task_run(site, method):
    """ run task, if the task is not running, else return False

    """
    key = '{0}.{1}'.format(site, method.split('_')[0])
    with lock:
        if key in SCHEDULE_STATE:
            # print 'run_task:: The Task of {0}:{1} is already running.'.format(key, method)
            # with open('/tmp/sche.debug', 'a') as fd:
            #     fd.write('run_task:: The Task of {0}:{1} is already running.\n'.format(key, method))
            #     fd.write(str(SCHEDULE_STATE) + '\n\n')
            return False
        # open('/tmp/sche.debug', 'a').write('run_task:: The Task of {0}:{1} is running now.\n'.format(key, method))
        SCHEDULE_STATE.add(key)
        return True


def task_completed(greenlet, site, method):
    """ removes state info from set """
    key = '{0}.{1}'.format(site, method.split('_')[0])
    # open('/tmp/sche.debug', 'a').write('{0}:{1} is complete.\n'.format(key, method))
    with lock:
        if key in SCHEDULE_STATE:
            SCHEDULE_STATE.remove(key) 
            # open('/tmp/sche.debug', 'a').write('{0}:{1} is delete key.\n'.format(key, method))

def task_broke_completed(site, method):
    """ removes state info from set """
    key = '{0}.{1}'.format(site, method.split('_')[0])
    # open('/tmp/sche.debug', 'a').write('{0}:{1} is broke complete.\n'.format(key, method))
    with lock:
        if key in SCHEDULE_STATE:
            SCHEDULE_STATE.remove(key) 
            # open('/tmp/sche.debug', 'a').write('{0}:{1} is broke delete key.\n'.format(key, method))
