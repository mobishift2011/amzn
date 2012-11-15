# -*- coding: utf-8 -*-
"""
backend.monitor.watcher
~~~~~~~~~~~~~~~~~~~~~~~

a watch-dog like daemon to monitor the run.py process.

It  is supposed to be called from run module as that starts running.

run.py

"""

import os

def watch(ps_name):
    results = os.popen('ps aux | grep %s' % ps_name)
    results = 
    

if __name__ == "__main__":
    watch('run.py')
