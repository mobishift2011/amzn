#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
backends.monitor.onlytask
~~~~~~~~~~~~~~~~~~~~~~~
Avoid one schedule run two task at the same time.

avoid_two_same_task_running: call before execute one task
release_one_task_key: call after the post_general_update

And we can delete_expire_task: the task is running, but no update in 7 minutes

site:           name of the crawler's directory
method:         name of the crawler's function
"""

from .setting import SCHEDULE_STATE

def avoid_two_same_task_running(site, method):
    """ avoid two same task running at the same time
    """
    key = '{0}.{1}'.format(site, method)
    if key in SCHEDULE_STATE:
        # gevent will catch this exception
        raise Exception('The Task of {0} is already running.'.format(key))
    SCHEDULE_STATE[key] = True


def release_one_task_key(site, method):
    """ pop the key from dict, this schedule can run again.
    """
    key = '{0}.{1}'.format(site, method)
    if key in SCHEDULE_STATE:
        SCHEDULE_STATE.pop(key)

