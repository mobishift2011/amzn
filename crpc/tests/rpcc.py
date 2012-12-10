#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from gevent import monkey; monkey.patch_all()
import gevent
import zerorpc

cli = zerorpc.Client('tcp://127.0.0.1:5688', timeout=None)

def call():
    for i in xrange(10000):
        cli.abc()

if __name__ == '__main__':
    gevent.joinall([ gevent.spawn(call) for _ in xrange(1000)])
