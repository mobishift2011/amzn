#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import zerorpc

class sth(object):
    def __init__(self):
        self.count = 0

    def abc(self):
        print self.count
        self.count += 1

if __name__ == '__main__':
    server = zerorpc.Server(sth(), pool_size=2)
    server.bind('tcp://0.0.0.0:5688')
    server.run()
