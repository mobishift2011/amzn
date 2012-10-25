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

import os
import zerorpc
from selenium import webdriver
from selenium.common.exceptions import *
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support.ui import WebDriverWait
#selenium.webdriver.support.wait.POLL_FREQUENCY = 0.05

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *
import datetime

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

        self.browser.implicitly_wait(2)
        self.browser.get(self.siteurl)
        
        # click the login link
        node = self.browser.find_element_by_id('pendingTab')
        node.click()

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

    def check_signin(self):
        if not self._signin:
            self.login(self.email, self.passwd)

    def crawl_category(self,target_categorys=[]):
        """.. :py:method::
            From top depts, get all the events
        """
        categorys = target_categorys or ['women', 'men', 'living','kids','todays-fix']
        debug_info.send(sender=DB + '.category.begin')

        product_count = 0
        event_count = 0

        for category in categorys:
            url = 'http://www.ruelala.com/category/%s' %category
            self.event_list += self._get_event_list(category,url)

        while self.event_list:
            event = self.event_list.pop(0)
            sale_id =  event[0]
            event_url =  event[1]
            event_count += 1
            print '>>event count',event_count
            result = self._get_product_list(sale_id,event_url)
            if len(result) == 0:
                print '>>empty product in event ',event_url
            self.product_list +=  result
            product_count += len(result)
            print '>>product count',product_count


        while self.product_list:
            product = self.product_list.pop(0)
            product_id = product[0]
            product_url = product[1]
            self._crawl_product_detail(product_id,product_url)

        debug_info.send(sender=DB + '.category.end')

    def crawl_listing(self,sale_id,event_url):
        event_list = [(sale_id,event_url)]
        while event_list:
            event = event_list.pop()
            sale_id =  event[0]
            event_url =  event[1]
            self._get_product_list(sale_id,event_url)
        return

    def crawl_product(self,product_id,product_url):
        product_list = [(product_id,product_url)]
        for product in product_list:
            product_id = product[0]
            product_url = product[1]
            self._crawl_product_detail(product_id,product_url)
        return

    def _get_event_list(self,category_name,url):
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
            return '%s' %date

        result = []
        try:
            self.browser.get(url)
        except TimeoutException:
            print 'time out url:',url
            return  result

        try:
            span = self.browser.find_element_by_xpath('//span[@class="viewAll"]')
        except:
            pass
        else:
            span.click()

        nodes = []
        if not nodes:
            nodes = self.browser.find_elements_by_xpath('//section[@id="alsoOnDoors"]/article')

        for node in nodes:
            # pass the hiden element
            if not node.is_displayed():
                continue

            a_title = node.find_element_by_xpath('./footer/a[@class="eventDoorLink centerMe eventDoorContent"]/div[@class="eventName"]')
            if not a_title:
                continue

            footer =  node.find_element_by_xpath('./footer')
            clock = footer.find_element_by_xpath('./a/div[@class="closing clock"]').text
            try:
                end_time = get_end_time(clock)
            except ValueError:
                pass
            else:
                event.end_time = end_time

            #image = node.find_element_by_xpath('./a/img').get_attribute('src')
            a_link = node.find_element_by_xpath('./a[@class="eventDoorLink"]').get_attribute('href')
            a_url = self.format_url(a_link)
            sale_id = self._url2saleid(a_link)
            event,is_new = Event.objects.get_or_create(sale_id=sale_id)
            if is_new:
                event.img_url= 'http://www.ruelala.com/images/content/events/%s_doormini.jpg' %sale_id
                event.category_name = category_name
                event.sale_title = a_title.text

            event.update_time = datetime.datetime.utcnow()
            event.save()
            category_saved.send(sender=DB + '._get_event_list', site=DB, key=sale_id, is_new=is_new, is_updated=not is_new)
            result.append((sale_id,a_url))

        return result

    def _get_product_list(self,sale_id,event_url):
        result = []
        try:
            self.browser.get(event_url)
        except TimeoutException:
            print 'time out url:',event_url
            return  result

        try:
            span = self.browser.find_element_by_xpath('//span[@class="viewAll"]')
        except:
            pass
        else:
            try:
                span.click()
            except selenium.common.exceptions.WebDriverException:
                # just have 1 page
                pass

        nodes = []
        if not nodes:
            nodes = self.browser.find_elements_by_xpath('//article[@class="product"]')
        if not nodes:
            nodes = self.browser.find_elements_by_xpath('//article[@class="column eventDoor halfDoor grid-one-third alpha"]')

        if not nodes:

            """
            patch:
            some event url (like:http://www.ruelala.com/event/57961) will 301 redirect to product detail page:
            http://www.ruelala.com/product/detail/eventId/57961/styleNum/4112913877/viewAll/0
            """
            url_301 = self.browser.current_url
            if url_301 <>  event_url:
                self.product_list.append(url_301)
            else:
                raise ValueError('can not find product @url:%s sale id:%s' %(event_url,sale_id))

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

            try:
                s = node.find_elements_by_tag_name('span')[1]
            except IndexError:
                pass
            else:
                if s.get_attribute('class') == 'soldOutOverlay swiEnabled':
                    product.sold_out = True

            product.updated = True
            product.title = title
            product.price = str(product_price)
            product.list_price = str(strike_price)
            product.sale_id = str(sale_id)
            product.save()
            result.append((product_id,url))
        return result

    def _crawl_product_detail(self,product_id,url):
        """.. :py:method::
            Got all the product basic information and save into the database
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
        server.crawl_category(['women'])

