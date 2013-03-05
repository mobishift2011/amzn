#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import zerorpc
from crawlers.common.stash import picked_crawlers

class CheckServer(object):
    def __init__(self):
        self.mod = {}

        for crawler in picked_crawlers:
            try:
                m = __import__('crawlers.{0}.simpleclient'.format(crawler), fromlist=['CheckServer'])
                self.mod[crawler] = m.CheckServer()
            except:
                continue

    def run_cmd(self, site, method, args, kwargs):
        return getattr(self.mod[site], method)(*args, **kwargs)

if __name__ == '__main__':
    import sys
    from settings import CRAWLER_PORT

    port = CRAWLER_PORT if len(sys.argv) != 2 else int(sys.argv[1])
    server = zerorpc.Server(CheckServer(), pool_size=50, heartbeat=None)
    server.bind("tcp://0.0.0.0:{0}".format(port))
    server.run()
