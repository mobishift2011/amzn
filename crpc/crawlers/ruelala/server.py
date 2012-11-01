#!/usr/bin/env python
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

import os
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support.ui import WebDriverWait
#selenium.webdriver.support.wait.POLL_FREQUENCY = 0.05

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *
from crawlers.common.events import common_saved, common_failed
import lxml
import datetime
import time
import urllib

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

    def get(self,url):
        start = time.time()
        try:
            self.browser.get(url)
        except TimeoutException:
            print 'time out >> ',url
            return False
        else:
            print 'load page used:',time.time() - start
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
            #self.browser = webdriver.Firefox()
        except:
            #self.browser = webdriver.Firefox()
            self.browser = webdriver.Chrome()
            #self.browser.set_page_load_timeout(10)
            #self.profile = webdriver.FirefoxProfile()
            #self.profile.set_preference("general.useragent.override","Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3")

        #self.browser.implicitly_wait(1)
        self.browser.get(self.siteurl)
        time.sleep(1)
        
        # click the login link
        node = self.browser.find_element_by_id('pendingTab')
        node.click()
        time.sleep(1)

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

    def crawl_category(self,ctx=False):
        """.. :py:method::
            From top depts, get all the events
        """
        self.login(self.email, self.passwd)
        categorys = ['women', 'men', 'living','kids','todays-fix']

        for category in categorys:
            url = 'http://www.ruelala.com/category/%s' %category
            print 'go to ',url
            print 'res',self._get_event_list(category,url,ctx)

    def _get_event_list(self,category_name,url,ctx):
        """.. :py:method::
            Get all the events from event list.
        """

        def get_end_time(str):
            str =  str.replace('CLOSING IN ','').replace(' ','')
            if 'DAYS' in str:
                i = str.split('DAYS,')
            else:
                i = str.split('DAY,')

            days = int(i[0])
            j = i[1].split(':')
            hours = int(j[0])
            minutes = int(j[1])
            seconds = int(j[2])
            now = datetime.datetime.utcnow()
            delta = datetime.timedelta(days=days,hours=hours,minutes=minutes,seconds=seconds)
            date = now + delta
            return date

        result = []
        print 'go to 2',url
        self.browser.get(url)

        try:
            span = self.browser.find_element_by_xpath('//span[@class="viewAll"]')
        except:
            pass
        else:
            span.click()
            time.sleep(1)

        nodes = []
        if not nodes:
            nodes = self.browser.find_elements_by_xpath('//section[@id="alsoOnDoors"]/article')
        print 'nodes',nodes

        for node in nodes:
            # pass the hiden element
            if not node.is_displayed():
                continue

            a_title = node.find_element_by_xpath('./footer/a[@class="eventDoorLink centerMe eventDoorContent"]/div[@class="eventName"]')
            if not a_title:
                continue

            #image = node.find_element_by_xpath('./a/img').get_attribute('src')
            a_link = node.find_element_by_xpath('./a[@class="eventDoorLink"]').get_attribute('href')
            a_url = self.format_url(a_link)
            event_id = self._url2saleid(a_link)
            event,is_new = Event.objects.get_or_create(event_id=event_id)
            footer =  node.find_element_by_xpath('./footer')
            clock = footer.find_element_by_xpath('./a/div[@class="closing clock"]').text
            try:
                end_time = get_end_time(clock)
            except ValueError:
                pass
            else:
                event.events_end = end_time

            if is_new:
                event.img_url= 'http://www.ruelala.com/images/content/events/%s_doormini.jpg' %event_id
                event.dept = category_name
                event.sale_title = a_title.text
            
            event.update_time = datetime.datetime.utcnow()
            event.is_leaf = True
            event.save()
            common_saved.send(sender=ctx, site=DB, key=event_id, is_new=is_new, is_updated=not is_new)
            result.append((event_id,a_url))
        return result

    def crawl_listing(self,url,ctx):
        event_url = url
        event_id = self._url2saleid(event_url)
        self.login(self.email, self.passwd)
        result = []
        self.get(event_url)

        try:
            span = self.browser.find_element_by_xpath('//span[@class="viewAll"]')
        except:
            pass
        else:
            try:
                span.click()
                time.sleep(1)
            except selenium.common.exceptions.WebDriverException:
                # just have 1 page
                pass

        nodes = []
        if not nodes:
            nodes = self.browser.find_elements_by_xpath('//article[@class="product"]')
        if not nodes:
            nodes = self.browser.find_elements_by_xpath('//article[@class="column eventDoor halfDoor grid-one-third alpha"]')

        if not nodes:

            #patch:
            #some event url (like:http://www.ruelala.com/event/57961) will 301 redirect to product detail page:
            #http://www.ruelala.com/product/detail/eventId/57961/styleNum/4112913877/viewAll/0
            url_301 = self.browser.current_url
            if url_301 <>  event_url:
                # TODO 
                product_id = self._url2product_id(url_301)
                #self.product_list.append(url_301)
                pass
            else:
                raise ValueError('can not find product @url:%s sale id:%s' %(event_url,event_id))

        for node in nodes:
            if not node.is_displayed():
                continue
            a = node.find_element_by_xpath('./a')
            href = a.get_attribute('href')

            # patch 
            if href.split('/')[-2] == 'event':
                self.event_list.append(self.format_url(href))
                continue

            img = node.find_element_by_xpath('./a/img')
            title = img.get_attribute('alt')
            url = self.format_url(href)
            product_id = self._url2product_id(url)
            strike_price = node.find_element_by_xpath('./div/span[@class="strikePrice"]').text
            product_price = node.find_element_by_xpath('./div/span[@class="productPrice"]').text
            

            """
            print 'node a',a
            print 'title',title
            print 'href',href
            print 'url',url
            print 'product id',product_id,type(product_id)
            print 'x price',strike_price
            print 'price',product_price
            """
            # get base product info
            product,is_new = Product.objects.get_or_create(key=str(product_id))
            if not is_new:
                product.url = url
                product.event_id = [str(event_id)]

            try:
                s = node.find_elements_by_tag_name('span')[1]
            except IndexError:
                pass
            else:
                if s.get_attribute('class') == 'soldOutOverlay swiEnabled':
                    product.soldout = True

            product.updated = True
            product.title = title
            product.price = str(product_price)
            product.list_price = str(strike_price)
            if str(event_id) in product.event_id:
                pass
            else:
                product.event_id.append(str(event_id))

            product.save()
            common_saved.send(sender=ctx, site=DB, key=product.key, is_new=is_new, is_updated=not is_new)
            result.append((product_id,url))
        return result

    def _make_img_urls(slef,product_key,img_count):
        """
        the keyworld `RLLZ` in url  meaning large size(about 800*1000), `RLLD` meaning small size (about 400 *500)
        http://www.ruelala.com/images/product/131385/1313856984_RLLZ_1.jpg
        http://www.ruelala.com/images/product/131385/1313856984_RLLZ_2.jpg
        
        http://www.ruelala.com/images/product/131385/1313856984_RLLZ_1.jpg
        http://www.ruelala.com/images/product/131385/1313856984_RLLZ_2.jpg
        """
        urls = []
        prefix = 'http://www.ruelala.com/images/product/'
        for i in range(0,img_count):
            subfix = '%s/%s_RLLZ_%d.jpg'%(product_key[:6],product_key,i+1)
            url = urllib.basejoin(prefix,subfix)
            urls.append(url)
        return urls

    def crawl_product(self,url,ctx=False):
        """.. :py:method::
            Got all the product basic information and save into the database
        """
        product_id = self._url2product_id
        if not self.get(url):
            return False

        try:
            self.browser.find_element_by_css_selector('div#optionsLoadingIndicator.row')
        except:
            time.sleep(3)
        
        point1= time.time()
        image_urls = []
        # TODO imgDetail
        imgs_node = self.browser.find_element_by_css_selector('section#productImages')
        #first_img_url = imgs_node.find_element_by_css_selector('img#imgZoom').get_attribute('href')
        try:
            img_count = len(imgs_node.find_elements_by_css_selector('div#imageThumbWrapper img'))
        except:
            img_count = 1
        img_urls = self._make_img_urls(product_id,img_count)
        print 'parse img urls used',time.time() - point1
        
        point2 = time.time()
        list_info = []
        for li in self.browser.find_elements_by_css_selector('section#info ul li'):
            list_info.append(li.text)
        print 'parse list info used',time.time() - point2
        
        #########################
        # section 2 productAttributes
        #########################
        
        attribute_node = self.browser.find_elements_by_css_selector('section#productAttributes.floatLeft')[0]
        point3 = time.time()
        sizes = []
        size_list = attribute_node.find_elements_by_css_selector('ul#sizeSwatches li.swatch a.normal')
        if size_list:
            for a in size_list:
                a.click()
                key = a.text
                left = ''
                span = attribute_node.find_element_by_id('inventoryAvailable')
                left = span.text.split(' ')[0]
                sizes.append((key,left))
        else:
            left =  attribute_node.find_element_by_css_selector('span#inventoryAvailable.active').text
            sizes = [('std',left)]

        print 'parse sizes used ',time.time() - point3
        point4 = time.time()
        shipping = attribute_node.find_element_by_id('readyToShip').text
        price = attribute_node.find_element_by_id('salePrice').text
        listprice  = attribute_node.find_element_by_id('strikePrice').text
        print 'parse other userd',time.time() - point4
        
        point5 = time.time()
        product, is_new = Product.objects.get_or_create(key=str(product_id))
        if is_new:
            product.shipping = shipping
            product.image_urls = image_urls
            product.list_info = info_table

        product.sizes_scarcity = sizes
        product.price = price
        product.listprice = listprice
        product.shipping = shipping

        product.updated = True
        product.full_update_time = datetime.datetime.utcnow()
        product.save()
        print 'save data used ',time.time() - point5
        print 'parse product detail used',time.time() - point1
        common_saved.send(sender=ctx, site=DB, key=product.key, is_new=is_new, is_updated=not is_new)

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
            s = urllib.basejoin(self.siteurl,url)
            return s

if __name__ == '__main__':
    server = Server()
    if 0:
        server.crawl_category()
    if 0: 
        event_id = '59118'
        event_url ='http://www.ruelala.com/event/59118'
        product_list = server._get_product_list(sale_id,event_url)
        print 'result >>',len(product_list)
        ps =  Product.objects.all()
        print 'ps',ps

    if 0:
        product_id = '1411892550'
        url = 'http://www.ruelala.com/event/product/53652/1411892550/1/DEFAULT'
        result = server.crawl_product(product_id,url)

    if 1:
        server = Server()
        url = 'http://www.ruelala.com/event/53652'
        server.crawl_listing(url,'x')

    if 0:
        server = Server()
        product_id = '1313856978'
        url = 'http://www.ruelala.com/event/product/59326/1313856978/1/DEFAULT'
        result = server._crawl_product_detail(product_id,url)

    if 0:
        print '>>>>>>'
        category = 'women'
        server._get_event_list('women','http://www.ruelala.com/category/women')

    if 0:
        count = 0
        error_count = 0
        server = Server()
        server._get_event_list('women','http://www.ruelala.com/category/women')
        start = time.time()
        for c in Category.objects.all():
            print 'product list',server._get_product_list(c.sale_id,c.url())
        print '>>>>>>end',time.time() - start

        ps =  Product.objects.all()
        print 'ps',ps
        total = len(ps)
        start = time.time()
        for p in ps:
            print p.key
            try:
                server._crawl_product_detail(p.key,p.url())
            except:
                print 'error ',p.url()
                error_count +=1
            else:
                count += 1

            print 'key',p.key
            print 'total',total
            print 'count',count
            print 'error count',error_count
            print 'used time',time.time() - start
