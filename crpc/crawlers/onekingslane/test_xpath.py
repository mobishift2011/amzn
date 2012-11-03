#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
import requests
import re
from datetime import datetime, timedelta
import pytz


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
        self.siteurl = 'http://www.zulily.com'
        self.upcoming_url = 'http://www.zulily.com/upcoming_events'
        self.net = zulilyLogin()
        self.extract_event_re = re.compile(r'(http://www.zulily.com/e/(.*).html).*')
        self.extract_image_re = re.compile(r'(http://mcdn.zulily.com/images/cache/event/)\d+x\d+/(.+)')

    def crawl_category(self):
        depts = ['girls', 'boys', 'women', 'baby-maternity', 'toys-playtime', 'home']
        self.get_brand_list('girls', 'http://www.zulily.com/?tab=women')

#        for dept in depts:
#            link = 'http://www.zulily.com/index.php?tab={0}'.format(dept)
#            self.get_brand_list(dept, link)
#        self.cycle_crawl_category()

    def get_brand_list(self, dept, url):
        cont = self.net.fetch_page(url)
        tree = lxml.html.fromstring(cont)
        nodes = tree.xpath('//div[@class="container"]/div[@id="main"]/div[@id="home-page-content"]/div//div[starts-with(@class, "home-row home-row-x")]/div[starts-with(@id, "eid_")]')
        print len(nodes)
        count = 0
        for node in nodes:
            link = node.xpath('./a[@class="wrapped-link"]')[0].get('href')
            link, lug = self.extract_event_re.match(link).groups()

            img = node.xpath('./a/span[@class="homepage-image"]/img/@src')[0]
            image = ''.join( self.extract_image_re.match(img).groups() )
            text = node.xpath('./a/span[@class="txt"]')[0]
            sale_title = text.xpath('./span[@class="category-name"]/span/text()')[0]
            desc = text.xpath('.//span[@class="description-highlights"]/text()')[0].strip()
            start_end_date = text.xpath('./span[@class="description"]/span[@class="start-end-date"]')[0].text_content().strip()
            print [link], [lug], [image], [sale_title], [desc], [start_end_date]
            count += 1
        print count
            
            
    def upcoming_proc(self):
        """.. :py:method::
            Get all the upcoming brands info 
        """
        upcoming_list = []
        cont = self.net.fetch_page(self.upcoming_url)
        tree = lxml.html.fromstring(cont)
        nodes = tree.xpath('//div[@class="event-content-list-wrapper"]/ul/li/a')
        for node in nodes:
            link = node.get('href')
            text = node.text_content()
            upcoming_list.append( (text, link) )
        self.upcoming_detail(upcoming_list)

    def upcoming_detail(self, upcoming_list):
        """.. :py:method::
        """
        for pair in upcoming_list:
            cont = self.net.fetch_page(pair[1])
            node = lxml.html.fromstring(cont).cssselect('div.event-content-wrapper')[0]
#            img = tree.xpath('//div[ends-with(@class, "event-content-image")]/img/@src')[0]
#            sale_title = tree.xpath('//div[@class="span-5 event-content-copy"]/h1/text()')[0]
#            sale_description = tree.xpath('//div[@class="span-5 event-content-copy"]/div[@id="desc-with-expanded"]')[0].text_content().strip()
#            start_time = tree.xpath('//div[@class="pan-9 upcoming-date-reminder]//span[@class="reminder-text"]/text()')[0]
#
            img = node.cssselect('div.event-content-image img')[0].get('src')
            image = ''.join( self.extract_image_re.match(img).groups() )
            sale_title = node.cssselect('div.event-content-copy h1')[0].text_content()
            sale_description = node.cssselect('div.event-content-copy div#desc-with-expanded')[0].text_content().strip()
            start_time = node.cssselect('div.upcoming-date-reminder span.reminder-text')[0].text_content() # 'Starts Sat 10/27 6am pt - SET REMINDER'
            events_begin = self.time_proc( ' '.join( start_time.split(' ', 4)[1:-1] ) )
            
            calendar_file = node.cssselect('div.upcoming-date-reminder a.reminder-ical')[0].get('href')
            ics_file = self.net.fetch_page(calendar_file)
            m = re.compile(r'URL:http://www.zulily.com/e/(.+).html.*').search(ics_file)
            lug = m.group(1)
            print [image], [sale_title], [sale_description], [events_begin], [lug]


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
    s.crawl_category()
    s.upcoming_proc()
