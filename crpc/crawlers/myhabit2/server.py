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

#        sale_title = node[0].find_element_by_xpath('./div[@id="saleTitle"]').text
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
        brand.save()
        category_saved.send(sender=DB + '.parse_category', site=DB, key=sale_id, is_new=is_new, is_updated=not is_new)

        elements = node[0].find_elements_by_xpath('../../div[@id="asinbox"]/ul/li[starts-with(@id, "result_")]')
        for ele in elements:
            self.parse_category_product(ele)


    def parse_category_product(self, element):
        """.. :py:method::
            Brand page, product parsing

        :param element: product's xpath element
        """
        l = element.find_element_by_class_name('evt-prdtDesc-a').get_attribute('href')
        link = l if l startswith('http') else 'http://www.myhabit.com/homepage' + l
        title = element.find_element_by_class_name('title').text
        listprice = element.find_element_by_class_name('listprice').text
        ourprice = element.find_element_by_class_name('ourprice').text
#        img = element.find_element_by_class_name('iImg').get_attribute('src')

        asin, casin = self.url2asin(link)
        product, is_new = Product.objects.get_or_create(pk=casin)
        if is_new:
            product.dept = dept
            product.sale_id = sale_id
            product.asin = asin
            product.title = title
        product.price = ourprice
        product.listprice = listprice
        product.save()
        product_saved.send(sender=DB + '.parse_category', site=DB, key=casin, is_new=is_new, is_updated=not is_new)


    def crawl_listing(self):
        """.. :py:method::
            not implement
        """
        pass

    def crawl_product(self, url):
        """.. :py:method::

        :param url: product url
        """
        self.browser.get(url)
        node = self.browser.find_element_by_xpath('//div[@id="main"]/div[@id="page-content"]/div[@id="detail-page"]')
        shortDesc = node.find_element_by_class_name('shortDesc').text
        node.find_element_by_xpath()

        self.parse_product(url)

        
    def parse_product(self, url):
        try:
            node = tree.xpath('//div[@id="wrapper"]/div[@id="frame"]/div[@id="align"]')[0]
        except:
            log.log_traceback(self.logger_product, 'Parsing page problem: {0}'.format(url))
            redis_SERVER.hincrby(redis_KEY, 'num_parse_error', 1)
            return

        also_like = []
        like = node.xpath('./div[@id="lCol"]//div[@class="mbContent"]//ul/li')
        for l in like:
            link = l.xpath('./a/@href')[0]
            title = l.xpath('./a/text()')[0]
            link = link if link.startswith('http') else self.caturl + link
            also_like.append( (title, link) )

        title = node.xpath('./div[@id="rCol"]//h1[@class="productHeading"]/text()')[0]
        price = node.xpath('./div[@id="rCol"]//div[@class="op"]/text()')
        if not price:
            log.log_traceback(self.logger_product, 'Page donot have a price: {0}'.format(url))

        shipping = node.xpath('./div[@id="rCol"]//div[@class="fs"]//font[@class="alert"]/text()')
        img = node.xpath('./div[@id="rCol"]/div[@class="r1w secSpace"]//div[@id="galImg"]/a/img/@src')
        if not img:
            img = tree.xpath('//div[@id="wrapper"]/div[@id="frame"]/form[@name="path"]/input/@value')
        if not img:
            log.log_traceback(self.logger_product, 'Page donot have a image: {0}'.format(url))

        description = node.xpath('./div[@id="rCol"]/div[@id="FieldsetProductInfo"]')[0].text_content()
        model = ''
        if description:
            m = re.compile(r'.*(Model|Model Number):(.*)\n').search(description)
            if m: model = m.group(1).strip()

        available = node.xpath('./div[@id="rCol"]//div[@id="prodpad"]//div[@class="availability"]/text()')
        if available:
            available = ''.join(available).strip()

        comment = []
        rating = node.xpath('./div[@id="rCol"]/div[@id="FieldsetCustomerReviews"]//div[@class="pr-snapshot-rating rating"]/span[@class="pr-rating pr-rounded average"]/text()')
        reviews = node.xpath('./div[@id="rCol"]/div[@id="FieldsetCustomerReviews"]//div[@class="pr-snapshot-rating rating"]//span[@class="count"]/text()')
        if reviews: reviews = int(reviews[0].replace(',', ''))
        if rating:
            rating = float(rating[0])

            comment_all = node.xpath('./div[@id="rCol"]/div[@id="FieldsetCustomerReviews"]//div[starts-with(@id, "pr-contents-")]//div[@class="pr-review-wrap"]')
            for comm in comment_all:
                rate = comm.xpath('.//span[@class="pr-rating pr-rounded"]/text()')[0]
                head = comm.xpath('.//p[@class="pr-review-rating-headline"]/text()')[0]
                text = comm.xpath('./div[@class="pr-review-main-wrapper"]//p[@class="pr-comments"]/text()')[0]
                comment.append(rate, head, text)


        itemNO = re.compile(r'http://www.dickssportinggoods.com/product/index.jsp.*productId=(\d+).*').match(url).group(1)
        product = Product.objects(itemNO=itemNO).first()
        if not product:
            product = Product(itemNO=itemNO)
            redis_SERVER.hincrby(redis_KEY, 'num_new_crawl', 1)
        else:
            redis_SERVER.hincrby(redis_KEY, 'num_new_update', 1)

        product.title = title
        if also_like: product.also_like = also_like
        if price:
            product.price = price[0].split(':')[1].strip().replace('$', '').replace(',', '')
        if shipping: product.shipping = shipping
        if img: product.image = img[0]
        if description: product.description = description
        if model: product.model = model
        if available: product.available = available
        if rating: product.rating = rating
        if review: product.reviews = reviews
        if comment: product.comment = comment

        product.full_update_time = datetime.utcnow()
        product.updated = True
        product.save()


    def update_product(self, product, *targs):
        """ Parameter *targs for updating:
                useful_param = ['price', 'available', 'shipping', 'rating', 'reviews']
        """
        url = product.url()
        content = self.fetch_page(url)
        if not content:
            log.log_traceback(self.logger_update, 'Page url can not be downloaded {0}'.format(url))
        try:
            tree = lxml.html.fromstring(content)
        except:
            log.log_traceback(self.logger_update, 'Page {0} can not build xml tree {1}'.format(url, content))
            return

        try:
            node = tree.xpath('//div[@id="wrapper"]/div[@id="frame"]/div[@id="align"]')[0]
        except:
            redis_SERVER.hincrby(redis_KEY, 'num_parse_error', 1)
            log.log_traceback(self.logger_update, 'Product url can not be parsed: {0}'.format(url))
#            log.log_print('content: {0}'.format(content), self.logger_update, logging.DEBUG)
            return

        if 'price' in targs:
            price = node.xpath('./div[@id="rCol"]//div[@class="op"]/text()')
            if price:
                product.price = price[0].split(':')[1].strip().replace('$', '').replace(',', '')

        if 'available' in targs:
            available = node.xpath('./div[@id="rCol"]//div[@id="prodpad"]//div[@class="availability"]/text()')
            if available:
                product.available = ''.join(available).strip()

        if 'shipping' in targs:
            shipping = node.xpath('./div[@id="rCol"]//div[@class="fs"]//font[@class="alert"]/text()')
            if shipping: product.shipping = shipping

        if 'rating' in targs:
            rating = node.xpath('./div[@id="rCol"]/div[@id="FieldsetCustomerReviews"]//div[@class="pr-snapshot-rating rating"]/span[@class="pr-rating pr-rounded average"]/text()')
            if rating:
                rating = float(rating[0])
                product.rating = rating

        if 'reviews' in targs:
            reviews = node.xpath('./div[@id="rCol"]/div[@id="FieldsetCustomerReviews"]//div[@class="pr-snapshot-rating rating"]//span[@class="count"]/text()')
            if reviews:
                reviews = int(reviews[0].replace(',', ''))
                product.reviews = reviews

        product.save()


if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
    server.run()
