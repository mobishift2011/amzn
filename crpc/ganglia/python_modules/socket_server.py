#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

"""
run this process as the user run run.py
"""
import os
import zerorpc
import subprocess

class socketServer(object):
    def _getsocket():
        pid = subprocess.Popen('ps aux | grep {0} | grep -v grep | grep -v dtach'.format(name.split('_')[0]), shell=True, stdout=subprocess.PIPE).communicate()[0].split()[1]
        ret = os.listdir('/proc/{0}/fd'.format(pid))
        return len(ret)

if __name__ == '__main__':
    ss = zerorpc.Server(socketServer(), heartbeat=None)
    ss.bind('tcp://localhost:6357')
    ss.run()
