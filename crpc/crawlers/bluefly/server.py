# -*- coding: utf-8 -*-
"""
crawlers.ruelala.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""

from gevent import monkey
monkey.patch_all()
from gevent.coros import Semaphore
lock = Semaphore()
from crawlers.common.rpcserver import BaseServer

import os
from selenium import webdriver
from selenium.common.exceptions import *
from crawlers.common.events import category_saved, category_failed, category_deleted
from crawlers.common.events import product_saved, product_failed, product_deleted

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *
import urllib
import lxml.html
import time

def safe_lock(func,*arg,**kwargs):
    def wrapper(*arg,**kwargs):
        lock.acquire()
        res = func(*arg,**kwargs)
        lock.release()
        return res
    return wrapper

class Server(BaseServer):
    """.. :py:class:: Server
    This is zeroRPC server class for ec2 instance to crawl pages.
    """
    
    def __init__(self):
        self.siteurl = 'http://www.bluefly.com'
        self.site ='bluefly'
        #self.login(self.email, self.passwd)

    def login(self, email=None, passwd=None):
        """.. :py:method::
            login urelala

        :param email: login email
        :param passwd: login passwd
        """
        

        #self.browser.implicitly_wait(2)
        self.browser.get(self.siteurl)
        time.sleep(3)
        
        # click the login link
        node = self.browser.find_element_by_id('pendingTab')
        node.click()
        time.sleep(2)

        a = self.browser.find_element_by_id('txtEmailLogin')
        a.click()
        a.send_keys(email)

        b = self.browser.find_element_by_id('txtPass')
        b.click()
        b.send_keys(passwd)

        signin_button = self.browser.find_element_by_id('btnEnter')
        signin_button.click()

        title = self.browser.find_element_by_xpath('//title').text
        if title  == 'Rue La La - Boutiques':
            self._signin = True
        else:
            self._signin = False

    def get_navs(self):
        result = []
        tree = self.ropen(self.siteurl)
        for a in tree.xpath('//ul[@id="siteNav1"]/li/a')[:-1]:
            name = a.text_content()
            href = a.get('href') 
            url = self.format_url(href)
            result.append((name,url))
        return result


    def url2category_key(self,href):
        return  href.split('/')[-2]

    def _get_all_category(self,nav,url):

            
        tree = self.ropen(url)
        for div in tree.xpath('//div[@id="deptLeftnavContainer"]'):
            h3 = div.xpath('.//h3')[0].text_content()
            if h3 == 'categories':
                links = div.xpath('.//ul/li/a')
                break
        # patch
        if nav.upper() == 'KIDS':
            links = tree.xpath('//span[@class="listCategoryItems"]/a')

        for a in links:
            href = a.get('href')
            name = a.text_content()
            url = self.format_url(href)
            key = self.url2category_key(href)
            
            category ,is_new = Category.objects.get_or_create(key=key)
            category.name = name
            category.url = url
            category.save()
            # send singnal
            category_saved.send(sender = 'bluefly.crawl_category',
                                site = self.site,
                                key = key,
                                is_new = is_new,
                                is_updated = not is_new)

    @safe_lock
    def crawl_category(self):
        """.. :py:method::
            From top depts, get all the events
        """
        for i in self.get_navs():
            import time
            time.sleep(2)
            nav,url = i
            print nav,url
            self._get_all_category(nav,url)
    
    def crawl_listig(self,url):
        key = self.url2category_key(url)
        category ,is_new = Category.objects.get_or_create(key=key)
        pass

    def _crawl_product_detail(self,product_id,url):
        """.. :py:method::
            Got all the product basic information and save into the database
        """
        pass

if __name__ == '__main__':
    server = Server()
    #server._get_all_category('test','http://www.bluefly.com/a/shoes')
    server.crawl_category()
    #print server.get_navs()
