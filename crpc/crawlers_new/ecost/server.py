#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawler.ecost.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client.py automatically, run on many differen ec2 instances.

"""
import os
import re
import sys
import time
import zerorpc
import logging
import requests
import traceback
import lxml.html
import logging
import log
import Queue
import string

from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from urllib import quote, unquote
from datetime import datetime, timedelta
from settings import *

sys.path.insert(0, os.path.abspath( os.path.dirname(__file__) ))
from common.stash import *


top_category = {
#    "Apple": "http://www.ecost.com/n/Apple-Computer/mainMenu-222006384",
    "Computers": "http://www.ecost.com/n/Computers/mainMenu-2045",
    "Networking": "http://www.ecost.com/n/Networking/mainMenu-222006880",
    "Electronics & Entertainment": "http://www.ecost.com/n/Electronics-And-Entertainment/mainMenu-222011888",
    "TV's, Monitors & Projectors": "http://www.ecost.com/n/Tvs-Monitors-And-Projectors/mainMenu-222007888",
    "Cameras & Camcorders": "http://www.ecost.com/n/Cameras-And-Camcorders/mainMenu-2754",
    "Memory & Storage": "http://www.ecost.com/n/Memory-And-Storage/mainMenu-2047",
    "Appliances": "http://www.ecost.com/n/Home-Appliances/mainMenu-3305",
    "Floor Care": "http://www.ecost.com/n/Floor-Care/mainMenu-3418",
    "Outdoor Fitness": "http://www.ecost.com/n/Outdoor-Gear/mainMenu-3390",
    "Personal Care": "http://www.ecost.com/n/Personal-Care/mainMenu-3391",
    "Watches": "http://www.ecost.com/n/Watches/mainMenu-3424",
    "Cookware": "http://www.ecost.com/s/Cookware?cc=CHC*,CH*,CHD*,CHE*,CHA*",
    "Cutlery": "http://www.ecost.com/s/Cutlery?cc=CI*,CIB*,CIA*,CIC*",
    "Home Decor": "http://www.ecost.com/s/Home-Decor?cc=CK*,CKAA,CKB*,CKF*,CKG*",
}

class Server(object):
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    def __init__(self):
        self.logger_category = log.init(DB + '_category', DB + '_category.txt')
        self.logger_list = log.init(DB + '_list', DB + '_list.txt')
        self.logger_product = log.init(DB + '_product', DB + '_product.txt')

    def get_main_category(self):
        """.. :py:method::
            put top category into queue
        """
        for top, link in top_category.items():
            self.queue.put(([top], link))
        self.queue.put((['Apple', 'iPod'], 'http://www.ecost.com/n/Apple-Ipod/mainMenu-2083'))

    def crawl_category(self):
        """.. :py:method::
            crawl ecost category
        """
        log.log_print('Initialization of ecost category cralwer.', self.logger_category, logging.INFO)
        self.queue = Queue.Queue()
        self.get_main_category()

        self.cycle_crawl_category(TIMEOUT)
        log.log_print('Close ecost category cralwer.', self.logger_category, logging.INFO)


    def cycle_crawl_category(self, timeover=60):
        """.. :py:method::
            read (category, link) tuple from queue, crawl sub-category, insert into the queue
        """
        while not self.queue.empty():
            try:
                job = self.queue.get(timeout=timeover)
                utf8_content = fetch_page(job[1])
                if not utf8_content: continue
                self.parse_category(job[0], job[1], utf8_content)
            except Queue.Empty:
                log.log_traceback(self.logger_category, 'Queue waiting {0} seconds without response!'.format(timeover))
            except:
                log.log_traceback(self.logger_category)


    def parse_category(self, category_list_path, url, content):
        """.. :py:method::
            parse the category in the page source
        """
        tree = lxml.html.fromstring(content)
        if tree.xpath('//img[@src="/croppedWidgets/images.browseCategoriesTitle.png"]'):
            # has 'BROWSE CATEGORIES' image
            categories = tree.xpath('//div[@class="nav-list wt"]/h2[@class="wt"]/span/a')
            if not categories:
                categories = tree.xpath('//body[@class="wbd"]/table/./tr[4]//tr/td/a[@class="wt"]')
                if not categories:
                    # http://www.ecost.com/n/Blu-Ray-Dvd-Player/mainMenu-3368
                    # treat as leaf
                    self.conn.set_leaf_category(category_list_path)
                    log.log_print('Special page {0}'.format(url), self.logger_category, logging.WARNING)
                    return

            for category in categories:
                link = category.get('href')
                name = category.text_content()
                if not link.startswith('http'):
                    link = 'http://www.ecost.com' + link

                # trap "Household Insulation":
                # ['Electronics & Entertainment', 'Audio & Video', 'Accessories', 'Receivers', 'Accessories', 'Receivers', ...
                if name in category_list_path:
                    continue

                cats = category_list_path + [name]
                log.log_print('category ==> {0}'.format(cats), self.logger_category)
                if self.conn.category_updated(' > '.join(cats)):
                    continue

                log.log_print('queue size ==> {0}'.format(self.queue.qsize()), self.logger_category)
                self.conn.insert_update_category(cats, link)
                self.queue.put((cats, link))
        else:
            # leaf node
            num = tree.xpath('//div[@class="searchHeaderDisplayTitle"]/span[1]/text()')
            if num:
                total_num = int(num[0])
                self.conn.set_leaf_category(category_list_path, total_num)
            else:
                log.log_traceback(self.logger_category, 'Not a valid page {0}'.format(url))
#                log.log_print('content: {0}'.format(content), self.logger_category, logging.DEBUG)
                return


    def crawl_listing(self, url, catstr, num=None):
        """.. :py:method::
            crawl list page to get part of products' info
        """
        content = fetch_page(url)
        if content:
            self.parse_listing(catstr, url, content, num)
        
    def crawl_product(self, url, ecost=''):
        """.. :py:method::
            crawl the detail page to get another part of products' info
        """
        content = fetch_page(url)
        if content:
            self.parse_product(url, content, ecost)
        
    def parse_listing(self, catstr, url, content, num):
        """.. :py:method::
            only for price. some special page don't have a item number.
            ITEM_PER_PAGE: 25 in setting.py
        """
        tree = lxml.html.fromstring(content)

        if not num:
            # special page, have 'BROWSE CATEGORIES', but is leaf node
            # price in listing page is not the same in product page.
            price = tree.xpath('//div[@class="noDisplayPricen"]//span[@class="itemFinalPrice wt14"]')
            prices = [p.text_content().strip().replace('$','').replace(',','') for p in price]
            links = tree.xpath('//span[@class="itemName wcB1"]/a')
            if len(prices) != len(links):
                log.log_traceback(self.logger_list, 'Special page: prices number != links number {0}'.format(url))
                raw_input()
            for j in xrange( len(links) ):
                href = links[j].get('href')
                if not href or not links[j].text_content().strip():
                    continue
                if not href.startswith('http'):
                    href = 'http://www.ecost.com' + href
                self.conn.title_link(links[j].text_content().strip(), href, prices[j])
            return

        total_num = int(tree.xpath('//div[@class="searchHeaderDisplayTitle"]/span[1]/text()')[0])
        page_num = (total_num - 1) // ITEM_PER_PAGE + 1

        if page_num == 0:
            log.log_print('Listing page do not have any items! -- {0}'.format(url), self.logger_list, logging.ERROR)
        elif page_num == 1:
            self.get_info(url, catstr, total_num, page_num)
        else:
            for i in xrange(1, page_num):
                self.get_info('{0}&op=zones.SearchResults.pageNo&pageNo={1}'.format(url, i), catstr, ITEM_PER_PAGE, i)
            self.get_info('{0}&op=zones.SearchResults.pageNo&pageNo={1}'.format(url, page_num), catstr, total_num % ITEM_PER_PAGE, page_num)


    def get_info(self, url, catstr, item_num, page_num):
        """  """
        content = fetch_page(url)
        tree = lxml.html.fromstring(content)
        nodes = tree.xpath('//div[@id="searchResultList"]/div[@class="sr-table_content"]')

        ecost = []
        models = []
        prices = []
        links = []
        for node in nodes:
            pnode = node.xpath('.//td[@class="rscontent"]/span')
            for p in pnode:
                l = p.xpath('./font[1]/text()')
                if l:
                    prices.append( l[0].replace('$', '').replace(',', '') )
                else:
                    prices.append('')
            m = node.xpath('.//td[@class="sr-item_img rscontent"]//span[@class="wt11 rsPartNo"]/text()')
            for i in m:
                temp = i.split(u'\xa0')
                # [u'eCOST Part #: 9106327 ', u' ', u' ', u' Mfr. Part #: 960-000866']
                ecost.append( temp[0].split(u':')[1].strip() )
                models.append( temp[-1].split(u':')[1].strip() if 'Mfr. Part' in temp[-1] else '' )

            link = node.xpath('.//td[@class="sr-item_img rscontent"]//span[@class="sr-item_description"]/h5/a/@href')
            for l in link:
                links.append( l if l.startswith('http') else 'http://www.ecost.com' + l )


        if item_num != len(ecost):
            log.log_traceback(self.logger_list, '{0} item_num: {1}, ecost_num: {2}, page_num: {3}'.format(url, item_num, len(ecost), page_num) )

        log.log_print('{0} {1} {2} {3} {4}'.format(len(ecost), len(models), len(prices), len(links), url), self.logger_list)
        timenow = datetime.utcnow()

        for j in xrange( len(ecost) ):
            # This rank changes all the time.If some product updated, some not, same rank on two products will happen!
            sell_rank = ITEM_PER_PAGE * (page_num-1) + j + 1
            try:
                price = string.atof( prices[j] )
            except ValueError as e:
                log.log_print(e, self.logger_list, logging.WARNING)
                price = ''
            except IndexError as e:
                log.log_print('{0}, index:{1}, prices:{2}'.format(e, j, prices), self.logger_list, logging.WARNING)

            try:
                self.conn.update_listing(ecost[j], models[j], price, sell_rank, links[j], catstr, timenow, updated=False)
            except:
                log.log_traceback(self.logger_list, '{0} item of {1} items. item_num: {2}'.format(j, len(ecost), item_num))

    

    def parse_product(self, url, content, ecost):
        tree = lxml.html.fromstring(content)

        title = tree.xpath('//h1[@class="prodInfo wt"]/text()')[-1]
        image = tree.xpath('//td[@width]/img[@src]/@src')[0]
        if image.startswith('//'):
            image = 'http' + image
        price = tree.xpath('//td[@class="leftPane"]//td[starts-with(@class, "infoPrice infoBorderContent")]//text()')
        if not price:
            price = tree.xpath('//td[@class="leftPane"]//td[@class="infoContent infoPrice wt15"]/text()')
        price = price[0].replace('$', '').replace(',', '') if price else ''

        self.info = {'ecost': '', 'model':'', 'shipping': '', 'available': '', 'platform': '', 'manufacturer': '', 'upc': '', 'review': 0, 'rating': ''}
        node = tree.xpath('//td[@class="rightPane"]/table//tr')
        for tr in node:
            name = tr.xpath('./td[@class="infoLabel"]/text()')
            if name:
                self.label_value(name, tr)

        tables = tree.xpath('//div[@class="simpleTab06 wt11 wcGray1"]/div[@id="pdpTechSpecs"]//tr[@class="dtls"]')
        specifications = dict(t.text_content().strip().split('\n\t\t\t\t') for t in tables)

        try:
            self.conn.update_product(title, image, price, ecost, self.info['model'], self.info['shipping'], self.info['available'], self.info['platform'], self.info['manufacturer'], self.info['upc'], self.info['review'], self.info['rating'], specifications)
        except:
            log.log_traceback(self.logger_product, '{0} {1}'.format(url, self.info))


    def label_value(self, name, tr):
        if name == ['eCOST Part#:']:
            ecost = tr.xpath('./td[@class="infoContent wcGray2"]/text()')
            if ecost:
                self.info['ecost'] = ecost[0]
            else:
                self.info['ecost'] = ''
        elif name == ['Mfr Part#:']:
            model = tr.xpath('./td[@class="infoContent wcGray2"]/text()')
            if model:
                self.info['model'] = model[0]
            else:
                self.info['model'] = ''
        elif name == ['Usually Ships:']:
            shipping = tr.xpath('./td[@class="infoContent"]//td[1]/a/text()')
            if shipping:
                self.info['shipping'] = shipping[0]
            else:
                self.info['shipping'] = ''
        elif name == ['Availability:']:
            available = tr.xpath('./td[@class="infoLink"]/a/text()')
            if available:
                self.info['available'] = available[0]
            else:
                self.info['available'] = ''
        elif name == ['Platform:']:
            platform = tr.xpath('./td[@class="infoContent wcGray2"]/text()')
            if platform:
                self.info['platform'] = platform[0]
            else:
                self.info['platform'] = ''
        elif name == ['Manufacturer:']:
            manufacturer = tr.xpath('./td[@class="infoLink wcGray2"]/a/text()')
            if manufacturer:
                self.info['manufacturer'] = manufacturer[0]
            else:
                self.info['manufacturer'] = ''
        elif name == ['UPC:']:
            upc = tr.xpath('./td[@class="infoContent wcGray2"]/text()')
            if upc:
                self.info['upc'] = upc[0]
            else:
                self.info['upc'] = ''
        elif name == ['Customer Rating:']:
            rate = tr.xpath('./td[@class="infoContent wcGray2"]/span[@class="list-ratingy"]')
            if rate:
                self.info['review'] = int( rate[0].text_content().strip().replace('(', '').replace(')', '') )
                self.info['rating'] = rate[0].xpath('.//li/@style')[0].split(':')[-1]
#            elif tr.xpath('./td[@class="infoContent wcGray2"]/span[@class="list-ratingn"]'):
            else:
                self.info['review'] = 0
                self.info['rating'] = ''



if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
    server.run()
