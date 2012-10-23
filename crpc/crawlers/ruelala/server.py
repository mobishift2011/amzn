#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.ruelala.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""
import gevent
gevent.monkey.patch_all()
from gevent.pool import Pool

import os
import re
import sys
import time
import Queue
import zerorpc
import lxml.html
import pytz

from urllib import quote, unquote
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support.ui import WebDriverWait

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *

class Server:
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """

    def __init__(self):
        self.siteurl = 'http://www.myhabit.com'
        self.email = 'huanzhu@favbuy.com'
        self.passwd = '4110050209'
        self.login(self.email, self.passwd)

    def login(self, email=None, passwd=None):
        """.. :py:method::
            login myhabit

        :param email: login email
        :param passwd: login passwd
        """
        if not email:
            email, passwd = self.email, self.passwd
        try:
            self.browser = webdriver.Chrome()
        except:
            self.browser = webdriver.Firefox()
            self.browser.set_page_load_timeout(5)
#        self.browser.implicitly_wait(5)

        self.browser.get(self.siteurl)
        self.browser.find_element_by_id('ap_email').send_keys(email)
        self.browser.find_element_by_id('ap_password').send_keys(passwd)
        signin_button = self.browser.find_element_by_id('signInSubmit')
        signin_button.submit()

        self._signin = True

    def check_signin(self):
        if not self._signin:
            self.login(self.email, self.passwd)

    def crawl(self,target_categorys=''):
        """.. :py:method::
            From top depts, get all the brands
        """
        categorys = target_categorys or ['women', 'men', 'living','kids','todays-fix']
        debug_info.send(sender=DB + '.category.begin')

        for category in categorys:
            url = 'http://www.ruelala.com/category/%s' %category
            event_list = self.crawl_event_list(category,url)

            for event in event_list:
                event_url =  event[0]
                sale_id =  event[1]
                product_list = self.crawl_product_list(sale_id,event_url)

                for product in product_list:
                    product_id = product[0]
                    product_url = product[1]
                    self.crawl_product_detail(product_id,product_url)

        debug_info.send(sender=DB + '.category.end')

    def crawl_event_list(self,category_name,url):
        """.. :py:method::
            Get all the brands from brand list.
            Brand have a list of product.

        :param dept: dept in the page
        :param url: the dept's url
        """
        self.browser.get(url)
        result = []
        nodes = self.browser.find_elements_by_xpath('//section[@id="alsoOnDoors"]/article"]')
        for node in nodes:
            image = node.find_element_by_xpath('./a/img').get_attribute('src')
            a_title = node.find_element_by_xpath('./footer/a[@class="eventDoorLink centerMe eventDoorContent"]/div[@class="eventName"]')
            a_link = node.find_element_by_xpath('./a[@class="eventDoorLink"]').get_attribute('href')
            a_url = os.path.join(self.siteurl,a_link)
            sale_id = self.url2saleid(a_link)
            event,is_new = Event.objects.get_or_create(pk=sale_id)

            if is_new:
                event.category_name = category_name
                event.sale_title = a_title.text

            event.update_time = datetime.utcnow()
            event.save()
            event_saved.send(sender=DB + '.get_brand_list', site=DB, key=sale_id, is_new=is_new, is_updated=not is_new)
            result.append(a_url)

        return result

    def crawl_product_list(self,sale_id,event_url):
        self.browser.get(event_url)
        result = []
        nodes = self.browser.find_elements_by_xpath('//div[@id="productGrid"]/article"]')
        for node in nodes:
            a = node.fid_elements_by_xpath('./div/a')
            title = a.txt
            href = a.get_attribute('href')
            url = os.path.join(self.siteurl,href)
            product_id = self.url2product_id(url)
            strike_price = node.find_elements_by_xpath('./div/span[@class="strikePrice"]').text
            product_price = node.find_elements_by_xpath('./div/span[@class="productPrice"]').text
            
            # get base product info
            product,is_new = Product.objects.get_or_create(pk=product_id)
            if is_new:
                product.url = url

            product.updated = True
            product.title = title
            product.price = product_price
            product.list_price = strike_price
            product.sale_id = sale_id
            product.save()
            result.append((product_id,url))
        return result


    def url2saleid(self, url):
        """.. :py:method::

        :param url: the brand's url
        :rtype: string of sale_id
        """
        id = url.split('/')[-1]
        try:
            id = int(id)
        except:
            raise ValueError('sale id error @ url %s' %url)
        else:
            return id

    def url2product_id(self,url):
        if not url.startswith('http://'):
            raise ValueError('url is not start with http @url:%s in function `server.url2product_id`' %url)

        try:
            return url.split('/')[-3]
        except:
            raise ValueError('split url error @url:%s' %url)

    def crawl_product_detail(self,product_id,url):
        """.. :py:method::
            Got all the product information and save into the database

        :param url: product url
        """
        self.browser.get(url)
        
        image_urls = []
        for image in self.browser.find_elements_by_xpath('//div[@id="imageViews"]/img'):
            href = image.get_attribute('src')
            url = os.path.join(self.siteurl,href)
            image_urls.append(url)

        list_info = []
        for li in self.browser.find_elements_by_xpath('//section[@id="info"]/ul/li'):
            list_info.append(li.text)

        sizes = []
        for li in self.browser.find_elements_by_xpath('//div[@id="sizeOptions"]/ul/li/a'):
            sizes.append(li.text)

        price = self.browser.find_elements_by_xpath('./span[@id="salePrice"]').text
        listprice  = self.browser.find_elements_by_xpath('./span[@id="strikePrice"]').text
        _shipping = self.browser.find_elements_by_xpath('//section[@id="shipping"]/p')
        shipping = _shipping[0].text
        returns = _shipping[1].text

        span = self.browser.find_elements_by_xpath('./span[@id="inventoryAvailable"]')
        if span:
            left = span.text.split(' ')[0]
        
        product, is_new = Product.objects.get_or_create(pk=product_id)
        if is_new:
            product.returns = returns
            priduct.shipping = shipping
            product.summary = shortDesc
            product.image_urls = image_urls
            product.list_info = info_table
            if sizes: product.sizes = sizes

        product.price = price
        product.listprice = listprice
        product.shipping = shipping
        if left:product.left = left 
        product.updated = True
        product.full_update_time = datetime.utcnow()
        product.save()
        
        product_saved.send(sender=DB + '.parse_product_detail', site=DB, key=casin, is_new=is_new, is_updated=not is_new)

if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
    server.run()