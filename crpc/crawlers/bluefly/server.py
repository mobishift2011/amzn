#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.ruelala.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from gevent.coros import Semaphore
lock = Semaphore()

import os
import zerorpc
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support.ui import WebDriverWait
#selenium.webdriver.support.wait.POLL_FREQUENCY = 0.05

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *
import lxml
import datetime
import time

def safe_lock(func,*arg,**kwargs):
    def wrapper(*arg,**kwargs):
        lock.acquire()
        res = func(*arg,**kwargs)
        lock.release()
        return res
    return wrapper

class Server:
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    
    def __init__(self):
        self.siteurl = 'http://www.ruelala.com'
        self.email = 'huanzhu@favbuy.com'
        self.passwd = '4110050209'
        self.login(self.email, self.passwd)
        self.event_list = []
        self.product_list = []

    def get(self,url):
        try:
            self.browser.get(url)
        except TimeoutException:
            print 'time out >> ',url
            return False
        else:
            return True
            #return lxml.html.fromstring(self.browser.content)

    def login(self, email=None, passwd=None):
        """.. :py:method::
            login urelala

        :param email: login email
        :param passwd: login passwd
        """
        
        if not email:
            email, passwd = self.email, self.passwd
        try:
            self.browser = webdriver.Chrome()
        except:
            self.browser = webdriver.Firefox()
            self.browser.set_page_load_timeout(10)
            #self.profile = webdriver.FirefoxProfile()
            #self.profile.set_preference("general.useragent.override","Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3")

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
        self.get(self.site_url)
        result = []
        for i in self.browser.get_elements_by_xpath('//ul[@id="siteNav1"]/li')[0:-3]:
            a  = i.get_element_by_tag_name('a')
            name = a.text
            url = self.format_url(a.get_attribute('href'))
            result.append((name,url))
        return result
    
    @safe_lock
    def crawl_category(self,target_categorys=[]):
        """.. :py:method::
            From top depts, get all the events
        """
        all_category = []
        all_product = []

        navs = get_navs()
        for i in navs:
            nav,url = i
            all_category = self.get_all_category(nav,url)

            for j in all_category:
                name,url = j
                all_product = self.get_all_product(name,url)

                for k in all_product:
                    self.crawl_prodect_detail(k)

    @safe_lock
    def crawl_listing(self,sale_id,event_url):
        pass

    @safe_lock
    def crawl_product(self,product_id,product_url):
        pass

    def _crawl_product_detail(self,product_id,url):
        """.. :py:method::
            Got all the product basic information and save into the database
        """
        if not self.get(url):
            return False

        image_urls = []
        for image in self.browser.find_elements_by_xpath('//div[@id="imageViews"]/img'):
            href = image.get_attribute('src')
            url = os.path.join(self.siteurl,href)
            image_urls.append(url)

        list_info = []
        for li in self.browser.find_elements_by_xpath('//section[@id="info"]/ul/li'):
            list_info.append(li.text)

        sizes = []
        soldout_size = []
        for a in self.browser.find_elements_by_xpath('//ul[@id="sizeSwatches"]/li/a[@class="normal"]'):
            if a.get_attribute('class') == 'normal':
                sizes.append(a.text)
            else:
                soldout_size.append(a.text)

        price = self.browser.find_element_by_id('salePrice').text
        listprice  = self.browser.find_element_by_id('strikePrice').text
        _shipping = self.browser.find_elements_by_xpath('//section[@id="shipping"]/p')
        shipping = _shipping[0].text
        returns = _shipping[1].text
        left = False
        try:
            #span = self.browser.find_element_by_xpath('./section/span[@id="inventoryAvailable"]')
            span = self.browser.find_element_by_id('inventoryAvailable')
        except :
            pass
        else:
            left = span.text.split(' ')[0]
        
        product, is_new = Product.objects.get_or_create(key=str(product_id))
        if is_new:
            product.returns = returns
            priduct.shipping = shipping
            product.image_urls = image_urls
            product.list_info = info_table
            if sizes: product.sizes = sizes

        product.price = price
        product.listprice = listprice
        product.shipping = shipping
        if left == False:
            pass
        else:
            product.scarcity = left


        product.updated = True
        product.full_update_time = datetime.datetime.utcnow()
        product.save()
        """
        print 'size',sizes
        print 'shipping',shipping
        print 'returns',returns
        print 'left',left
        print 'list info',list_info 
        print 'image urls',image_urls
        """
        
        product_saved.send(sender=DB + '.parse_product_detail', site=DB, key=product_id, is_new=is_new, is_updated=not is_new)

    def _url2saleid(self, url):
        """.. :py:method::

        :param url: the brand's url
        :rtype: string of sale_id
        """
        id = url.split('/')[-1]
        try:
            id = str(id)
        except:
            raise ValueError('sale id error @ url %s' %url)
        else:
            return id

    def _url2product_id(self,url):
        if not url.startswith('http://'):
            raise ValueError('url is not start with http @url:%s in function `server.url2product_id`' %url)

        try:
            id = url.split('/')[-3]
            id = str(id)
            return id
        except:
            raise ValueError('split url error @url:%s' %url)

    def format_url(self,url):
        """
        ensure the url is start with `http://www.xxx.com`
        """

        if url.startswith('http://'):
            return url
        else:
            return os.path.join(self.site_url,url)

if __name__ == '__main__':
    server = Server()
    if 0: 
        sale_id = '54082'
        event_url = 'http://www.ruelala.com/event/54082'
        product_list = server._get_product_list(sale_id,event_url)
        print 'result >>',len(product_list)

    if 0:
        product_id = '1411832058'
        url = 'http://www.ruelala.com/event/product/58602/1411832058/1/DEFAULT'
        result = server._crawl_product_detail(product_id,url)

    if 0:
        id= '59022'
        url= 'http://www.ruelala.com/event/59022'
        server.crawl_listing(id,url)

    if 0:
        product_id = '1411832058'
        url = 'http://www.ruelala.com/event/product/58602/1411832058/1/DEFAULT'
        result = server.crawl_product(product_id,url)

    if 0:
        print '>>>>>>'
        category = 'women'
        server._get_event_list('women','http://www.ruelala.com/category/women')

    if 1:
        server.crawl_category()

