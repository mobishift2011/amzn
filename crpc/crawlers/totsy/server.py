#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
from datetime import datetime, timedelta

from crawlers.common.stash import *
from crawlers.common.events import common_saved, common_failed
from models import *

class totsyLogin(object):
    """.. :py:class:: totsyLogin
        login, check whether login, fetch page.
    """
    def __init__(self):
        """.. :py:method::
            variables need to be used
        """
        self.login_url = 'https://www.totsy.com/customer/account/login/'
        self.data = { 
            'login[username]': login_email,
            'login[password]': login_passwd,
        }    

        self._signin = False

    def login_account(self):
        """.. :py:method::
            use post method to login
        """
        request.get(self.login_url)
        request.post('https://www.totsy.com/customer/account/loginPost/', data=self.data)
        self._signin = True

    def check_signin(self):
        """.. :py:method::
            check whether the account is login
        """
        if not self._signin:
            self.login_account()

    def fetch_page(self, url):
        """.. :py:method::
            fetch page.
            check whether the account is login, if not, login and fetch again
        """
        ret = request.get(url)

        if 'https://www.totsy.com/customer/account/login' in ret.url:
            self.login_account()
            ret = request.get(url)
        if ret.ok: return ret.content

        return ret.status_code


class Server(object):
    def __init__(self):
        self.eventurl = 'http://www.totsy.com/event'
        self.net = totsyLogin()
        self.extract_event_id = re.compile('http://www.totsy.com/sales/(.+).html')
        self.extract_events_end = re.compile("getTimerHtml\(.+('|\")(.+)('|\")\);")


    def crawl_category(self, ctx=''):
        """.. :py:method::
        """
        content = self.net.fetch_page(self.eventurl)
        if content is None or isinstance(content, int):
            common_failed.send(sender=ctx, key='', url=url,
                    reason='download event page failed: {0}'.format(content))
        tree = lxml.html.fromstring(content)
        nodes = tree.cssselect('div#stickywrap section#events-live ul.thumbnails > li.catalog-event')
        for node in nodes:
            self.parse_event_node(node, ctx)

        upcoming_nodes = tree.cssselect('div#stickywrap section#events-upcoming > ul.thumbnails > li.catalog-event')
        for node in upcoming_nodes:
            self.parse_upcoming_node(node, ctx)

    def parse_event_node(self, node, ctx):
        """.. :py:method::
            parse every event node
        """
        link = node.cssselect('a.thumbnail')[0].get('href')
        event_id = self.extract_event_id.match(link).group(1)
        sale_title = node.cssselect('a.thumbnail > hgroup')[0].text_content().strip()
        nav = node.cssselect('a.thumbnail > div.more > div.more-content > section.container > h6')
        dept, ages = [], []
        for n in nav:
            if n.text_content() == 'Categories:':
                for d in n.getnext().text_content().split('\n'):
                    if d.strip(): dept.append(d.strip())
            elif n.text_content() == 'Ages:': 
                for d in n.getnext().text_content().split('\n'):
                    if d.strip(): ages.append(d.strip())
        text = node.cssselect('a.thumbnail > script')[0].text_content()
        ends = self.extract_events_end.search(text).group(2) # 'December 23, 2012, 8:00:00' the timezone when you regist
        utc_events_end = datetime.strptime(ends, '%B %d, %Y, %X') - timedelta(hours=8) # -8 hours, set beijing to utc

        event, is_new, is_updated = self.get_or_create_event(event_id, link, sale_title)
        [event.dept.append(d) for d in dept if d not in event.dept]
        [event.ages.append(d) for d in ages if d not in event.ages]
        event.events_end = utc_events_end
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=link, is_new=is_new, is_updated=is_updated)

    def parse_upcoming_node(self, node, ctx):
        """.. :py:method::
            parse every upcoming event node
        """
        link = node.cssselect('span.echoShare')[0].get('data-producturl')
        event_id = self.extract_event_id.match(link).group(1)
        sale_title = node.cssselect('span.echoShare')[0].get('data-productname')
        text = node.cssselect('div.thumbnail > script')[0].text_content()
        begin = self.extract_events_end.search(text).group(2) # 'December 23, 2012, 8:00:00' the timezone when you regist
        utc_events_begin = datetime.strptime(begin, '%B %d, %Y, %X') - timedelta(hours=8) # -8 hours, set beijing to utc

        event, is_new, is_updated = self.get_or_create_event(event_id, link, sale_title)
        if is_new:
            content = self.net.fetch_page(link)
            tree = lxml.html.fromstring(content)
            nav = tree.cssselect('div#mainContent > section.event-landing > div.intro')[0]
            img = nav.cssselect('div > div.category-image > img')[0].get('src')
            sale_description = nav.cssselect('div.intro-content > p')[0].text_content()
            event.image_urls = [img]
            event.sale_description = sale_description
        event.events_begin = utc_events_begin
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=link, is_new=is_new, is_updated=is_updated)

    def get_or_create_event(self, event_id, link, sale_title):
        """.. :py:method::
        :param event_id:
        :param link: event listing url
        :param sale_title: event title 
        """
        is_new, is_updated = False, False
        event = Event.objects(event_id=event_id).first()
        if not event:
            is_new = True
            event = Event(event_id=event_id)
            event.urgent = True
            event.combine_url = link
            event.sale_title = sale_title
        return event, is_new, is_updated

    def crawl_listing(self, url, ctx=''):
        pass

    def crawl_product(self, url, ctx=''):
        pass

if __name__ == '__main__':
    Server().crawl_category()
