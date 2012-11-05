#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
import requests
import re
from datetime import datetime, timedelta
import pytz

headers = {
    'Host': 'www.onekingslane.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.2) Gecko/20121028 Firefox/15.2.1 PaleMoon/15.2.1',
    'Referer': 'https://www.onekingslane.com/login',
}

config = { 
    'max_retries': 3,
    'pool_connections': 10, 
    'pool_maxsize': 10, 
}
req = requests.Session(prefetch=True, timeout=20, config=config, headers=headers)


class onekingslaneLogin(object):
    """.. :py:class:: onekingslaneLogin
        login, check whether login, fetch page.
    """
    def __init__(self):
        """.. :py:method::
            variables need to be used
        """
        self.login_url = 'https://www.onekingslane.com/login'
        self.data = { 
            'email': 'huanzhu@favbuy.com',
            'password': '4110050209',
            'keepLogIn': 1,
            'sumbit.x': 54,
            'sumbit.y': 7,
            'returnUrl': '0',
        }   
        self._signin = False
        self.login_account()

    def login_account(self):
        """.. :py:method::
            use post method to login
        """
        req.post(self.login_url, data=self.data)
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
        ret = req.get(url)
        if ret.ok: return ret.content

    
class Server(object):
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    def __init__(self):
        self.siteurl = 'https://www.onekingslane.com'
        self.upcoming_url = 'https://www.onekingslane.com/calendar'
        self.net = onekingslaneLogin()
        self.extract_eventid = re.compile('https://www.onekingslane.com/sales/(\d+)')

    def crawl_category(self):
        """.. :py:method::
            From top depts, get all the events
        """
        depts = ['girls', 'boys', 'women', 'baby-maternity', 'toys-playtime', 'home']

        self.upcoming_proc()
        exit()
        for dept in depts:
            link = 'http://www.zulily.com/?tab={0}'.format(dept)
            self.get_event_list(dept, link, ctx)

            
    def upcoming_proc(self):
        """.. :py:method::
            Get all the upcoming brands info 
        """
        cont = self.net.fetch_page(self.upcoming_url)
        tree = lxml.html.fromstring(cont)
        nodes = tree.cssselect('body.holiday > div#wrapper > div#okl-content > div.calendar-r > div.day')
        for node in nodes:
            date = node.cssselect('span.date')[0].text_content()
            all_times = node.cssselect('div.all-times li > h3')
            markets = node.cssselect('div.all-times > ul > li')
            for market in markets:
                link = market.cssselect('h4 > a')[0].get('href')
                link = link if link.startswith('http') else self.siteurl + link
                event_id = self.extract_eventid.match(link).group(1)
#                event, is_new = Event.objects.get_or_create(event_id=event_id)
#                if is_new:
                img = market.cssselect('h4 > a > img')[0].get('src') + '?$mp_hero_standard_2.8$'
                sale_title = market.cssselect('h4 > a')[0].text_content()
                short_desc = market.cssselect('p.shortDescription')[0].text_content()
                detail_tree = lxml.html.fromstring(self.net.fetch_page(link))
                sale_description = detail_tree.cssselect('div#wrapper > div#okl-content > div.sales-event > div#okl-bio > div.event-description div.description')[0].text
                print event_id, img, sale_title, short_desc, sale_description
                


    def time_proc(self, time_str):
        """.. :py:method::

        :param time_str: 'Sat 10/27 6am'
        :rtype: datetime type utc time
        """
        time_format = '%a %m/%d %I%p%Y'
        pt = pytz.timezone('US/Pacific')
        tinfo = time_str + str(pt.normalize(datetime.now(tz=pt)).year)
        endtime = pt.localize(datetime.strptime(tinfo, time_format))
        return endtime.astimezone(pytz.utc)



if __name__ == '__main__':
    s = Server()
#    s.crawl_category()
    s.upcoming_proc()
