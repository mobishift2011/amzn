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
        self.upcoming_label = 'li.up-result' 
        self.event_label = 'div#centerContent'
        self.listing_label = ''
        self.product_label = 'div#bbContent'

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

    def download_page(self, url, label=None):
        """.. :py:method::
            download the url
        :param url: the url need to download
        """
#        time_begin_benchmark = time.time()
        try:
            self.browser.get(url)
            if self.browser.title == u'Amazon.com Sign In':
                self.fill_login_form()
            if label:
                WebDriverWait(self.browser, TIMEOUT, 0.5).until(lambda driver: driver.execute_script('return $.active') == 0 and driver.find_element_by_css_selector(label))
            else:
                WebDriverWait(self.browser, TIMEOUT, 0.5).until(lambda driver: driver.execute_script('return $.active') == 0)
        except selenium.common.exceptions.TimeoutException:
            print 'Timeout ---> {0}, {1}'.format(url, label)
            return 1
#        print 'time download benchmark: ', time.time() - time_begin_benchmark


    @exclusive_lock(DB)
    def crawl_category(self, ctx):
        """.. :py:method::
            From top depts, get all the events
        """
        self.check_signin()
        depts = ['women', 'men', 'kids', 'home', 'designer']
        self.upcoming_queue = Queue.Queue()
        debug_info.send(sender=DB + '.category.begin')

        for dept in depts:
            link = 'http://www.myhabit.com/homepage?#page=g&dept={0}&ref=qd_nav_tab_{0}'.format(dept)
            try:
                self.get_event_list(dept, link, ctx)
            except:
                common_failed.send(sender=ctx, key='crawl_category', url=link, reason=sys.exc_info())
        self.cycle_crawl_category(ctx)
        
        debug_info.send(sender=DB + '.category.end')


    def cycle_crawl_category(self, ctx, timeover=30):
        """.. :py:method::
            read (category, link) tuple from queue, crawl sub-category, insert into the queue
            get queue and parse the event page

        :param timeover: timeout in queue.get
        """
        debug_info.send(sender='{0}.cycle_crawl_category.begin:queue size {1}'.format(DB, self.upcoming_queue.qsize()))
        while not self.upcoming_queue.empty():
            try:
                job = self.upcoming_queue.get(timeout=timeover)
                if self.download_page(job[1], self.upcoming_label) == 1:
                    pass
                self.parse_upcoming(job[0], job[1], ctx)
            except Queue.Empty:
                common_failed.send(sender=ctx, key='cycle_crawl_category', url='' )
            except:
                common_failed.send(sender=ctx, key='cycle_crawl_category', url=job[1], reason=sys.exc_info())
        debug_info.send(sender=DB + '.cycle_crawl_category.end')


    def url2saleid(self, url):
        """.. :py:method::

        :param url: the event's url
        :rtype: string of event_id
        """
        return re.compile(r'http://www.myhabit.com/homepage\??#page=b&dept=\w+&sale=(\w+)').match(url).group(1)

    def url2asin(self, url):
        """.. :py:method::

        :param url: the product's url
        :rtype: string of asin, cAsin
        """
        m = re.compile(r'http://www.myhabit.com/.*#page=d&dept=\w+&sale=\w+&asin=(\w+)&cAsin=(\w+)').match(url)
#        if not m: print 'Can not parse detail product url: ', url
        return m.groups()
    

    def get_event_list(self, dept, url, ctx):
        """.. :py:method::
            Get all the events from event list.
            Brand have a list of product.

        :param dept: dept in the page
        :param url: the dept's url
        """
        self.download_page(url, self.event_label)
        browser = lxml.html.fromstring(self.browser.page_source)
        nodes = browser.xpath('//div[@id="main"]/div[@id="page-content"]/div[@id="currentSales"]//div[starts-with(@id, "privateSale")]')
        if len(nodes) == 0 or not nodes:
            time.sleep(1)
            browser = lxml.html.fromstring(self.browser.page_source)
            nodes = browser.xpath('//div[@id="main"]/div[@id="page-content"]/div[@id="currentSales"]//div[starts-with(@id, "privateSale")]')

        for node in nodes:
            a_title = node.xpath('./div[@class="caption"]/a')[0]
            l = a_title.get('href')
            link = l if l.startswith('http') else 'http://www.myhabit.com/homepage' + l
            event_id = self.url2saleid(link)

            image = node.xpath('./div[@class="image"]/a/img')[0].get('src')
            # try: # if can't be found, cost a long time and raise NoSuchElementException
            soldout = node.xpath('./div[@class="image"]/a/div[@class="soldout"]')

            event = Event.objects(event_id=event_id).first()
            is_new, is_updated = False, False
            if not event:
                is_new = True
                event = Event(event_id=event_id)
                event.dept = [dept]
                event.sale_title = a_title.text
                event.image_urls = [image]
                event.soldout = True if soldout else False
                event.urgent = True
                event.combine_url = 'http://www.myhabit.com/homepage#page=b&sale={0}'.format(event_id)
            else:
                if soldout and event.soldout != True:
                    event.soldout = True
                    is_updated = True
                if dept not in event.dept: event.dept.append(dept) # for designer dept
            event.update_time = datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, key=event_id, url=url, is_new=is_new, is_updated=is_updated)

        # upcoming event
        nodes = browser.xpath('//div[@id="main"]/div[@id="page-content"]/div[@id="upcomingSales"]//div[@class="fourColumnSales"]//div[@class="caption"]/a')
        for node in nodes:
            l = node.get('href')
            link = l if l.startswith('http') else 'http://www.myhabit.com/homepage' + l 
#            title = node.text
            self.upcoming_queue.put( (dept, link) )
        

    def parse_upcoming(self, dept, url, ctx):
        """.. :py:method::
            upcoming event page parsing
            upcoming event also have duplicate designer

        :param dept: dept in the page
        :param url: url in the page
        """
        event_id = self.url2saleid(url)
        event = Event.objects(event_id=event_id).first()
        is_new, is_updated = False, False
        if not event:
            is_new = True
            browser = lxml.html.fromstring(self.browser.page_source)
            path = browser.cssselect('div#main div#page-content div#top-content')[0]

            try:
                begin_date = path.cssselect('div#startHeader span.date')[0].text # SAT OCT 20
            except:
                time.sleep(1)
                browser = lxml.html.fromstring(self.browser.page_source)
                path = browser.cssselect('div#main div#page-content div#top-content')[0]
                begin_date = path.cssselect('div#startHeader span.date')[0].text # SAT OCT 20
#                common_failed.send(sender=ctx, url=url, reason='probably the begin_date can not be pased.')
            begin_time = path.xpath('./div[@id="startHeader"]/span[@class="time"]')[0].text # 9 AM PT
            utc_begintime = time_convert(begin_date + ' ' + begin_time.replace('PT', ''), '%a %b %d %I %p %Y') #u'SAT OCT 20 9 AM '
            brand_info = path.cssselect('div#upcomingSaleBlurb')[0].text
            img = path.xpath('./div[@class="upcomingSaleHero"]/div[@class="image"]/img')[0].get('src')
            sale_title = path.xpath('./div[@class="upcomingSaleHero"]/div[@class="image"]/img')[0].get('alt')
            subs = []
            for sub in path.xpath('./div[@id="asinbox"]/ul/li'):
                sub_title = sub.cssselect('div.title')[0].text
                sub_img = sub.xpath('./img')[0].get('src')
                subs.append([sub_title, sub_img])

            event = Event(event_id=event_id)
            event.dept = [dept]
            event.sale_title = sale_title
            event.image_urls = [img]
            event.events_begin = utc_begintime
            event.sale_description = brand_info
            event.upcoming_title_img = subs
            event.update_time = datetime.utcnow()
            event.urgent = True
            event.combine_url = 'http://www.myhabit.com/homepage#page=b&sale={0}'.format(event_id)
        else:
            if dept not in event.dept: event.dept.append(dept)
        event.save()
        common_saved.send(sender=ctx, key=event_id, url=url, is_new=is_new, is_updated=False)


    @exclusive_lock(DB)
    def crawl_listing(self, url, ctx):
        """.. :py:method::
            Brand page parsing

        :param url: url in the page
        """
        self.check_signin()
        if self.download_page(url, self.listing_label) == 1:
            pass
        time_begin_benchmark = time.time()
        browser = lxml.html.fromstring(self.browser.page_source)
        try:
            node = browser.cssselect('div#main div#page-content div')[0]
        except:
            time.sleep(1)
            browser = lxml.html.fromstring(self.browser.page_source)
            node = browser.cssselect('div#main div#page-content div')[0]

        sale_title = node.cssselect('div#top div#saleTitle')[0].text
        sale_description = node.cssselect('div#top div#saleDescription')[0].text
        end_date = node.cssselect('div#top div#saleEndTime span.date')[0].text # SAT OCT 20
        end_time = node.cssselect('div#top div#saleEndTime span.time')[0].text # 9 AM PT
        utc_endtime = time_convert(end_date + ' ' + end_time.replace('PT', ''), '%a %b %d %I %p %Y') #u'SAT OCT 20 9 AM '
        try:
            sale_brand_link = node.xpath('.//div[@id="saleBrandLink"]/a')[0].get('href')
        except:
            sale_brand_link = ''
        num = node.cssselect('div#middle div#middleCenter div#numResults')[0].text
        num = int(num.split()[0])
        event_id = re.compile(r'http://www.myhabit.com/homepage\??#page=b&sale=(\w+)').match(url).group(1)
        elements = node.xpath('./div[@id="asinbox"]/ul/li[starts-with(@id, "result_")]')
        for ele in elements:
            self.parse_category_product(ele, event_id, sale_title, ctx)

        # crawl info before, so always not new
        event = Event.objects(event_id=event_id).first()
        is_new, is_updated = False, False
        if not event:
            is_new = True
            event = Event(event_id=event_id)
        event.sale_description = sale_description
        event.events_end = utc_endtime
        if sale_brand_link: event.brand_link = sale_brand_link
        event.num = num
        if event.urgent == True:
            event.urgent = False
            ready = 'Event'
        else:
            ready = None
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, key=event_id, url=url, is_new=is_new, is_updated=is_updated, ready=ready)
#        print 'time proc event list: ', time.time() - time_begin_benchmark


    def parse_category_product(self, element, event_id, sale_title, ctx):
        """.. :py:method::
            Brand page, product parsing

        :param element: product's xpath element
        :param sale_title: as event pass to product
        """
        soldout = element.cssselect('a.evt-prdtImg-a div.soldout')
        prod = element.cssselect('a.evt-prdtDesc-a')[0]
        l = prod.get('href')
        link = l if l.startswith('http') else 'http://www.myhabit.com/homepage' + l
        title = prod.cssselect('div.title')[0].text
        listprice_node = prod.cssselect('span.listprice')
        if listprice_node:
            listprice = listprice_node[0].text.replace('$', '').replace(',', '')
        else:
            listprice = ''
        ourprice_node = prod.cssselect('span.ourprice')
        if ourprice_node:
            ourprice = ourprice_node[0].text.replace('$', '').replace(',', '')
        else:
            ourprice = ''
#        img = element.find_element_by_class_name('iImg').get_attribute('src')

        asin, casin = self.url2asin(link)
        product, is_new = Product.objects.get_or_create(pk=casin)
        is_updated = False
        if is_new:
            product.event_id = [event_id]
#            product.brand = sale_title
            product.asin = asin
            product.title = title
            product.soldout = True if soldout else False
            product.updated = False
            product.combine_url = 'http://www.myhabit.com/homepage#page=d&sale={0}&asin={1}&cAsin={2}'.format(event_id, asin, casin)
        else:
            if soldout and product.soldout != True:
                product.soldout = True
                is_updated = True
            if event_id not in product.event_id: product.event_id.append(event_id)
        product.price = ourprice
        if listprice: product.listprice = listprice
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
        if self.download_page(url, self.product_label) == 1:
            pass
        time_begin_benchmark = time.time()
        browser = lxml.html.fromstring(self.browser.page_source)
        try:
            pre = browser.cssselect('div#main div#page-content div#detail-page')[0]
        except:
            time.sleep(1)
            browser = lxml.html.fromstring(self.browser.page_source)
            pre = browser.cssselect('div#main div#page-content div#detail-page')[0]
        node = pre.cssselect('div#dpLeftCol')[0]
        right_col = pre.cssselect('div#dpRightCol div#innerRightCol')[0]

        product, is_new = Product.objects.get_or_create(pk=casin)
        info_table, image_urls, video = [], [], ''
        shortDesc_node = node.cssselect('div#dpProdDesc div#pdBullets li.shortDesc')
        if shortDesc_node: shortDesc = shortDesc_node[0].text
        else: shortDesc = ''
        international_shipping = node.cssselect('div#dpProdDesc div#pdBullets li#intlShippableBullet')[0].text
        returned = node.cssselect('div#dpProdDesc div#pdBullets li#returnPolicyBullet')[0].text
        already_have = [international_shipping, returned]
        if shortDesc: already_have.append(shortDesc)

        for bullet in node.cssselect('div#dpProdDesc div#pdBullets li'):
            if bullet.text and bullet.text not in already_have:
                info_table.append(bullet.text)

        for img in node.cssselect('div#altImgContainer > div'):
            try:
                picture = img.cssselect('.zoomImageL2')[0].get('value')
                image_urls.append(picture)
            except:
                try:
                    video = img.cssselect('.videoURL').get('value')
                except:
                    video = ''

        color_node = right_col.xpath('.//div[@class="dimensionAltText variationSelectOn"]')
        if color_node: color = color_node[0].text
        else: color = ''
        sizes_node = right_col.xpath('./div[@id="dpVariationMatrix"]//select[@class="variationDropdown"]/option')
        if sizes_node: sizes = [s.text for s in sizes_node if not s.text.startswith('Please')]
        else: sizes = [] 

        product.summary = shortDesc
        product.list_info = info_table
        product.image_urls = image_urls
        if video: product.video = video
        if international_shipping: product.international_shipping = international_shipping
        if returned: product.returned = returned
        if color: product.color = color
        if sizes: product.sizes = sizes

        listprice = right_col.cssselect('div#dpPriceRow span#listPrice')[0].text
        if listprice:
            listprice = listprice.replace('$', '').replace(',', '')
        else:
            listprice = ''
        ourprice = right_col.cssselect('div#dpPriceRow span#ourPrice')[0].text.replace('$', '').replace(',', '')
        scarcity = right_col.cssselect('div#scarcity')[0].text
        shipping = '; '.join( [a.text for a in right_col.cssselect('div.dpRightColLabel') if a.text] )

        product.price = ourprice
        if listprice: product.listprice = listprice
        product.shipping = shipping
        if scarcity: product.scarcity = scarcity
        if product.updated == False:
            product.updated = True
            ready = 'Product'
        else:
            ready = None
        product.full_update_time = datetime.utcnow()
        product.save()
        
        common_saved.send(sender=ctx, key=casin, url=url, is_new=is_new, is_updated=False, ready=ready)
#        print 'time product process benchmark: ', time.time() - time_begin_benchmark


if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
    server.run()
