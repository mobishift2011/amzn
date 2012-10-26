#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.zulily.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""
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

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *

TIMEOUT = 9
headers = { 'User-Agent': 'Mozilla 5.0/Firefox 16.0.1', }
config = { 
    'max_retries': 3,
    'pool_connections': 10, 
    'pool_maxsize': 10, 
}
req = requests.Session(prefetch=True, timeout=15, config=config, headers=headers)


class zulilyLogin(object):
    """.. :py:class:: zulilyLogin
        login, check whether login, fetch page.
    """
    def __init__(self):
        """.. :py:method::
            variables need to be used
        """
        self.login_url = 'https://www.zulily.com/auth'
        self.email = 'huanzhu@favbuy.com'
        self.passwd = '4110050209'
        self.data = {
            'login[username]': self.email,
            'login[password]': self.passwd
        }
        self.reg_check = re.compile(r'https://www.zulily.com/auth/create.*')
        self._signin = False

    def login_account(self):
        """.. :py:method::
            use post method to login
        """
        req.post(self.login_url, data=self.data)
        self._signin = True

    def check_signin(self):
        """.. :py:method::
            check whether the account is login
        """
        if not self._signin:
            self.login_account()

    def fetch_page(url):
        """.. :py:method::
            fetch page.
            check whether the account is login, if not, login and fetch again
        """
        ret = req.get(url)

        if self.reg_check.match(ret.url) is not None: # need to authentication
            self.login_account()
            ret = req.get(url)
        if ret.ok: return ret.content



class Server(object):
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    def __init__(self):
        self.siteurl = 'http://www.zulily.com'
        self.upcoming_url = 'http://www.zulily.com/upcoming_events'
        self.net = zulilyLogin()
        self.extract_event_re = re.compile(r'(http://www.zulily.com/e/(.*).html).*')
        self.extract_image_re = re.compile(r'(http://mcdn.zulily.com/images/cache/event/)\d+x\d+/(.+)')


    def crawl_category(self):
        """.. :py:method::
            From top depts, get all the events
        """
        depts = ['girls', 'boys', 'women', 'baby-maternity', 'toys-playtime', 'home']
        self.queue = Queue.Queue()
        self.upcoming_queue = Queue.Queue()
        debug_info.send(sender=DB + '.category.begin')

        for dept in depts:
            link = 'http://www.zulily.com/?tab={0}'.format(dept)
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
        cont = self.net.fetch_page(url)
        tree = lxml.html.fromstring(cont)
        nodes = tree.xpath('//div[@class="container"]/div[@id="main"]/div[@id="home-page-content"]/div//div[starts-with(@id, "eid_")]')
        
        for node in nodes:
            link = node.xpath('./a[@class="wrapped-link"]').get('href')
            link, lug = self.extract_event_re.match(link).groups()

            brand, is_new = Category.objects.get_or_create(lug=lug)
            if is_new:
                image = node.xpath('./a/span[@class="homepage-image"]/img').get('src')
                text = node.xpath('./a/span[@class="txt"]')
                sale_title = text.xpath('./span[@class="category-name"]/span/text')
                desc = text.xpath('.//span[@class="description-highlights"]/text')
                start_end_date = text.xpath('./span[@class="description"]/span[@class="start-end-date"]/span').text_content()

                brand.image_urls = [image]
                brand.sale_title = sale_title
                brand.short_desc = desc
                brand.start_end_date = start_end_date
            if dept not in brand.dept: brand.dept.append(dept) # events are mixed in different category
            brand.update_time = datetime.utcnow()
            brand.save()
            category_saved.send(sender=DB + '.get_brand_list', site=DB, key=lug, is_new=is_new, is_updated=not is_new)


    def upcoming_proc(self):
        """.. :py:method::
            Get all the upcoming brands info 
        """
        upcoming_list = []
        cont = self.net.fetch_page(self.upcoming_url)
        tree = lxml.html.fromstring(cont)
        nodes = tree.xpath('//div[@class="event-content-list-wrapper"]/ul/li/a')
        for node in nodes:
            link = node.get('href')
            text = node.text_content()
            upcoming_list.append( (text, link) )
        upcoming_detail(upcoming_list)


    def upcoming_detail(self, upcoming_list):
        """.. :py:method::
        """
        for pair in upcoming_list:
            cont = self.net.fetch_page(pair[1])
            tree = lxml.html.fromstring(cont)
            img = tree.xpath('//div[ends-with(@class, "event-content-image")]/img/@src')
            image = ''.join( self.extract_image_re.match(img) )
            sale_title = tree.xpath('//div[ends-with(@class, "event-content-copy")]/h1/text')
            sale_description = tree.xpath('//div[ends-with(@class, "event-content-copy")]/div[@id="desc-with-expanded"]').text_content()
            start_time = tree.xpath('//div[ends-with(@class, "upcoming-date-reminder")]//span[@class="reminder-text"]/text')
            


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
        if not m: print url
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
        pt = pytz.timezone('US/Pacific')
        tinfo = time_str + str(pt.normalize(datetime.now(tz=pt)).year)
        endtime = datetime.strptime(tinfo, '%a %b %d %I %p %Y').replace(tzinfo=pt)
        return pt.normalize(endtime).astimezone(pytz.utc)
    
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
            path = self.browser.find_element_by_xpath('//div[@id="main"]/div[@id="page-content"]/div[@id="top-content"]')
            begin_date = path.find_element_by_xpath('./div[@id="startHeader"]/span[@class="date"]').text # SAT OCT 20
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
            brand.image_url = img
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
#        try:
#        node = self.browser.find_elements_by_xpath('//div[@id="main"]/div[@id="page-content"]/div/div[@id="top"]/div[@id="salePageDescription"]')
        node = self.browser.find_elements_by_xpath('//div[@id="main"]/div[@id="page-content"]/div/div[@id="top"]')
#        except:
#            category_failed.send(sender=DB + '.brand_page', site=DB, url=url, reason='Url can not be parsed.')
#            return

        print node, url
        sale_title = node[0].find_element_by_xpath('.//div[@id="saleTitle"]').text
        sale_description = node[0].find_element_by_xpath('.//div[@id="saleDescription"]').text
        end_date = node[0].find_element_by_xpath('.//div[@id="saleEndTime"]/span[@class="date"]').text # SAT OCT 20
        end_time = node[0].find_element_by_xpath('.//div[@id="saleEndTime"]/span[@class="time"]').text # 9 AM PT
        utc_endtime = self.time_proc(end_date + ' ' + end_time.replace('PT', ''))
        try:
            sale_brand_link = node[0].find_element_by_xpath('.//div[@id="saleBrandLink"]/a').get_attribute('href')
        except:
            sale_brand_link = ''
        num = node[0].find_element_by_xpath('../div[@id="middle"]/div[@id="middleCenter"]/div[@id="numResults"]').text
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

        elements = node[0].find_elements_by_xpath('../div[@id="asinbox"]/ul/li[starts-with(@id, "result_")]')
        for ele in elements:
            self.parse_category_product(ele, sale_id, sale_title, dept)


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
            product.sale_id = sale_id
            product.brand = sale_title
            product.asin = asin
            product.title = title
        product.price = ourprice
        if listprice: product.listprice = listprice
        product.soldout = soldout
        product.updated = False
        product.list_update_time = datetime.utcnow()
        product.save()
        product_saved.send(sender=DB + '.parse_category', site=DB, key=casin, is_new=is_new, is_updated=not is_new)
        debug_info.send(sender="myhabit.parse_category_product", title=title, sale_id=sale_id, asin=asin, casin=casin)


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
        self.check_signin()
        if self.download_page(url) == 1: return
        node = self.browser.find_element_by_xpath('//div[@id="main"]/div[@id="page-content"]/div[@id="detail-page"]/div[@id="dpLeftCol"]')
        shortDesc = node.find_element_by_class_name('shortDesc').text

        international_shipping = node.find_element_by_id('intlShippableBullet').text
        returned = node.find_element_by_id('returnPolicyBullet').text

        already_have = [shortDesc, international_shipping, returned]
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
