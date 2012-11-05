# -*- coding: utf-8 -*-
"""
crawlers.ruelala.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""

from gevent import monkey
monkey.patch_all()
from gevent.coros import Semaphore
from crawlers.common.baseserver import BaseServer

from selenium.common.exceptions import *
from crawlers.common.events import category_saved, category_failed, category_deleted
from crawlers.common.events import product_saved, product_failed, product_deleted
from crawlers.common.events import common_saved, common_failed
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

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

    def crawl_category(self,ctx=''):
        """.. :py:method::
            From top depts, get all the events
        """
        ###########################
        # section 2, parse deal products
        ###########################
        categorys = ['women','men','home','electronics','lifestyle']
        for name in categorys:
            self._crawl_category_product(name,ctx)

        # the kids section is diffirent from others 
        self.crawl_listing('http://nomorerack.com/daily_deals/category/kids',ctx)

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
            event.update_time = datetime.datetime.utcnow()
            event.is_leaf = True
            try:
                event.save()
            except:
                common_failed.send(sender=ctx, site=DB, key=event_id, is_new=is_new, is_updated=not is_new)
            else:
                common_saved.send(sender=ctx, site=DB, key=event_id, is_new=is_new, is_updated=not is_new)

    def _crawl_category_product(self,name,ctx=''):
        _url = 'http://nomorerack.com/daily_deals/category_jxhrq/%s?sort=best_selling&offset=%d'
        for i in range(0,10000):
            if name == 'kids':
                url = 'http://nomorerack.com/daily_deals/category/kids'
            else:
                url = _url%(name,i*12)

            tree = self.ropen(url)
            try:
                divs = tree.xpath('//div[starts-with(@class,"deal")]')
            except NoSuchElementException:
                return
            
            # the cralwer at the end of list page
            if not divs:
                return False
            
            for div in  divs:
                img_url = div.xpath('.//img')[0].get('src')
                category = div.xpath('.//h4')[0].text or ''
                price = div.xpath('.//div[@class="pricing"]/ins')[0].text
                listprice = div.xpath('.//div[@class="pricing"]/del')[0].text
                href = div.xpath('.//a')[0].get('href')
                detail_url = self.format_url(href)
                title = div.xpath('.//p')[0].text
                key = self.url2product_id(detail_url)

                #for i in locals().items():
                #    print 'i',i

                product,is_new = Product.objects.get_or_create(pk=key)
                if category.upper() == 'SOLD OUT':
                    product.soldout = True
                    product.cats = [name]
                else:
                    product.cates = [name,category]
                product.image_urls = [img_url]
                product.price = price
                product.listprice = listprice
                product.title = title
                try:
                    product.save()
                except:
                    common_failed.send(sender=ctx, site=DB, key=key, is_new=is_new, is_updated=not is_new)
                else:
                    common_saved.send(sender=ctx, site=DB, key=key, is_new=is_new, is_updated=not is_new)
            
            # the kids category just have one page 
            if name == 'kids':
                return

    def url2product_id(self,url):
        m = re.compile(r'^http://(.*)nomorerack.com/daily_deals/view/(\d+)-').findall(url)[0]
        return m[-1]

    def url2event_id(self,url):
        # http://www.nomorerack.com/events/view/1018
        m = re.compile(r'^http://(.*)nomorerack.com/events/view/(\d+)').findall(url)[0]
        return m[-1]

    def make_image_urls(self,url,count):
        urls = []
        m = re.compile(r'^http://nmr.allcdn.net/images/products/(\d+)-').findall(url)
        img_id = m[0]
        for i in range(0,count):
            url = 'http://nmr.allcdn.net/images/products/%s-%d-lg.jpg' %(img_id,i)
            urls.append(url)
        return urls
    
    @exclusive_lock(DB)
    def crawl_listing(self,url,ctx=''):
        print 'to open',url
        self.bopen(url)
        try:
            main = self.browser.find_element_by_xpath('//div[@class="raw_grid deals events_page"]')
        except NoSuchElementException:
            main = self.browser.find_element_by_css_selector('div#content')
        print 'main>>>',main

        for item in main.find_elements_by_css_selector('div.deal'):
            title = item.find_element_by_css_selector('p').text
            price = item.find_element_by_css_selector('div.pricing ins').text
            listprice = item.find_element_by_css_selector('div.pricing del').text
            href = item.find_element_by_css_selector('div.image a').get_attribute('href')
            item_url = self.format_url(href)
            key = self.url2product_id(item_url)
            product ,is_new = Product.objects.get_or_create(key=key)
            product.price = price
            product.listproce = listprice
            product.title = title
            try:
                product.save()
            except:
                common_failed.send(sender=ctx, site=DB, key=key, is_new=is_new, is_updated=not is_new)
            else:
                common_saved.send(sender=ctx, site=DB, key=key, is_new=is_new, is_updated=not is_new)

    @exclusive_lock(DB)
    def crawl_product(self,url,ctx=''):
        """.. :py:method::
            Got all the product basic information and save into the database
        """
        key = self.url2product_id(url)
        product,is_new = Product.objects.get_or_create(key=key)
        self.browser.get(url)

        node = self.browser.find_element_by_css_selector('div#products_view.standard')
        dept = node.find_element_by_css_selector('div.right h5').text
        title = node.find_element_by_css_selector('div.right h2').text
        summary = node.find_element_by_css_selector('p.description').text
        thumbs = node.find_element_by_css_selector('div.thumbs')
        image_count = len(thumbs.find_elements_by_css_selector('img'))
        image_url = thumbs.find_element_by_css_selector('img').get_attribute('src')
        image_urls = self.make_image_urls(image_url,image_count)
        attributes = node.find_elements_by_css_selector('div.select-cascade select')
        sizes = []
        colors = []
        for attr in attributes:
            ops = attr.find_elements_by_css_selector('option')
            m  = ops[0].get_attribute('value')
            if m == 'Select a size':
                for op in  ops:
                    size = op.get_attribute('value')
                    sizes.append({'size':size})
            elif m == 'Select a color':
                for op in  ops:
                    colors.append(op.text)

        date_str = ''
        try:
            date_str = self.browser.find_element_by_css_selector('div.ribbon-center h4').text
        except NoSuchElementException:
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
        product.pagesize    =   sizes
        product.updated = True

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
        #        or  'This event is only live until November 2nd 11:59 AM EST'
        print 're.date str:',date_str
        m = re.compile(r'This (.*)deal is only live until (.*)$').findall(date_str)
        print 're.m',m
        str = m[0][-1]
        return dt_parser.parse(str)


if __name__ == '__main__':
    server = Server()
    import time
    if 0:
        server._crawl_category_product('kids')
    if 0:
        server.crawl_category()

    if 0:
        for event in Event.objects.all():
            url = event.url()
            server.crawl_listing(url)
    if 1:
        url = 'http://nomorerack.com/daily_deals/category/kids'
        server.crawl_listing(url)

    if 0:
        url = Product.objects.all()[10].url()
        server.crawl_product(url)
