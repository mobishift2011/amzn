#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.myhabit.server
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


    def crawl_category(self):
        """.. :py:method::
            From top depts, get all the brands
        """
        depts = ['women', 'men', 'kids', 'home', 'designer']
        self.queue = Queue.Queue()
        debug_info.send(sender=DB + '.category.begin')

        for dept in depts:
            link = 'http://www.myhabit.com/homepage?#page=g&dept={0}&ref=qd_nav_tab_{0}'.format(dept)
            self.get_brand_list(dept, link)
        self.cycle_crawl_category()
        debug_info.send(sender=DB + '.category.end')

    def get_brand_list(self, dept, url):
        """.. :py:method::
            Get all the brands from brand list.
            Brand have a list of product.

        :param dept: dept in the page
        :param url: the dept's url
        """
        # TODO: upcoming events
        self.browser.get(url)
        nodes = self.browser.find_elements_by_xpath('//div[@id="main"]/div[@id="page-content"]/div[@id="currentSales"]/div[starts-with(@id, "privateSale")]/div[@class="caption"]/a')
        for node in nodes:
            try: # if can't be found, cost a long time and raise NoSuchElementException
                node.find_element_by_xpath('./div[@class="image"]/a/div[@class="soldout"]')
            except:
                soldout = False
            else:
                soldout = True
            image = node.find_element_by_xpath('./div[@class="image"]/a/img').get_attribute('src')
            a_title = node.find_element_by_xpath('./div[@class="caption"]/a')
            l = a_title.get_attribute('href')
            link = l if l.startswith('http') else 'http://www.myhabit.com/homepage' + l
            sale_id = self.url2saleid(link)

            brand, is_new = Category.objects.get_or_create(pk=sale_id)
            if is_new:
                brand.dept = dept
                brand.sale_title = a_title.text
                brand.image_url = image
            brand.soldout = soldout
            brand.save()
            category_saved.send(sender=DB + '.get_brand_list', site=DB, key=sale_id, is_new=is_new, is_updated=not is_new)

            self.queue.put( (dept, link) )

    def url2saleid(self, url):
        """.. :py:method::

        :param url: the brand's url
        :rtype: string of sale_id
        """
        return re.compile(r'http://www.myhabit.com/homepage\??#page=b&dept=\w+&sale=(\w+)').match(url).group(1)

    def url2asin(self, url):
        """.. :py:method::

        :param url: the product's url
        :rtype: string of asin, cAsin
        """
        return re.compile(r'http://www.myhabit.com/homepage\??#page=d&dept=\w+&sale=\w+&asin=(\w+)&cAsin=(\w+)').match(url).groups()

    def cycle_crawl_category(self, timeover=60):
        """.. :py:method::
            read (category, link) tuple from queue, crawl sub-category, insert into the queue

        :param timeover: timeout in queue.get
        """
        while not self.queue.empty():
            try:
                job = self.queue.get(timeout=timeover)
                self.browser.get(job[1])
                self.parse_category(job[0], job[1])
            except Queue.Empty:
                debug_info.send(sender="{0}.category:Queue waiting {1} seconds without response!".format(DB, timeover))
            except:
                debug_info.send(sender=DB + ".category", tracebackinfo=sys.exc_info())


    def time_proc(self, time_str):
        """.. :py:method::

        :param time_str: u'SAT OCT 20 9 AM '
        :rtype: datetime type utc time
        """
        pt = pytz.timezone('US/Pacific')
        tinfo = time_str + str(pt.normalize(datetime.now(tz=pt)).year)
        endtime = datetime.strptime(tinfo, '%a %b %d %I %p %Y').replace(tzinfo=pt)
        return pt.normalize(endtime).astimezone(pytz.utc)
    
    def parse_category(self, dept, url):
        """.. :py:method::
            Brand page parsing

        :param dept: dept in the page
        :param url: url in the page
        """
        try:
            node = self.browser.find_elements_by_xpath('//div[@id="main"]/div[@id="page-content"]/div/div[@id="top"]/div[@id="salePageDescription"]')
        except:
            category_failed.send(sender=DB + '.brand_page', site=DB, url=url, reason='Url can not be parsed.')
            return

        sale_title = node[0].find_element_by_xpath('./div[@id="saleTitle"]').text
        sale_description = node[0].find_element_by_xpath('./div[@id="saleDescription"]').text
        end_date = node[0].find_element_by_xpath('./div[@id="saleEndTime"]/span[@class="date"]').text # SAT OCT 20
        end_time = node[0].find_element_by_xpath('./div[@id="saleEndTime"]/span[@class="time"]').text # 9 AM PT
        utc_endtime = self.time_proc(end_date + ' ' + end_time.replace('PT', ''))
        try:
            sale_brand_link = node[0].find_element_by_xpath('./div[@id="saleBrandLink"]/a').get_attribute('href')
        except:
            sale_brand_link = ''
        num = node[0].find_element_by_xpath('../../div[@id="middle"]/div[@id="middleCenter"]/div[@id="numResults"]').text
        num = int(num.split()[0])
        sale_id = self.url2saleid(url)

        brand, is_new = Category.objects.get_or_create(pk=sale_id)
        # crawl infor before, so always not new
        brand.sale_description = sale_description
        brand.events_end = utc_endtime
        if sale_brand_link: brand.brand_link = sale_brand_link
        brand.num = num
        brand.update_time = datetime.utcnow()
        brand.save()
        category_saved.send(sender=DB + '.parse_category', site=DB, key=sale_id, is_new=is_new, is_updated=not is_new)

        elements = node[0].find_elements_by_xpath('../../div[@id="asinbox"]/ul/li[starts-with(@id, "result_")]')
        for ele in elements:
            self.parse_category_product(ele, sale_title)


    def parse_category_product(self, element, sale_title):
        """.. :py:method::
            Brand page, product parsing

        :param element: product's xpath element
        :param sale_title: as brand pass to product
        """
        try:
            element.find_element_by_class_name('soldout')
        except:
            soldout = False
        else: soldout = True
        l = element.find_element_by_class_name('evt-prdtDesc-a').get_attribute('href')
        link = l if l startswith('http') else 'http://www.myhabit.com/homepage' + l
        title = element.find_element_by_class_name('title').text
        listprice = element.find_element_by_class_name('listprice').text.replace('$', '').replace(',', '')
        ourprice = element.find_element_by_class_name('ourprice').text.replace('$', '').replace(',', '')
#        img = element.find_element_by_class_name('iImg').get_attribute('src')

        asin, casin = self.url2asin(link)
        product, is_new = Product.objects.get_or_create(pk=casin)
        if is_new:
            product.dept = dept
            product.sale_id = sale_id
            product.brand = sale_title
            product.asin = asin
            product.title = title
        product.price = ourprice
        product.listprice = listprice
        product.soldout = soldout
        product.updated = False
        product.list_update_time = datetime.utcnow()
        product.save()
        product_saved.send(sender=DB + '.parse_category', site=DB, key=casin, is_new=is_new, is_updated=not is_new)


    def crawl_listing(self):
        """.. :py:method::
            not implement
        """
        pass

    def crawl_product(self, url, casin):
        """.. :py:method::
            Got all the product information and save into the database

        :param url: product url
        """
        self.browser.get(url)
        node = self.browser.find_element_by_xpath('//div[@id="main"]/div[@id="page-content"]/div[@id="detail-page"]/div[@id="dpLeftCol"]')
        shortDesc = node.find_element_by_class_name('shortDesc').text

        international_shipping = node.find_element_by_id('intlShippableBullet').text
        returned = node.find_element_by_id('returnPolicyBullet').text

        already_have = [shortDesc, internaltional_shipping, returned]
        bullets = node.find_elements_by_tag_name('li')
        info_table = []
        for bullet in bullets:
            if bullet.text and bullet.text not in already_have:
                info_table.append(bullet.text)

        image_urls = []
        video = ''
        imgs = node.find_elements_by_xpath('.//div[@id="altImgContainer"]/div')
        for img in imgs:
            try:
                picture = img.find_element_by_class_name('zoomImageL2').get_attribute('value')
                image_urls.append(picture)
            except:
                video = img.find_element_by_class_name('videoURL').get_attribute('value')


        right_col = node.find_element_by_xpath('../div[@id="dpRightCol"]/div[@id="innerRightCol"]')
        try:
            color = right_col.find_element_by_xpath('.//div[@class="dimensionAltText variationSelectOn"]').text
        except:
            color = ''
        try:
            sizes = right_col.find_elements_by_xpath('./div[@id="dpVariationMatrix"]//select[@class="variationDropdown"]/option')
            size = [s for s in sizes if not s.text.startswith('Please')]
        except:
            sizes = [] 

        listprice = right_col.find_element_by_id('listPrice').text.replace('$', '').replace(',', '')
        ourprice = right_col.find_element_by_id('ourPrice').text.replace('$', '').replace(',', '')
        scarcity = right_col.find_element_by_id('scarcity').text
        shipping = '; '.join( [a.text for a in right_col.find_elements_by_class_name('dpRightColLabel') if a.text] )

        product, is_new = Product.objects.get_or_create(pk=casin)
        if is_new:
            product.summary = shortDesc
            product.image_urls = image_urls
            product.list_info = info_table
            if video: product.video = video
            if color: product.color = color
            if sizes: product.sizes = sizes
            if international_shipping: product.international_shipping = international_shipping
            if returned: product.returned = returned
        product.price = ourprice
        product.listprice = listprice
        product.shipping = shipping
        if scarcity: product.scarcity = scarcity
        product.updated = True
        product.full_update_time = datetime.utcnow()
        product.save()
        
        product_saved.send(sender=DB + '.parse_product_detail', site=DB, key=casin, is_new=is_new, is_updated=not is_new)

        

if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
    server.run()
