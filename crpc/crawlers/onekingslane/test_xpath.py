#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
import re
from datetime import datetime, timedelta

from crawlers.common.stash import *
import requests
from requests.packages.urllib3.connectionpool import *
import ssl
def connect_vnew(self):
    # Add certificate verification
    sock = socket.create_connection((self.host, self.port), self.timeout)

    # Wrap socket using verification with the root certs in
    # trusted_root_certs
    self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file,
                                cert_reqs=self.cert_reqs,
                                ca_certs=self.ca_certs,
                                ssl_version=ssl.PROTOCOL_TLSv1)
    if self.ca_certs:
        match_hostname(self.sock.getpeercert(), self.host)


VerifiedHTTPSConnection.connect = connect_vnew

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
            date = ' '.join( [d for d in node.cssselect('span.date')[0].text_content().split('\n') if d] )
            all_times = node.cssselect('div.all-times > h3')[0].text_content().split('PT')[0].split()[-1]
            datethen = time_convert(date + ' ' + all_times + ' ', '%b %d %I%p %Y')
            print datethen
            markets = node.cssselect('div.all-times > ul > li')
            for market in markets:
                link = market.cssselect('h4 > a')[0].get('href')
                link = link if link.startswith('http') else self.siteurl + link
                event_id = self.extract_eventid.match(link).group(1)
                img = market.cssselect('h4 > a > img')[0].get('src') + '?$mp_hero_standard_2.8$'
                sale_title = market.cssselect('h4 > a')[0].text_content()
                short_desc = market.cssselect('p.shortDescription')[0].text_content()
                detail_tree = lxml.html.fromstring(self.net.fetch_page(link))
                sale_description = detail_tree.cssselect('div#wrapper > div#okl-content > div.sales-event > div#okl-bio > div.event-description .description')
                if sale_description:
                    sale_description = sale_description[0].text.strip()
#                print event_id, img, sale_title, [short_desc], sale_description
                


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

    def one_page(self, url):
        self.extract_eventid = re.compile('https://www.onekingslane.com/sales/(\d+)')
        cont = self.net.fetch_page(url)
        tree = lxml.html.fromstring(cont)
        path = tree.cssselect('div#wrapper > div#okl-content > div.sales-event')[0]
        event_id = self.extract_eventid.match(url).group(1)
        sale_description = path.cssselect('div#okl-bio > div.event-description .description')
        if sale_description:
            print sale_description[0].text.strip()
        end_date = path.cssselect('div#okl-bio > h2.share')[0].get('data-end')
        print self.utcstr2datetime(end_date)

    def utcstr2datetime(self, date_str):
        """.. :py:method::
            covert time from the format into utcnow()
            '20121105T150000Z'
        """
        fmt = "%Y%m%dT%H%M%S"
        return datetime.strptime(date_str.rstrip('Z'), fmt)


if __name__ == '__main__':
    s = Server()
#    s.crawl_category()
    s.upcoming_proc()
