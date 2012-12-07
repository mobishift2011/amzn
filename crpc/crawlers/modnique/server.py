#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

"""
crawlers.modnique.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.
"""
import lxml.html

from models import *
from crawlers.common.events import common_saved, common_failed
from crawlers.common.stash import *


class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.modnique.com'
        self.eventurl = 'http://www.modnique.com/all-sale-events'

    def crawl_category(self, ctx=''):
        content = fetch_page(self.eventurl)
        if content is None or isinstance(content, int):
            content = fetch_page(self.eventurl)
        tree = lxml.html.fromstring(content)
        events = tree.cssselect('div.bgDark > div.mbm > div > div.page > ul#nav > li.fCalc:first-of-type')[0]
        category_link = {}
        # categories should be ['apparel', 'jewelry-watches', 'handbags-accessories', 'shoes', 'beauty', 'men']
        for e in events.cssselect('ul.subnav > li.eventsMenuWidth > ul.pbm > li.unit > a.pbn'):
            link = e.get('href')
            category_link[ link.rsplit('/', 1)[-1] ] = link
        
        for e in tree.cssselect('div.bgDark > div.mbm > div > div.page > ul#nav > li.fCalc:nth-of-type(2) > a.phl')[0].get('href'):
            link = e.get('href')
            category_link[ link.rsplit('/', 1)[-1] ] = link

        # http://www.modnique.com/saleevent/Daily-Deal/2000/seeac/gseeac
        sale = tree.cssselect('div.bgDark > div.mbm > div > div.page > ul#nav > li.fCalc:nth-of-type(3) > a.phl')[0].get('href')

        for category, link in category_link.iteritems():
            pass

    def crawl_listing(self, url, ctx=''):
        content = fetch_page(self.eventurl)
        if content is None or isinstance(content, int):
            common_failed.send(sender=ctx, key='', url=self.eventurl,
                    reason='download event url error, {0}'.format(content))
            return

if __name__ == '__main__':
    Server().crawl_category()
#    import zerorpc
#    server = zerorpc.Server(Server())
#    server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
#    server.run()
