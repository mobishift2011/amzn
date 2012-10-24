#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.ruelala.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""
from selenium.webdriver.common.action_chains import ActionChains
from gevent import monkey
monkey.patch_all()
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
import logging
#import selenium
#selenium.webdriver.support.wait.POLL_FREQUENCY = 0.05

class Server:
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """

    def __init__(self):
        self.siteurl = 'http://www.ruelala.com'
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
            self.browser.set_page_load_timeout(10)
            #self.profile = webdriver.FirefoxProfile()
            #self.profile.set_preference("general.useragent.override","Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3")

        self.browser.implicitly_wait(2)
        self.browser.get(self.siteurl)
        
        # click the login link
        node = self.browser.find_element_by_id('pendingTab')
        debug_info.send('debug: get node %s' %node)
        node.click()
        debug_info.send('debug: click node %s' %node)

        a = self.browser.find_element_by_id('txtEmailLogin')
        a.click()
        #a.execute_script("$('#textEmailLogin').val('fuck'))")
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

    def check_signin(self):
        if not self._signin:
            self.login(self.email, self.passwd)

    def crawl(self,target_categorys=[]):
        """.. :py:method::
            From top depts, get all the brands
        """
        categorys = target_categorys or ['women', 'men', 'living','kids','todays-fix']
        debug_info.send(sender=DB + '.category.begin')
        product_count = 0

        for category in categorys:
            url = 'http://www.ruelala.com/category/%s' %category
            event_list = self.get_event_list(category,url)

            for event in event_list:
                sale_id =  event[0]
                event_url =  event[1]
                product_list = self.get_product_list(sale_id,event_url)

                for product in product_list:
                    product_id = product[0]
                    product_url = product[1]
                    self.crawl_product_detail(product_id,product_url)
                    product_count += 1

        print '>>>>>>>>>>>>>>>>>>>count:',product_count
        debug_info.send(sender=DB + '.category.end')

    def get_event_list(self,category_name,url):
        """.. :py:method::
            Get all the brands from brand list.
            Brand have a list of product.

        :param dept: dept in the page
        :param url: the dept's url
        """
        self.browser.get(url)
        result = []
        nodes = self.browser.find_elements_by_xpath('//section[@id="alsoOnDoors"]/article')
        for node in nodes:
            image = node.find_element_by_xpath('./a/img').get_attribute('src')
            a_title = node.find_element_by_xpath('./footer/a[@class="eventDoorLink centerMe eventDoorContent"]/div[@class="eventName"]')
            a_link = node.find_element_by_xpath('./a[@class="eventDoorLink"]').get_attribute('href')
            a_url = self.format_url(a_link)
            sale_id = self.url2saleid(a_link)
            event,is_new = Event.objects.get_or_create(sale_id=sale_id)

            if is_new:
                event.category_name = category_name
                event.sale_title = a_title.text

            event.update_time = datetime.utcnow()
            event.save()
            #event_saved.send(sender=DB + '.get_brand_list', site=DB, key=sale_id, is_new=is_new, is_updated=not is_new)
            result.append((sale_id,a_url))

        return result

    def format_url(self,url):
        if url.startswith('http://'):
            return url
        else:
            return os.path.join(self.site_url,url)

    def get_product_list(self,sale_id,event_url):
        self.browser.get(event_url)
        try:
            span = self.browser.find_element_by_xpath('//span[@class="viewAll"]')
        except:
            pass
        else:
            span.click()

        result = []
        nodes = self.browser.find_elements_by_xpath('//article[@class="product"]')
        print 'nodes',nodes
        if not nodes:
            raise ValueError('can not find product @url:%s sale id:%s' %(event_url,sale_id))

        for node in nodes:
            if not node.is_displayed():
                continue
            print 'node .text',node.text
            a = node.find_element_by_xpath('./a')
            img = node.find_element_by_xpath('./a/img')
            title = img.get_attribute('alt')
            href = a.get_attribute('href')
            url = self.format_url(href)
            product_id = self.url2product_id(url)
            strike_price = node.find_element_by_xpath('./div/span[@class="strikePrice"]').text
            product_price = node.find_element_by_xpath('./div/span[@class="productPrice"]').text
            print 'node a',a
            print 'title',title
            print 'href',href
            print 'url',url
            print 'product id',product_id,type(product_id)
            print 'x price',strike_price
            print 'price',product_price
            # get base product info
            product,is_new = Product.objects.get_or_create(key=str(product_id))
            #product.key = product_id
            if not is_new:
                product.url = url

            product.updated = True
            product.title = str(title)
            product.price = str(product_price)
            product.list_price = str(strike_price)
            product.sale_id = str(sale_id)
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
            id = str(id)
        except:
            raise ValueError('sale id error @ url %s' %url)
        else:
            return id

    def url2product_id(self,url):
        if not url.startswith('http://'):
            raise ValueError('url is not start with http @url:%s in function `server.url2product_id`' %url)

        try:
            id = url.split('/')[-3]
            id = str(id)
            return id
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
        soldout_size = []
        for a in self.browser.find_elements_by_xpath('//ul[@id="sizeSwatches"]/li/a[@class="normal"]'):
            if a.get_attribute('class') == 'normal':
                sizes.append(li.text)
            else:
                soldout_size.append(li.text)

        #price = self.browser.find_element_by_xpath('./span[@id="salePrice"]').text
        #listprice  = self.browser.find_element_by_xpath('./span[@id="strikePrice"]').text
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

        #product.price = price
        #product.listprice = listprice
        product.shipping = shipping
        if left == False:
            pass
        else:
            product.scarcity = left


        product.updated = True
        product.full_update_time = datetime.utcnow()
        product.save()
        print 'size',sizes
        print 'shipping',shipping
        print 'returns',returns
        print 'left',left
        print 'list info',list_info 
        print 'image urls',image_urls
        
        #product_saved.send(sender=DB + '.parse_product_detail', site=DB, key=casin, is_new=is_new, is_updated=not is_new)

if __name__ == '__main__':
    server = Server()
    if 0: 
        sale_id = '58602'
        event_url = 'http://www.ruelala.com/event/58602'
        product_list = server.get_product_list(sale_id,event_url)
        print 'result >>>>>>>>>>',len(product_list)

    if 0:
        product_id = '1411832058'
        url = 'http://www.ruelala.com/event/product/58602/1411832058/1/DEFAULT'
        result = server.crawl_product_detail(product_id,url)

    server.crawl(['women'])

    #s = server.get_product_list('58602','http://www.ruelala.com/event/58602')
    #s = server.crawl_product_detail('1411832058','http://www.ruelala.com/event/product/58602/1411832058/1/DEFAULT')
    #server.crawl()
    #server = zerorpc.Server(Server())
    #server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
    #server.run()
