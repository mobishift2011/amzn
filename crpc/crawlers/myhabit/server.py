#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.myhabit.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""
import os
import re
import sys
import time
import Queue
import zerorpc
import lxml.html
import pytz

from urllib import quote, unquote
from datetime import datetime
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.action_chains import ActionChains

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *

TIMEOUT = 5

class Server:
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    def __init__(self):
        self.siteurl = 'http://www.myhabit.com'
        self._signin = False
#        webdriver.support.wait.POLL_FREQUENCY = 0.05

    def login(self):
        """.. :py:method::
            login myhabit
            Using Firefox will cause Xvfb memory leaf and program broke.

        """
        self.browser = webdriver.Chrome()
#        self.browser.set_page_load_timeout(5)
#        self.browser.implicitly_wait(1)
        self.download_page('http://www.myhabit.com/my-account')

    def fill_login_form(self):
        """.. :py:method:
            fill in login form when firefox driver is open
        """
        self.browser.find_element_by_id('ap_email').send_keys(login_email)
        self.browser.find_element_by_id('ap_password').send_keys(login_passwd)
        self.browser.find_element_by_id('signInSubmit').submit()
        self._signin = True

    def check_signin(self):
        if not self._signin:
            self.login()

    def close_browser(self):
        """
            close the webdriver browser
        """
        self.browser.quit()
        self._signin = False

    def download_page(self, url):
        """.. :py:method::
            download the url
        :param url: the url need to download
        """
        time_begin_benchmark = time.time()
        try:
            self.browser.get(url)
            if self.browser.title == u'Amazon.com Sign In':
                self.fill_login_form()
            WebDriverWait(self.browser, TIMEOUT, 0.05).until(lambda driver: driver.find_element_by_css_selector('div#body div#main div#page-content div#bottom-content'))
        except selenium.common.exceptions.TimeoutException:
            try:
                WebDriverWait(self.browser, TIMEOUT, 0.05).until(lambda driver: driver.execute_script('return $.active') == 0)
            except selenium.common.exceptions.TimeoutException:
                print 'Timeout --> {0}'.format(url)
                return 1
        print 'time download benchmark: ', time.time() - time_begin_benchmark

    def download_page_for_product(self, url):
        time_begin_benchmark = time.time()
        try:
            self.browser.get(url)
            if self.browser.title == u'Amazon.com Sign In':
                self.fill_login_form()
            WebDriverWait(self.browser, TIMEOUT, 0.05).until(lambda driver: driver.execute_script('return $.active') == 0)
        except selenium.common.exceptions.TimeoutException:
            print 'Timeout --> {0}'.format(url)
            return 1
        print 'time download benchmark: ', time.time() - time_begin_benchmark



    @exclusive_lock(DB)
    def crawl_category(self, ctx):
        """.. :py:method::
            From top depts, get all the brands
        """
        self.check_signin()
        depts = ['women', 'men', 'kids', 'home', 'designer']
        self.upcoming_queue = Queue.Queue()
        debug_info.send(sender=DB + '.category.begin')

        for dept in depts:
            link = 'http://www.myhabit.com/homepage?#page=g&dept={0}&ref=qd_nav_tab_{0}'.format(dept)
            self.get_event_list(dept, link, ctx)
        self.cycle_crawl_category(ctx)
        
        self.close_browser()
        debug_info.send(sender=DB + '.category.end')

    def get_event_list(self, dept, url, ctx):
        """.. :py:method::
            Get all the brands from brand list.
            Brand have a list of product.

        :param dept: dept in the page
        :param url: the dept's url
        """
        self.download_page_for_product(url)
        nodes = self.browser.find_elements_by_xpath('//div[@id="main"]/div[@id="page-content"]/div[@id="currentSales"]/div[starts-with(@id, "privateSale")]')
        for node in nodes:
            a_title = node.find_element_by_xpath('./div[@class="caption"]/a')
            l = a_title.get_attribute('href')
            link = l if l.startswith('http') else 'http://www.myhabit.com/homepage' + l
            event_id = self.url2saleid(link)

            image = node.find_element_by_xpath('./div[@class="image"]/a/img').get_attribute('src')
            try: # if can't be found, cost a long time and raise NoSuchElementException
                node.find_element_by_xpath('./div[@class="image"]/a/div[@class="soldout"]')
            except:
                soldout = False
            else:
                soldout = True

            brand, is_new = Event.objects.get_or_create(event_id=event_id)
            is_updated = False
            if is_new:
                brand.sale_title = a_title.text
                brand.image_urls = [image]
                if soldout == True: product.soldout = True
            else:
                if soldout == True and product.soldout != True:
                    product.soldout = soldout
                    is_updated = True
            if dept not in brand.dept: brand.dept.append(dept) # for designer dept
            brand.update_time = datetime.utcnow()
            brand.is_leaf = True
            brand.save()
            common_saved.send(sender=ctx, key=event_id, url=url, is_new=is_new, is_updated=is_updated)

        # upcoming brand
        nodes = self.browser.find_elements_by_xpath('//div[@id="main"]/div[@id="page-content"]/div[@id="upcomingSales"]//div[@class="fourColumnSales"]//div[@class="caption"]/a')
        for node in nodes:
            l = node.get_attribute('href')
            link = l if l.startswith('http') else 'http://www.myhabit.com/homepage' + l 
#            title = node.text
            self.upcoming_queue.put( (dept, link) )

    def cycle_crawl_category(self, ctx, timeover=30):
        """.. :py:method::
            read (category, link) tuple from queue, crawl sub-category, insert into the queue
            get queue and parse the brand page

        :param timeover: timeout in queue.get
        """
        debug_info.send(sender='{0}.cycle_crawl_category.begin:queue size {1}'.format(DB, self.upcoming_queue.qsize()))
        while not self.upcoming_queue.empty():
#            try:
            job = self.upcoming_queue.get(timeout=timeover)
            if self.download_page(job[1]) == 1:
                continue
            self.parse_upcoming(job[0], job[1], ctx)
#            except Queue.Empty:
#                debug_info.send(sender="{0}.category:Queue waiting {1} seconds without response!".format(DB, timeover))
#            except:
#                debug_info.send(sender=DB + ".category", tracebackinfo=sys.exc_info())
        debug_info.send(sender=DB + '.cycle_crawl_category.end')

    def parse_upcoming(self, dept, url, ctx):
        """.. :py:method::
            upcoming brand page parsing
            upcoming brand also have duplicate designer

        :param dept: dept in the page
        :param url: url in the page
        """
        event_id = self.url2saleid(url)
        brand, is_new = Event.objects.get_or_create(event_id=event_id)
        if is_new:
            path = self.browser.find_element_by_css_selector('div#main div#page-content div#top-content')
            if path == []:
                # sleep 2 second, can not be any faster.
                time.sleep(2)
                path = self.browser.find_element_by_css_selector('div#main div#page-content div#top-content')
#            except selenium.common.exceptions.NoSuchElementException:
            try:
                begin_date = path.find_element_by_css_selector('div#startHeader span.date').text # SAT OCT 20
            except selenium.common.exceptions.NoSuchElementException:
                print 'No such element in begin_date',
                time.sleep(2)
                path = self.browser.find_element_by_css_selector('div#main div#page-content div#top-content')
                print path
                begin_date = path.find_element_by_css_selector('div#startHeader span.date').text # SAT OCT 20
            begin_time = path.find_element_by_xpath('./div[@id="startHeader"]/span[@class="time"]').text # 9 AM PT
            utc_begintime = time_convert(begin_date + ' ' + begin_time.replace('PT', ''), '%a %b %d %I %p %Y') #u'SAT OCT 20 9 AM '
            brand_info = path.find_element_by_id('upcomingSaleBlurb').text
            img = path.find_element_by_xpath('./div[@class="upcomingSaleHero"]/div[@class="image"]/img').get_attribute('src')
            sale_title = path.find_element_by_xpath('./div[@class="upcomingSaleHero"]/div[@class="image"]/img').get_attribute('alt')
            subs = []
            for sub in path.find_elements_by_xpath('./div[@id="asinbox"]/ul/li'):
                sub_title = sub.find_element_by_class_name('title').text
                sub_img = sub.find_element_by_xpath('./img').get_attribute('src')
                subs.append([sub_title, sub_img])

            brand.dept = [dept]
            brand.sale_title = sale_title
            brand.image_urls = [img]
            brand.events_begin = utc_begintime
            brand.sale_description = brand_info
            brand.upcoming_title_img = subs
            brand.update_time = datetime.utcnow()
        else:
            if dept not in brand.dept: brand.dept.append(dept)
        brand.save()
        common_saved.send(sender=ctx, key=event_id, url=url, is_new=is_new, is_updated=False)


        

    def url2saleid(self, url):
        """.. :py:method::

        :param url: the brand's url
        :rtype: string of event_id
        """
        return re.compile(r'http://www.myhabit.com/homepage\??#page=b&dept=\w+&sale=(\w+)').match(url).group(1)

    def url2asin(self, url):
        """.. :py:method::

        :param url: the product's url
        :rtype: string of asin, cAsin
        """
        m = re.compile(r'http://www.myhabit.com/homepage.*#page=d&dept=\w+&sale=\w+&asin=(\w+)&cAsin=(\w+)').match(url)
        if not m: print 'Can not parse detail product url: ', url
        return m.groups()
    

    @exclusive_lock(DB)
    def crawl_listing(self, url, ctx):
        """.. :py:method::
            Brand page parsing

        :param url: url in the page
        """
        self.check_signin()
        if self.download_page(url) == 1: return
        time_begin_benchmark = time.time()
#        node = self.browser.find_element_by_xpath('//div[@id="main"]/div[@id="page-content"]/div/div[@id="top"]/div[@id="salePageDescription"]')
        node = self.browser.find_element_by_css_selector('div#main div#page-content div')
        if node == []:
            time.sleep(0.5)
            node = self.browser.find_element_by_css_selector('div#main div#page-content div')

        sale_title = node.find_element_by_css_selector('div#top div#saleTitle').text
        sale_description = node.find_element_by_css_selector('div#top div#saleDescription').text
        end_date = node.find_element_by_css_selector('div#top div#saleEndTime span.date').text # SAT OCT 20
        end_time = node.find_element_by_css_selector('div#top div#saleEndTime span.time').text # 9 AM PT
        utc_endtime = time_convert(end_date + ' ' + end_time.replace('PT', ''), '%a %b %d %I %p %Y') #u'SAT OCT 20 9 AM '
        try:
            sale_brand_link = node.find_element_by_xpath('.//div[@id="saleBrandLink"]/a').get_attribute('href')
        except:
            sale_brand_link = ''
        num = node.find_element_by_css_selector('div#middle div#middleCenter div#numResults').text
        num = int(num.split()[0])
        event_id = re.compile(r'http://www.myhabit.com/homepage\??#page=b&sale=(\w+)').match(url).group(1)
        brand, is_new = Event.objects.get_or_create(event_id=event_id)
        # crawl infor before, so always not new
        brand.sale_description = sale_description
        brand.events_end = utc_endtime
        if sale_brand_link: brand.brand_link = sale_brand_link
        brand.num = num
        brand.update_time = datetime.utcnow()
        brand.save()
        common_saved.send(sender=ctx, key=event_id, url=url, is_new=is_new, is_updated=False)

        elements = node.find_elements_by_xpath('./div[@id="asinbox"]/ul/li[starts-with(@id, "result_")]')
        for ele in elements:
            self.parse_category_product(ele, event_id, sale_title, ctx)
        print 'time proc brand list: ', time.time() - time_begin_benchmark


    def parse_category_product(self, element, event_id, sale_title, ctx):
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
        link = l if l.startswith('http') else 'http://www.myhabit.com/homepage' + l
        title = element.find_element_by_class_name('title').text
        try:
            listprice = element.find_element_by_class_name('listprice').text.replace('$', '').replace(',', '')
        except:
            listprice = ''
        ourprice = element.find_element_by_class_name('ourprice').text.replace('$', '').replace(',', '')
#        img = element.find_element_by_class_name('iImg').get_attribute('src')

        asin, casin = self.url2asin(link)
        product, is_new = Product.objects.get_or_create(pk=casin)
        is_updated = False
        if is_new:
            product.event_id = [event_id]
            product.brand = sale_title
            product.asin = asin
            product.title = title
            if soldout == True: product.soldout = True
        else:
            if soldout == True and product.soldout != True:
                product.soldout = soldout
                is_updated = True
            if event_id not in product.event_id: product.event_id.append(event_id)
        product.price = ourprice
        if listprice: product.listprice = listprice
        product.updated = False
        product.list_update_time = datetime.utcnow()
        product.save()
        common_saved.send(sender=ctx, key=casin, url='', is_new=is_new, is_updated=is_updated)
        debug_info.send(sender="myhabit.parse_category_product", title=title, event_id=event_id, asin=asin, casin=casin)


    @exclusive_lock(DB)
    def crawl_product(self, url, casin, ctx):
        """.. :py:method::
            Got all the product information and save into the database

        :param url: product url
        """
        self.check_signin()
        if self.download_page_for_product(url) == 1: return
#            print url
        time_begin_benchmark = time.time()
        product, is_new = Product.objects.get_or_create(pk=casin)
        try:
            pre = self.browser.find_element_by_css_selector('div#main div#page-content div#detail-page')
        except selenium.common.exceptions.NoSuchElementException:
            time.sleep(0.3)
            pre = self.browser.find_element_by_css_selector('div#main div#page-content div#detail-page')
        node = pre.find_element_by_css_selector('div#dpLeftCol')
        right_col = pre.find_element_by_css_selector('div#dpRightCol div#innerRightCol')
        if is_new:
            info_table, image_urls, video = [], [], ''
            shortDesc = node.find_element_by_class_name('shortDesc').text
            international_shipping = node.find_element_by_id('intlShippableBullet').text
            returned = node.find_element_by_id('returnPolicyBullet').text
            already_have = [shortDesc, international_shipping, returned]

            for bullet in node.find_elements_by_tag_name('li'):
                if bullet.text and bullet.text not in already_have:
                    info_table.append(bullet.text)

            for img in node.find_elements_by_xpath('.//div[@id="altImgContainer"]/div'):
                try:
                    picture = img.find_element_by_class_name('zoomImageL2').get_attribute('value')
                    image_urls.append(picture)
                except:
                    video = img.find_element_by_class_name('videoURL').get_attribute('value')

            try:
                color = right_col.find_element_by_xpath('.//div[@class="dimensionAltText variationSelectOn"]').text
            except:
                color = ''
            try:
                sizes = right_col.find_elements_by_xpath('./div[@id="dpVariationMatrix"]//select[@class="variationDropdown"]/option')
                size = [s for s in sizes if not s.text.startswith('Please')]
            except:
                sizes = [] 

            product.summary = shortDesc
            product.list_info = info_table
            product.image_urls = image_urls
            if video: product.video = video
            if international_shipping: product.international_shipping = international_shipping
            if returned: product.returned = returned
            if color: product.color = color
            if sizes: product.sizes = sizes

        listprice = right_col.find_element_by_id('listPrice').text.replace('$', '').replace(',', '')
        ourprice = right_col.find_element_by_id('ourPrice').text.replace('$', '').replace(',', '')
        scarcity = right_col.find_element_by_id('scarcity').text
        shipping = '; '.join( [a.text for a in right_col.find_elements_by_class_name('dpRightColLabel') if a.text] )

        product.price = ourprice
        product.listprice = listprice
        product.shipping = shipping
        if scarcity: product.scarcity = scarcity
        product.updated = True
        product.full_update_time = datetime.utcnow()
        product.save()
        
        common_saved.send(sender=ctx, key=casin, url=url, is_new=is_new, is_updated=not is_new)
        print 'time product process benchmark: ', time.time() - time_begin_benchmark

        

if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
    server.run()
