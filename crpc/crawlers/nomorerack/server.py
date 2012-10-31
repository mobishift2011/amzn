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
from crawlers.common.baseserver import BaseServer

from selenium.common.exceptions import *
from crawlers.common.events import category_saved, category_failed, category_deleted
from crawlers.common.events import product_saved, product_failed, product_deleted

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *
import urllib
import lxml.html
import time
import datetime
import re

class Server(BaseServer):
    """.. :py:class:: Server
    This is zeroRPC server class for ec2 instance to crawl pages.
    """
    
    def __init__(self):
        self.siteurl = 'http://www.nomorerack.com'
        self.site ='nomorerack'
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

    def crawl_category(self,ctx=False):
        """.. :py:method::
            From top depts, get all the events
        """
        ###########################
        # section 1, parse events
        ###########################
        self.bopen(self.siteurl)
        for e in self.browser.find_elements_by_css_selector('div.event'):
            title = e.text
            if title == 'VIEW EVENT':
                continue

            a =  e.find_element_by_css_selector('div.image a.image_tag')
            expires_on = e.find_element_by_css_selector('div.countdown').get_attribute('expires_on')
            date_obj = datetime.datetime.fromtimestamp(int(expires_on[:10]))
            href = a.get_attribute('href')
            url = self.format_url(href)
            sale_id = self.url2sale_id(url) # return a string
            img_url = 'http://nmr.allcdn.net/images/events/all/banners/event-%s-medium.jpg' %sale_id
            event ,is_new = Event.objects.get_or_create(sale_id=sale_id)
            event.title = title
            event.image_urls = [img_url]
            event.events_end = date_obj
            event.save()
            if ctx:
                ctx.send(sender=DB + '.crawl_category1', site=DB, key=sale_id, is_new=is_new, is_updated=not is_new)

        ###########################
        # section 2, parse category
        ###########################
        categorys = ['women','men','home','electronics','kids','lifestyle']
        for name in categorys:
            url = 'http://nomorerack.com/daily_deals/category/%s' %name
            category ,is_new = Category.objects.get_or_create(key=name)
            category_saved.send(sender=DB + '.crawl_category2', site=DB, key=name, is_new=is_new, is_updated=not is_new)

    def url2product_id(self,url):
        m = re.compile(r'^http://nomorerack.com/daily_deals/view/(\d+)-').findall(url)
        return m[0]
    
    def crawl_listing(self,url):
        self.bopen(url)
        main = self.browser.find_element_by_xpath('//div[@class="raw_grid deals events_page"]')
        for item in main.find_elements_by_css_selector('div.deal'):
            title = item.find_element_by_css_selector('p').text
            price = item.find_element_by_css_selector('div.pricing ins').text
            listprice = item.find_element_by_css_selector('div.pricing del').text
            href = item.find_element_by_css_selector('div.image a').get_attribute('href')
            item_url = self.format_url(href)
            key = self.url2product_id(item_url)
            print 'local',locals()
        pass

    def crawl_product(self,url):
        """.. :py:method::
            Got all the product basic information and save into the database
        """
        pass


if __name__ == '__main__':
    server = Server()
    import time
    #server.crawl_category()
    if 0:
        for event in Event.objects.all():
            url = event.url()
            server.crawl_lisging(url)

    if 1:
        url = 'http://nomorerack.com/events/view/1041'
        server.crawl_listing(url)
