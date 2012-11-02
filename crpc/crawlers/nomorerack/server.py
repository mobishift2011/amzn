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
from crawlers.common.events import common_saved, common_failed

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *
import urllib
import lxml.html
import time
import datetime
import re
from dateutil import parser as dt_parser

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
            event_id = self.url2event_id(url) # return a string
            img_url = 'http://nmr.allcdn.net/images/events/all/banners/event-%s-medium.jpg' %event_id
            event ,is_new = Event.objects.get_or_create(event_id=event_id)
            event.title = title
            event.image_urls = [img_url]
            event.events_end = date_obj
            event.update_time = datetime.utcnow()
            event.is_leaf = True
            try:
                event.save()
            except:
                common_failed.send(sender=ctx, site=DB, key=event_id, is_new=is_new, is_updated=not is_new)
            else:
                common_saved.send(sender=ctx, site=DB, key=event_id, is_new=is_new, is_updated=not is_new)

        ###########################
        # section 2, parse deal products
        ###########################
        categorys = ['women','men','home','electronics','kids','lifestyle']
        for name in categorys:
            url = 'http://nomorerack.com/daily_deals/category/%s' %name
            self.crawl_category_product(name,url)

    def url2product_id(self,url):
        m = re.compile(r'^http://nomorerack.com/daily_deals/view/(\d+)-').findall(url)
        return m[0]

    def url2event_id(self,url):
        m = re.compile(r'^http://nomorerack.com/events/view/(\d+)-').findall(url)
        return m[0]

    def make_image_urls(self,url,count):
        urls = []
        m = re.compile(r'^http://nmr.allcdn.net/images/products/(\d+)-').findall(url)
        img_id = m[0]
        for i in range(0,count):
            url = 'http://nmr.allcdn.net/images/products/%s-%d-lg.jpg' %(img_id,i)
            urls.append(url)
        return urls
    
    def crawl_listing(self,url,ctx=''):
        self.bopen(url)
        main = self.browser.find_element_by_xpath('//div[@class="raw_grid deals events_page"]')
        for item in main.find_elements_by_css_selector('div.deal'):
            title = item.find_element_by_css_selector('p').text
            price = item.find_element_by_css_selector('div.pricing ins').text
            listprice = item.find_element_by_css_selector('div.pricing del').text
            href = item.find_element_by_css_selector('div.image a').get_attribute('href')
            #item_url = self.format_url(href)
            key = self.url2product_id(item_url)

            product ,is_new = Product.objects.get_or_create(key=key)
            product.price = price
            product.listproce = listprice
            product.title = title
            print 'local',locals()
            try:
                product.save()
            except:
                common_failed.send(sender=ctx, site=DB, key=key, is_new=is_new, is_updated=not is_new)
            else:
                common_saved.send(sender=ctx, site=DB, key=key, is_new=is_new, is_updated=not is_new)

    def crawl_product(self,url):
        """.. :py:method::
            Got all the product basic information and save into the database
        """
        key = self.url2product_id(url)
        product,is_new = Product.objects.get_or_create(key=key)

        self.bopen(url)
        node = self.browser.find_element_by_css_selector('div#products_view.standard')
        dept = node.find_element_by_css_selector('div.right h5').text
        title = node.find_element_by_css_selector('div.right h2').text
        summary = node.find_element_by_css_selector('p.description').text
        thumbs = node.find_element_by_css_selector('div.thumbs')
        image_count = len(thumbs.find_elements_by_css_selector('img'))
        image_url = thumbs.find_element_by_css_selector('img').get_attribute('src')
        image_urls = self.make_image_urls(image_url,image_count)
        attributes = node.find_elements_by_css_selector('div.select-cascade select')
        colors = []
        for op in attributes[0].find_elements_by_css_selector('option'):
            if not op.get_attribute('value'):
                continue
            else:
                colors.append(op.text)

        sizes = []
        for op in attributes[1].find_elements_by_css_selector('option'):
            size = op.text
            if not op.get_attribute('value'):
                continue
            else:
                sizes.append({size:''})
        date_str = self.browser.find_element_by_css_selector('div.ribbon-center p').text
        date_obj = self.format_date_str(date_str)
        price = node.find_element_by_css_selector('div.standard h3 span')
        listprice = node.find_element_by_css_selector('div.standard p del')

        product.summary = summary
        product.title = title
        product.dept = dept
        product.image_urls = image_urls
        product.end_time = date_obj
        product.price = price
        product.listprice = listprice

        try:
            product.save()
        except:
            common_failed.send(sender=ctx, site=DB, key=product.key, is_new=is_new, is_updated=not is_new)
        else:
            common_saved.send(sender=ctx, site=DB, key=product.key, is_new=is_new, is_updated=not is_new)

        for i in locals().items():
            print 'i',i

        return


    def format_date_str(self,date_str):
        """ translate the string to datetime object """

        # date_str = 'This deal is only live until November 2nd 11:59 AM EST'
        m = re.compile(r'^This deal is only live until (November 2nd 11:59 AM EST)$').findall(date_str)
        str = m[0]
        return dt_parser.parse(str)


if __name__ == '__main__':
    server = Server()
    import time
    if 1:
        server.crawl_category()

    if 0:
        for event in Event.objects.all():
            url = event.url()
            server.crawl_lisging(url)
    if 0:
        url = 'http://nomorerack.com/events/view/1041'
        server.crawl_listing(url)

    if 0:
        url = Product.objects.all()[10].url()
        server.crawl_product(url)
