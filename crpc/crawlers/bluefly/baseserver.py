#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.common.rpcserver
~~~~~~~~~~~~~~~~~~~~~~~~~

Provides a meta programmed integrated RPC call for all callers

"""
from gevent.coros import Semaphore
from selenium.common.exceptions import *
import lxml.html
import requests
import urllib
from selenium import webdriver
import time
from crawlers.common.stash import *


class BaseServer(object):
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    siteurl = ''
    email = '2012luxurygoods@gmail.com'
    passwd = 'abcd1234'
    session = requests.session()
    session.headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
                        'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 '}

    def __init__(self):
        self._browser = None
        
    @property
    def browser(self):
        if not self._browser:
            self._browser = webdriver.Chrome()
        return self._browser

    def bopen(self,url):
        """ open url with browser
        """
        start = time.time()
        try:
            self.browser.get(url)
        except TimeoutException:
            return False
        else:
            #self.html = self.browser.content
            #self.tree = lxml.html.fromstring(self.html)
            print 'bopen used',time.time() - start
            return True

    def ropen(self,url):
        """ open url with requests
        """
        start = time.time()
        res = self.session.get(url)
        status_code = res.status_code

        if status_code in [200,301]:
            self.html = res.text
            self.tree = lxml.html.fromstring(self.html)
            print 'ropen used',time.time() - start
            return self.tree
        else:
            raise HttpError(status_code,url)

    @exclusive_lock(siteurl)
    def crawl_category(self,*args,**kwargs):
        """.. :py:method::
            From top depts, get all the events
        """
        pass

    @exclusive_lock(siteurl)
    def crawl_listing(self,*args,**kwargs):
        pass

    @exclusive_lock(siteurl)
    def crawl_product(self,*args,**kwargs):
        pass

    def format_url(self,url):
        if url.startswith('http://'):
            return url
        else:
            return  urllib.basejoin(self.siteurl,url)

if __name__ == '__main__':
    s = BaserServer()
    #import zerorpc
    #zs = zerorpc.Server(CrawlerServer()) 
    #zs.bind("tcp://0.0.0.0:{0}".format(CRAWLER_PORT))
    #zs.run()

