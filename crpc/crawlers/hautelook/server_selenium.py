#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.myhabit.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""
import os
import re
import sys
import time
import Queue
import zerorpc
import lxml.html
import urllib2
import pytz

from urllib import quote, unquote
from datetime import datetime, timedelta
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *

TIMEOUT = 5

class Server(object):
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    def __init__(self):
        self.siteurl = 'http://www.hautelook.com'
        self._signin = False

        self.extract_eventid_re = re.compile(r'http://www.hautelook.com/event/(\d+).*')
        self.extract_eventimg_re = re.compile(r'/py/resizer/\d+x\d+(/assets/.*)')

    def login(self):
        """.. :py:method::
            login myhabit
            Using Firefox will cause Xvfb memory leaf and program broke.

        """
        self.browser = webdriver.Chrome()
#        self.browser.implicitly_wait(1)
        self.browser.get('http://www.hautelook.com/login')
        self.fill_login_form()
        WebDriverWait(self.browser, TIMEOUT, 0.1).until(lambda driver: driver.execute_script('return $.active') == 0)

    def fill_login_form(self):
        """.. :py:method:
            fill in login form when chrome driver is open
        """
        self.browser.find_element_by_css_selector('div#login_form_container > form#login_signin input#login_email').send_keys(login_email)
        self.browser.find_element_by_css_selector('div#login_form_container > form#login_signin input.passwordInput').send_keys(login_passwd)
        self.browser.find_element_by_css_selector('div#login_form_container > form#login_signin div#login_button_standard').click()
        self._signin = True

    def check_signin(self):
        """.. :py:method:
            If _signin flag is OK.
            But Chrome is not open by webdriver, the .title will raise a :
                URLError: <urlopen error [Errno 111] Connection refused>
        """
        if not self._signin:
            self.login()
        else:
            try:
                self.browser.title
            except urllib2.URLError:
                self.login()


    def download_page(self, url):
        """.. :py:method::
            download the url
        :param url: the url need to download
        """
        time_begin_benchmark = time.time()
        try:
            self.browser.get(url)
            WebDriverWait(self.browser, TIMEOUT, 0.1).until(lambda driver: driver.find_element_by_css_selector('div#body div#main div#page-content div#bottom-content'))
        except selenium.common.exceptions.TimeoutException:
            try:
                WebDriverWait(self.browser, TIMEOUT, 0.1).until(lambda driver: driver.execute_script('return $.active') == 0)
            except selenium.common.exceptions.TimeoutException:
                print 'Timeout --> {0}'.format(url)
                return 1
        print 'time download benchmark: ', time.time() - time_begin_benchmark

    def download_regular_page(self, url):
        time_begin_benchmark = time.time()
        try:
            self.browser.get(url)
            WebDriverWait(self.browser, TIMEOUT, 0.1).until(lambda driver: driver.execute_script('return $.active') == 0)
        except selenium.common.exceptions.TimeoutException:
            print 'Timeout --> {0}'.format(url)
            return 1
        print 'time download_regular_page benchmark: ', time.time() - time_begin_benchmark


    @exclusive_lock(DB)
    def crawl_category(self, ctx):
        """.. :py:method::
            From top depts, get all the brands
        """
        self.check_signin()
        depts = ['women', 'beauty', 'home', 'kids', 'men']
        debug_info.send(sender=DB + '.category.begin')

        self.upcoming_proc()
        for dept in depts:
            link = 'http://www.hautelook.com/events#{0}'.format(dept)
            self.get_event_list(dept, link, ctx)
        self.browser.quit()
        self._signin = False
        debug_info.send(sender=DB + '.category.end')

    def upcoming_proc(self):
        """.. :py:method::
            Get all the upcoming brands info 
        """
        tree = lxml.html.fromstring(self.browser.page_source)
        node = tree.cssselect('div#container > div#body_content > div#upcoming_events > div#module_coming_soon > div[id^=block_]')[0]

    def get_event_list(self, dept, url, ctx):
        """.. :py:method::
            Get all the brands from brand list.
            Brand have a list of product.

        :param dept: dept in the page
        :param url: the dept's url
        """
        self.download_regular_page(url)
        tree = lxml.html.fromstring(self.browser.page_source)
        nodes = tree.cssselect('div#container > div#body_content > div#module_event_tiles > div > div.tile')
        for node in nodes:
            l = node.cssselect('a.hero-link')[0].get('href')
            link = l if l.startswith('http') else self.siteurl + l
            sale_id = self.extract_eventid_re.match(link).group(1)
            
            sale_title = node.cssselect('a.hero-link > div.caption > .title')[0].text
            img = node.cssselect('a.hero-link > img.hero')[0].get('src')
            if not img.startswith('http'):
                img = self.siteurl + self.extract_eventimg_re.match(img).group(1)
            # pop-medium, pop-large.jpg; event-large.jpg < grid-large.jpg
            img = re.sub(r'(.*)(small|med).jpg', '\\1large.jpg', img)
            image = re.sub(r'(.*)event(-large.jpg)', '\\1grid\\2', img)

            brand, is_new = Event.objects.get_or_create(sale_id=sale_id)
            if is_new:
                brand.sale_title = sale_title
                brand.image_urls = [image]
                brand.dept = [dept]
            else:
                if image not in brand.image_urls: brand.image_urls.append(image)
                if dept not in brand.dept: brand.dept.append(dept) # for designer dept
            brand.update_time = datetime.utcnow()
            brand.save()
            print is_new
            common_saved.send(sender=ctx, key=sale_id, url=url, is_new=is_new, is_updated=not is_new)

    @exclusive_lock(DB)
    def crawl_listing(self, url, ctx):
        """.. :py:method::
            not implement
        """
        pass

    @exclusive_lock(DB)
    def crawl_product(self, url, ctx):
        """.. :py:method::
            not implement
        """
        pass

        

if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(CRAWLER_PORT))
    server.run()
