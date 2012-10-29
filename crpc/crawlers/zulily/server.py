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
req = requests.Session(prefetch=True, timeout=17, config=config, headers=headers)


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

    def fetch_page(self, url):
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
        self.extract_event_lug = re.compile(r'(http://www.zulily.com/e/(.*).html).*')
        self.extract_event_img = re.compile(r'(http://mcdn.zulily.com/images/cache/event/)\d+x\d+/(.+)')
        self.extract_product_img = re.compile(r'(http://mcdn.zulily.com/images/cache/product/)\d+x\d+/(.+)')
        self.extract_product_re = re.compile(r'http://www.zulily.com/p/(.+).html.*')

    def crawl_category(self):
        """.. :py:method::
            From top depts, get all the events
        """
        depts = ['girls', 'boys', 'women', 'baby-maternity', 'toys-playtime', 'home']
        self.queue = Queue.Queue()
        debug_info.send(sender=DB + '.category.begin')

        self.upcoming_proc()
        for dept in depts:
            link = 'http://www.zulily.com/?tab={0}'.format(dept)
            self.get_event_list(dept, link)
        debug_info.send(sender=DB + '.category.end')

    def get_event_list(self, dept, url):
        """.. :py:method::
            Get all the brands from brand list.
            Brand have a list of product.

        :param dept: dept in the page
        :param url: the dept's url
        """
        cont = self.net.fetch_page(url)
        tree = lxml.html.fromstring(cont)
        nodes = tree.xpath('//div[@class="container"]/div[@id="main"]/div[@id="home-page-content"]/div[@class="clearfix"]//div[starts-with(@id, "eid_")]')
        
        for node in nodes:
            link = node.xpath('./a[@class="wrapped-link"]')[0].get('href')
            link, lug = self.extract_event_lug.match(link).groups()

            brand, is_new = Category.objects.get_or_create(lug=lug)
            if is_new:
                img = node.xpath('./a/span[@class="homepage-image"]/img/@src')[0]
                image = ''.join( self.extract_event_img.match(img).groups() )
                text = node.xpath('./a/span[@class="txt"]')[0]
                sale_title = text.xpath('./span[@class="category-name"]/span/text()')[0]

                brand.image_urls = [image]
                brand.sale_title = sale_title
            if dept not in brand.dept: brand.dept.append(dept) # events are mixed in different category
            desc = text.xpath('.//span[@class="description-highlights"]/text()')[0].strip()
            start_end_date = text.xpath('./span[@class="description"]/span[@class="start-end-date"]/span')[0].text_content().strip()
            brand.short_desc = desc
            brand.start_end_date = start_end_date
            brand,is_leaf = True
            brand.update_time = datetime.utcnow()
            brand.save()
            category_saved.send(sender=DB + '.get_event_list', site=DB, key=lug, is_new=is_new, is_updated=not is_new)


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
        self.upcoming_detail(upcoming_list)

    def upcoming_detail(self, upcoming_list):
        """.. :py:method::
        """
        for pair in upcoming_list:
            cont = self.net.fetch_page(pair[1])
            node = lxml.html.fromstring(cont).cssselect('div.event-content-wrapper')[0]
            calendar_file = node.cssselect('div.upcoming-date-reminder a.reminder-ical')[0].get('href')
            ics_file = self.net.fetch_page(calendar_file)
            lug = re.compile(r'URL:http://www.zulily.com/e/(.+).html.*').search(ics_file).group(1)
            brand, is_new = Category.objects.get_or_create(lug=lug)
            if is_new:
                img = node.cssselect('div.event-content-image img')[0].get('src')
                image = ''.join( self.extract_event_img.match(img).groups() )
                sale_title = node.cssselect('div.event-content-copy h1')[0].text_content()
                sale_description = node.cssselect('div.event-content-copy div#desc-with-expanded')[0].text_content().strip()
                start_time = node.cssselect('div.upcoming-date-reminder span.reminder-text')[0].text_content() # 'Starts Sat 10/27 6am pt - SET REMINDER'
                events_begin = self.time_proc( ' '.join( start_time.split(' ', 4)[1:-1] ) )

                brand.image_urls = [image]
                brand.sale_title = sale_title 
                brand.sale_description = sale_description
                brand.events_begin = events_begin
                brand.update_time = datetime.utcnow()
                brand.save()
                category_saved.send(sender=DB + '.upcoming_detail', site=DB, key=lug, is_new=is_new, is_updated=not is_new)
            
    def time_proc(self, time_str):
        """.. :py:method::

        :param time_str: 'Sat 10/27 6am'
        :rtype: datetime type utc time
        """
        time_format = '%a %m/%d %I%p%Y'
        pt = pytz.timezone('US/Pacific')
        tinfo = time_str + str(pt.normalize(datetime.now(tz=pt)).year)
        endtime =  pt.localize(datetime.strptime(tinfo, time_format))
        return endtime.astimezone(pytz.utc)


    def crawl_listing(self, url):
        """.. :py:method::
            from url get listing page.
            from listing page get Eventi's description, endtime, number of products.
            Get all product's image, url, title, price, soldout

        :param url: listing page url
        """
        cont = self.net.fetch_page(url)
        tree = lxml.html.fromstring(cont)
        node = tree.cssselect('div.container>div#main>div#category-view')[0]
        lug = self.extract_event_lug.match(url).group(2)
        brand, is_new = Category.objects.get_or_create(lug=lug)
        if is_new or brand.sale_description is None:
            brand.sale_description = node.cssselect('div#category-description>div#desc-with-expanded')[0].text_content().strip()

        items = node.cssselect('div#products-grid li.item'):
        end_date = node.cssselect('div#new-content-header>div.end-date')[0].text_content().strip()
        end_date = end_date[end_date.find('in')+2:].strip() # '2 hours' or '1 day(s) 3 hours'
        days = int(end_date.split()[0]) if 'day' in end_date else 0
        hours = int(end_date.split()[-2]) if 'hour' in end_date else 0
        brand.events_end = datetime.utcnow() + timedelta(days=days, hours=hours)
        brand.num = len(items)
        brand.update_time = datetime.utcnow()
        brand.save()
        category_saved.send(sender=DB + '.crawl_listing', site=DB, key=lug, is_new=is_new, is_updated=not is_new)

        for item in items: self.crawl_list_product(item)
        page_num = 1
        if self.detect_list_next(node, page_num + 1) is True:
            self.crawl_list_next(url, next_page[-1].get('href'), page_num + 1)

    def detect_list_next(self, node, page_num):
        """.. :py:method::
            detect whether the listing page have a next page

        :param node: the node generate by crawl_listing
        :param page_num: page number of this event
        """
        next_page = node.cssselect('div#pagination>a[href]'): # if have next page
        if next_page:
            next_page_relative_url = next_page[-1].get('href')
            if str(page_num) in next_page_relative_url:
                return True

    def crawl_list_next(self, url, page_text, page_num):
        """.. :py:method::
            crawl listing page's next page, that is page 2, 3, 4, ...

        :param url: listing page url
        :param page_text: this page's relative url
        :param page_num: page number of this event
        """
        cont = self.net.fetch_page(url + page_text)
        tree = lxml.html.fromstring(cont)
        node = tree.cssselect('div.container>div#main>div#category-view')[0]
        items = node.cssselect('div#products-grid li.item'):

        for item in items: self.crawl_list_product(item)
        if self.detect_list_next(node, page_num + 1) is True:
            self.crawl_list_next(url, next_page[-1].get('href'), page_num + 1)

    def crawl_list_product(self, item)
        """.. :py:method::
            In listing page, Get all product's image, url, title, price, soldout

        :param item: item of xml node
        """
        title_link = item.cssselect('div.product-name>a[title]')[0]
        title = title_link.get('title')
        link = title_link.get('href')
        lug = self.extract_product_re.match(link).group(1)
        product, is_new = Product.objects.get_or_create(pk=lug)
        if is_new:
            img = item.cssselect('a.product-image>img')[0].get('src')
            image = ''.join( self.extract_product_img.match(img).groups() )
            product.image_urls = [image]
            product.title = title

        price_box = item.cssselect('a>div.price-boxConfig')[0]
        special_price = price_box.cssselect('div.special-price')[0].strip().replace('$','').replace(',','')
        listprice = price_box.cssselect('div.old-price')[0].replace('original','').strip().replace('$','').replace(',','')
        soldout = item.cssselect('a.product-image>span.sold-out')
#        product.brand = sale_title
        product.price = special_price
        product.listprice = listprice
        if soldout: product.soldout = True
        product.updated = False
        product.list_update_time = datetime.utcnow()
        product.save()
        product_saved.send(sender=DB + '.crawl_listing', site=DB, key=lug, is_new=is_new, is_updated=not is_new)
        debug_info.send(sender=DB + ".crawl_listing", url=url)


    def crawl_product(self, url, casin):
        """.. :py:method::
            Got all the product information and save into the database

        :param url: product url
        """
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
#    server = zerorpc.Server(Server())
#    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
#    server.run()
    s = Server()
    s.crawl_category()
