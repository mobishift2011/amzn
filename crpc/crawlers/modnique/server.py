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
        self.extract_slug_id = re.compile('.*/saleevent/(.+)/(\w+)/seeac/gseeac')
        self.headers = {
            'Host':' www.modnique.com',
            'Referer':' http://www.modnique.com/saleevents',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Ubuntu/12.10 Chromium/22.0.1229.94 Chrome/22.0.1229.94 Safari/537.4',
            'X-Requested-With': 'XMLHttpRequest',
        }

    def crawl_category(self, ctx=''):
        """.. :py:method::
        """
        content = fetch_page(self.eventurl, self.headers)
        if content is None or isinstance(content, int):
            content = fetch_page(self.eventurl, self.headers)
        tree = lxml.html.fromstring(content)
        events = tree.cssselect('div.bgDark > div.mbm > div > div.page > ul#nav > li.fCalc:first-of-type')[0]
        category_link = {}
        # categories should be ['apparel', 'jewelry-watches', 'handbags-accessories', 'shoes', 'beauty', 'men']
        for e in events.cssselect('ul.subnav > li.eventsMenuWidth > ul.pbm > li.unit > a.pbn'):
            link = e.get('href')
            category_link[ link.rsplit('/', 1)[-1] ] = link
        
        link = tree.cssselect('div.bgDark > div.mbm > div > div.page > ul#nav > li.fCalc:nth-of-type(2) > a.phl')[0].get('href')
        category_link[ link.rsplit('/', 1)[-1] ] = link

        # http://www.modnique.com/saleevent/Daily-Deal/2000/seeac/gseeac
        sale = tree.cssselect('div.bgDark > div.mbm > div > div.page > ul#nav > li.fCalc:nth-of-type(3) > a.phl')[0].get('href')

        for category, link in category_link.iteritems():
            self.crawl_dept(category, link, ctx)

    def crawl_dept(self, dept, url, ctx):
        """.. :py:method::
        """
        content = fetch_page(url, self.headers)
        if content is None or isinstance(content, int):
            content = fetch_page(url, self.headers)
        tree = lxml.html.fromstring(content)
        if dept == 'the-shops':
            nodes = tree.cssselect('div.bgShops > div#content > div#sales > div.pbm > div.page > ul.bannerfix > li > div.shop_thumb > div.media')
        else:
            nodes = tree.cssselect('div.bgDark > div#content > div.sales > div.pbm > div.page > ul.bannerfix > li#saleEventContainer > div.sale_thumb > div.media')
        for node in nodes:
            link = node.cssselect('a.sImage')[0].get('href')
            slug, event_id = self.extract_slug_id.match(link).groups()
            link = link if link.startswith('http') else self.siteurl + link
            img = node.cssselect('a.sImage > img')[0].get('src')
            if dept == 'the-shops': image_urls = [img]
            else: image_urls = [img.replace('B.jpg', 'A.jpg'), img]
            sale_title = node.cssselect('div.sDefault > div > a > span')[0].text_content().strip()

            is_new, is_updated = False, False
            event = Event.objects(event_id=event_id).first()
            if not event:
                is_new = True
                event = Event(event_id=event_id)
                event.urgent = True
                event.combine_url = link
                event.sale_title = sale_title
        if dept not in event.dept: event.dept.append(dept)
        [event.image_urls.append(img) for img in image_urls if img not in event.image_urls]
        # TODO event.events_begin = events_begin
        # event.events_end = events_end
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=link, is_new=is_new, is_updated=is_updated)



    def crawl_listing(self, url, ctx=''):
        """.. :py:method::
        """
        content = fetch_page(url)
        content = fetch_page(url, self.headers)
        if content is None or isinstance(content, int):
            common_failed.send(sender=ctx, key='', url=url,
                    reason='download listing url error, {0}'.format(content))
            return
        tree = lxml.html.fromstring(content)


if __name__ == '__main__':
    import zerorpc
    from settings import CRAWLER_PORT
    server = zerorpc.Server(Server(), heartbeat=None)
    server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
    server.run()
