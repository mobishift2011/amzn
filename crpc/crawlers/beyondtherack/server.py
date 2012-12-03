#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.beyondtherack.com'

    def crawl_category(self, ctx=''):
        dept_link = {
            'women': 'http://www.beyondtherack.com/event/calendar?category=1',
            'men': 'http://www.beyondtherack.com/event/calendar?category=2',
            'kids&babies': 'http://www.beyondtherack.com/event/calendar?category=3',
            'home': 'http://www.beyondtherack.com/event/calendar?category=4',
            'closet': 'http://www.beyondtherack.com/event/calendar?category=10',
        }

    def crawl_listing(self, url, ctx=''):
        pass

    def crawl_product(self, url, ctx=''):
        pass

if __name__ == '__main__':
    import zerorpc
    from settings import CRAWLER_PORT
    server = zerorpc.Server(Server())
    server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
    server.run()
