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
from datetime import datetime, timedelta
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *

TIMEOUT = 5

class Server(object):
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    def __init__(self):
        self.siteurl = 'http://www.hautelook.com'
        self.email = 'huanzhu@favbuy.com'
        self.passwd = '4110050209'
        self._signin = False

        self.extract_eventid_re = re.compile(r'http://www.hautelook.com/event/(\d+).*')

    def login(self):
        """.. :py:method::
            login myhabit
            Using Firefox will cause Xvfb memory leaf and program broke.

        """
        self.browser = webdriver.Chrome()
#        self.browser.implicitly_wait(1)
        self.browser.get('http://www.hautelook.com/login')
        self.fill_login_form()
        WebDriverWait(self.browser, TIMEOUT, 0.1).until(lambda driver: driver.execute_script('return $.active') == 0)

    def fill_login_form(self):
        """.. :py:method:
            fill in login form when chrome driver is open
        """
        self.browser.find_element_by_css_selector('div#login_form_container > form#login_signin input#login_email').send_keys(self.email)
        self.browser.find_element_by_css_selector('div#login_form_container > form#login_signin input.passwordInput').send_keys(self.passwd)
        self.browser.find_element_by_css_selector('div#login_form_container > form#login_signin div#login_button_standard').click()
        self._signin = True

    def check_signin(self):
        if not self._signin:
            self.login()


    def download_page(self, url):
        """.. :py:method::
            download the url
        :param url: the url need to download
        """
        time_begin_benchmark = time.time()
        try:
            self.browser.get(url)
            WebDriverWait(self.browser, TIMEOUT, 0.1).until(lambda driver: driver.find_element_by_css_selector('div#body div#main div#page-content div#bottom-content'))
        except selenium.common.exceptions.TimeoutException:
            try:
                WebDriverWait(self.browser, TIMEOUT, 0.1).until(lambda driver: driver.execute_script('return $.active') == 0)
            except selenium.common.exceptions.TimeoutException:
                print 'Timeout --> {0}'.format(url)
                return 1
        print 'time download benchmark: ', time.time() - time_begin_benchmark

    def download_regular_page(self, url):
        time_begin_benchmark = time.time()
        try:
            self.browser.get(url)
            WebDriverWait(self.browser, TIMEOUT, 0.1).until(lambda driver: driver.execute_script('return $.active') == 0)
        except selenium.common.exceptions.TimeoutException:
            print 'Timeout --> {0}'.format(url)
            return 1
        print 'time download_regular_page benchmark: ', time.time() - time_begin_benchmark


    @exclusive_lock(DB)
    def crawl_category(self):
        """.. :py:method::
            From top depts, get all the brands
        """
        self.check_signin()
        print self.browser.current_url
        depts = ['women', 'beauty', 'home', 'kids', 'men']
        depts = ['women', ]
        debug_info.send(sender=DB + '.category.begin')

        for dept in depts:
            link = 'http://www.hautelook.com/events#{0}'.format(dept)
            self.get_event_list(dept, link)
#        self.cycle_crawl_category()
        debug_info.send(sender=DB + '.category.end')
        self.browser.quit()
        self._signin = False

    def get_event_list(self, dept, url):
        """.. :py:method::
            Get all the brands from brand list.
            Brand have a list of product.

        :param dept: dept in the page
        :param url: the dept's url
        """
        self.download_regular_page(url)
        tree = lxml.html.fromstring(self.browser.page_source)
        nodes = tree.cssselect('div#container > div#body_content > div#module_event_tiles > div > div.tile')
        for node in nodes:
            l = node.cssselect('a.hero-link')[0].get('href')
            link = l if l.startswith('http') else self.siteurl + l
            sale_id = self.extract_eventid_re.match(link).group(1)
            
            sale_title = node.cssselect('a.hero-link > div.caption > .title')[0].text
            image = node.cssselect('a.hero-link > img.hero')[0].get('src')
            print [sale_title], [image], [link]


#            brand, is_new = Category.objects.get_or_create(sale_id=sale_id)
#            if is_new:
#                brand.sale_title = a_title.text
#                brand.image_urls = [image]
#            if dept not in brand.dept: brand.dept.append(dept) # for designer dept
#            brand.soldout = soldout
#            brand.update_time = datetime.utcnow()
#            brand.save()
#            category_saved.send(sender=DB + '.get_event_list', site=DB, key=sale_id, is_new=is_new, is_updated=not is_new)
#
#
#        # upcoming brand
#        nodes = self.browser.find_elements_by_xpath('//div[@id="main"]/div[@id="page-content"]/div[@id="upcomingSales"]//div[@class="fourColumnSales"]//div[@class="caption"]/a')
#        for node in nodes:
#            l = node.get_attribute('href')
#            link = l if l.startswith('http') else 'http://www.myhabit.com/homepage' + l 
##            title = node.text
#            self.upcoming_queue.put( (dept, link) )



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
        m = re.compile(r'http://www.myhabit.com/homepage.*#page=d&dept=\w+&sale=\w+&asin=(\w+)&cAsin=(\w+)').match(url)
        if not m: print 'Can not parse detail product url: ', url
        return m.groups()

    def cycle_crawl_category(self, timeover=30):
        """.. :py:method::
            read (category, link) tuple from queue, crawl sub-category, insert into the queue

        :param timeover: timeout in queue.get
        """
        self.queue_get_parse(self.upcoming_queue, timeover, upcoming=True)
        self.queue_get_parse(self.queue, timeover)

    def queue_get_parse(self, queue, timeover, upcoming=False):
        """.. :py:method::
            get queue and parse the brand page
        :param queue: upcoming brand queue or brand page queue
        :param upcoming: flag to shwo whether it is the upcoming queue or not
        """
        while not queue.empty():
#            try:
            job = queue.get(timeout=timeover)
            if self.download_page(job[1]) == 1:
                continue
            if upcoming:
                self.parse_upcoming(job[0], job[1])
            else:
                self.parse_category(job[0], job[1])
#            except Queue.Empty:
#                debug_info.send(sender="{0}.category:Queue waiting {1} seconds without response!".format(DB, timeover))
#            except:
#                debug_info.send(sender=DB + ".category", tracebackinfo=sys.exc_info())


    def time_proc(self, time_str):
        """.. :py:method::

        :param time_str: u'SAT OCT 20 9 AM '
        :rtype: datetime type utc time
        """
        time_format = '%a %b %d %I %p %Y'
        pt = pytz.timezone('US/Pacific')
        tinfo = time_str + str(pt.normalize(datetime.now(tz=pt)).year)
        endtime = pt.localize(datetime.strptime(tinfo, time_format))
        return endtime.astimezone(pytz.utc)
    
    def parse_upcoming(self, dept, url):
        """.. :py:method::
            upcoming brand page parsing
            upcoming brand also have duplicate designer

        :param dept: dept in the page
        :param url: url in the page
        """
        sale_id = self.url2saleid(url)
        brand, is_new = Category.objects.get_or_create(sale_id=sale_id)
        if is_new:
            path = self.browser.find_element_by_css_selector('div#main div#page-content div#top-content')
            try:
                begin_date = path.find_element_by_css_selector('div#startHeader span.date').text # SAT OCT 20
            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(1)
                path = self.browser.find_element_by_css_selector('div#main div#page-content div#top-content')
                begin_date = path.find_element_by_css_selector('div#startHeader span.date').text # SAT OCT 20
            begin_time = path.find_element_by_xpath('./div[@id="startHeader"]/span[@class="time"]').text # 9 AM PT
            utc_begintime = self.time_proc(begin_date + ' ' + begin_time.replace('PT', ''))
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
            brand.save()
        else:
            if dept not in brand.dept:
                brand.dept.append(dept)
                brand.save()
        category_saved.send(sender=DB + '.parse_upcoming', site=DB, key=sale_id, is_new=is_new, is_updated=not is_new)


    def parse_category(self, dept, url):
        """.. :py:method::
            Brand page parsing

        :param dept: dept in the page
        :param url: url in the page
        """
#        time.sleep(0.5)
#        node = self.browser.find_element_by_xpath('//div[@id="main"]/div[@id="page-content"]/div/div[@id="top"]/div[@id="salePageDescription"]')
        node = self.browser.find_element_by_css_selector('div#main div#page-content div')

#        print node, url
        time_begin_benchmark = time.time()
#        sale_title = node.find_element_by_xpath('.//div[@id="saleTitle"]').text
#        sale_description = node.find_element_by_xpath('.//div[@id="saleDescription"]').text
#        end_date = node.find_element_by_xpath('.//div[@id="saleEndTime"]/span[@class="date"]').text # SAT OCT 20
#        end_time = node.find_element_by_xpath('.//div[@id="saleEndTime"]/span[@class="time"]').text # 9 AM PT
        sale_title = node.find_element_by_css_selector('div#top div#saleTitle').text
        sale_description = node.find_element_by_css_selector('div#top div#saleDescription').text
        end_date = node.find_element_by_css_selector('div#top div#saleEndTime span.date').text # SAT OCT 20
        end_time = node.find_element_by_css_selector('div#top div#saleEndTime span.time').text # 9 AM PT
        utc_endtime = self.time_proc(end_date + ' ' + end_time.replace('PT', ''))
        try:
            sale_brand_link = node.find_element_by_xpath('.//div[@id="saleBrandLink"]/a').get_attribute('href')
        except:
            sale_brand_link = ''
        num = node.find_element_by_css_selector('div#middle div#middleCenter div#numResults').text
        num = int(num.split()[0])
        sale_id = self.url2saleid(url)

        brand, is_new = Category.objects.get_or_create(sale_id=sale_id)
        # crawl infor before, so always not new
        brand.sale_description = sale_description
        brand.events_end = utc_endtime
        if sale_brand_link: brand.brand_link = sale_brand_link
        brand.num = num
        brand.update_time = datetime.utcnow()
        brand.save()
        category_saved.send(sender=DB + '.parse_category', site=DB, key=sale_id, is_new=is_new, is_updated=not is_new)

        elements = node.find_elements_by_xpath('./div[@id="asinbox"]/ul/li[starts-with(@id, "result_")]')
        for ele in elements:
            self.parse_category_product(ele, sale_id, sale_title, dept)

        print 'time proc brand list: ', time.time() - time_begin_benchmark

    def parse_category_product(self, element, sale_id, sale_title, dept):
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
        if is_new:
            product.dept = dept
            product.sale_id = [sale_id]
            product.brand = sale_title
            product.asin = asin
            product.title = title
        else:
            if sale_id not in product.sale_id: product.sale_id.append(sale_id)
        product.price = ourprice
        if listprice: product.listprice = listprice
        product.soldout = soldout
        product.updated = False
        product.list_update_time = datetime.utcnow()
        product.save()
        product_saved.send(sender=DB + '.parse_category', site=DB, key=casin, is_new=is_new, is_updated=not is_new)
        debug_info.send(sender="myhabit.parse_category_product", title=title, sale_id=sale_id, asin=asin, casin=casin)


    @exclusive_lock(DB)
    def crawl_listing(self):
        """.. :py:method::
            not implement
        """
        pass

    @exclusive_lock(DB)
    def crawl_product(self, url, casin):
        """.. :py:method::
            Got all the product information and save into the database

        :param url: product url
        """
        self.check_signin()
        if self.download_page_for_product(url) == 1: return
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
        
        product_saved.send(sender=DB + '.parse_product_detail', site=DB, key=casin, is_new=is_new, is_updated=not is_new)
        print 'time product process benchmark: ', time.time() - time_begin_benchmark

        

if __name__ == '__main__':
    server = Server()
    server.crawl_category()
#    server = zerorpc.Server(Server())
#    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
#    server.run()
