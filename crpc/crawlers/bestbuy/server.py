#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool

import os
import re
import sys
import time
import redis
import zerorpc
import logging
import requests
import traceback
import lxml.html
import conn_mongo
import logging
import log
import Queue

from urllib import quote, unquote
from datetime import datetime, timedelta

from settings import *

s = requests.Session()

categories = {'TV & Home Theater': 'http://www.bestbuy.com/site/Electronics/TV-Video/abcat0100000.c?id=abcat0100000',
    'Audio & MP3': 'http://www.bestbuy.com/site/Electronics/Audio/abcat0200000.c?id=abcat0200000',
    'Mobile Phones': 'http://www.bestbuy.com/site/Electronics/Mobile-Cell-Phones/abcat0800000.c?id=abcat0800000',
    'Cameras & Camcorders': 'http://www.bestbuy.com/site/Electronics/Cameras-Camcorders/abcat0400000.c?id=abcat0400000',
    'Computers & Tablets': 'http://www.bestbuy.com/site/Electronics/Computers-PCs/abcat0500000.c?id=abcat0500000',
    'Car, Marine & GPS': 'http://www.bestbuy.com/site/Electronics/Car-Audio-GPS/abcat0300000.c?id=abcat0300000',
    'Office': 'http://www.bestbuy.com/site/Electronics/Office/pcmcat245100050028.c?id=pcmcat245100050028',
    'Health, Fitness & Sports': 'http://www.bestbuy.com/site/Electronics/Health-Fitness/pcmcat242800050021.c?id=pcmcat242800050021',
    'Movies & Music': 'http://www.bestbuy.com/site/Electronics/Music-Movies/abcat0600000.c?id=abcat0600000',
    'Musical Instruments': 'http://www.bestbuy.com/site/Audio/Musical-Instruments/abcat0207000.c?id=abcat0207000',
    'Video Games': 'http://www.bestbuy.com/site/Electronics/Video-Games/abcat0700000.c?id=abcat0700000',
    'Home': 'http://www.bestbuy.com/site/Electronics/Home/pcmcat248700050021.c?id=pcmcat248700050021',
    'Appliances': 'http://www.bestbuy.com/site/Electronics/Home-Appliances/abcat0900000.c?id=abcat0900000'}

class Server:
    def __init__(self):
        self.conn = conn_mongo.conn_mongo(DB, DB_HOST)
        self.product = self.conn.get_product_col('product')
        self.conn.index_unique(self.product, 'sku')
        self.logger_category = log.init('bestbuy_category', 'bestbuy_category.txt')
        self.logger_list = log.init('bestbuy_list', 'bestbuy_list.txt')
        self.logger_product = log.init('bestbuy_product', 'bestbuy_product.txt')

    def clear(self):
        self.conn.close_mongo()


    # crawl bestbuy category
    def crawl_category(self):
        self.queue = Queue.Queue()
        self.category = self.conn.get_category_col('category')
        self.conn.index_unique(self.category, 'catstr')
        log.log_print('Initialization of bestbuy category cralwer.', self.logger_category, logging.INFO)
        for top_category, url in categories.items():
            self.conn.set_update_flag(top_category)
            self.queue.put(([top_category], url))
        self.cycle_crawl_category(TIMEOUT)
        log.log_print('Close bestbuy category cralwer.', self.logger_category, logging.INFO)

    def cycle_crawl_category(self, timeover=60):
        while not self.queue.empty():
            try:
                job = self.queue.get(timeout=timeover)
                utf8_content = self.fetch_page(job[1])
                self.parse_category(job[0], job[1], utf8_content)
            except Queue.Empty:
                log.log_traceback(self.logger_category, 'Queue waiting {0} seconds without response!'.format(timeover))
            except:
                log.log_traceback(self.logger_category)

    def parse_category(self, category_list_path, link, content):
        tree = lxml.html.fromstring(content)

        items = tree.xpath('//div[@class="narrowcontent"]//a[@class="headlink"]')
        if not items:
            try:
                total_num = tree.xpath('//div[@id="rightcol"]//div[@id="top-padbar"]/div/strong[2]')[0].text
                self.conn.set_leaf_category(category_list_path, int(total_num))
            except:
                log.log_traceback(self.logger_category, '!* Do not get how many items of this category: {0}'.format(link))

        for item in items:
            category_link = item.get('href')
            if category_link:
                url = 'http://www.bestbuy.com' + category_link
            else:
                url = ''

            category = item.text.strip('\n')
            # trap "Household Insulation":
            # http://www.amazon.com/s/ref=sr_ex_n_1?rh=n%3A228013%2Cn%3A!468240%2Cn%3A551240%2Cn%3A495346&bbn=495346&ie=UTF8&qid=1344909516
            if category_list_path[-1] == category:
                continue

            cats = category_list_path + [category]
            log.log_print('category ==> {0}'.format(cats), self.logger_category)
            if self.conn.category_updated(' > '.join(cats)):
                continue

            if url:
                log.log_print('url ==> {0}'.format(url), self.logger_category)
            else:
                log.log_print('url ==> {0}'.format(url), self.logger_category, logging.ERROR)
            log.log_print('queue size ==> {0}'.format(self.queue.qsize()), self.logger_category)
            self.conn.insert_update_category(cats, url)
            self.queue.put((cats, url))


    def crawl_listing(self, url, catstr):
        content = self.fetch_page(url)
        self.parse_listing(catstr, url, content)
        
    def crawl_product(self, sku, url):
        content = self.fetch_page(url)
        self.parse_product(sku, url, content)
        
    def fetch_page(self, url):
        return s.get(url).content
    
    def parse_listing(self, catstr, url, content):
        """ parse listing page to get each product -> db """
        item_per_page = 15
        tree = lxml.html.fromstring(content)
        try:
            total_num = tree.xpath('//div[@id="rightcol"]//div[@id="top-padbar"]/div/strong[2]')[0].text
        except:
            log.log_traceback(self.logger_list, '!* Do not get how many items of this category: {0}'.format(url))
            return

        num = int(total_num)
        log.log_print('{0} items in {1}'.format(num, url), self.logger_list)

        page_num = (num - 1) // item_per_page + 1
        if page_num == 0:
            log.log_print('Listing page do not have any items! -- {0}'.format(url), self.logger_list, logging.ERROR)
        elif page_num == 1:
            self.get_info(url, catstr, num, page_num, item_per_page)
        else:
            for i in xrange(1, page_num):
                self.get_info('{0}&gf=y&cp={1}'.format(url, i), catstr, item_per_page, i, item_per_page)
            self.get_info('{0}&gf=y&cp={1}'.format(url, page_num), catstr, num % item_per_page, page_num, item_per_page)


    def get_info(self, url, catstr, item_num, page_num, item_per_page):
        
        """  """
        content = self.fetch_page(url)
        tree = lxml.html.fromstring(content)
        try:
            iter_ret = tree.xpath('//div[@id="rightcol"]//div[@id="listView"]')[0]
            # [<Element div at 0x1d8a7d0>] <Element div at 0x1d8a7d0>

            sku = [n.strip('\n') for n in iter_ret.xpath('.//div[@class="info-main"]/div[@class="attributes"]//strong[@class="sku"]/text()')]
        except:
            iter_ret = tree.xpath('//div[@id="container"]//div[@id="rightcol"]//div[@id="listView"]')
            if iter_ret:
                log.log_print('We need add container to xpath', self.logger_list, logging.ERROR)
            log.log_traceback(self.logger_list, 'Error when parse page: {0}'.format(url))
            return

        timenow = datetime.utcnow()
        time_diff = timedelta(1)
        images = []
        prices = []
        titles = []
        urls = []
        manufacturers = []
        models = []
        description = []
        rating = []
        review = []
        available = []
        marketplace = []
        for j in range(1, item_num + 1):
            # product exist and without update less than 1 day, continue without update
            # but sku's length is alway full(e.g. 15)
#            product = self.conn.get_product(sku[j-1])
#            if product:
#                if time_diff > (timenow - product['update_time']):
#                    continue

            try:
                node = iter_ret.xpath('.//div[@class="hproduct"][{0}]'.format(j))[0]
            except:
                log.log_traceback(self.logger_list, 'Product number[{0}] did not get'.format(item_num))
                continue

            try:
                image = node.xpath('.//div[@class="image-col"]/a/img/@src')
                if image:
                    images.append(image[0])
                else:
                    images.append('')
            except:
                images.append('')
                log.log_traceback(self.logger_list)

            try:
                price = node.xpath('.//div[@class="info-side"]//span[@itemprop="price"]/text()')
                if price:
                    prices.append(price[0])
                else:
                    info_id = node.xpath('.//div[@class="info-side"]//a[contains(@href, "viewPrice")]/@href')
                    if info_id:
                        # javascript:bbyCartController.viewPrice('{skuId:2658068,productId:1218343212620}')
                        info_id = info_id[0].split('{')[-1].split('}')[0].split(',') # ['skuId:2658068', 'productId:1218343212620']
                        info = [lid.split(':') for lid in info_id]
                        price_url = 'http://www.bestbuy.com/site/olspage.jsp?{0}={1}&{2}={3}&id=pcat18005&type=page&renderMapCart=true'.format(info[0][0], info[0][1], info[1][0], info[1][1])

                        price_page = self.fetch_page(price_url)
                        price_page_tree = lxml.html.fromstring(price_page)
                        price_hide = price_page_tree.xpath('//div[@class="bby-price css-price bdt-price"]//span[@itemprop="price"]/text()')
                        prices.append(price_hide[0])
                    else:
                        prices.append('')
            except:
                prices.append('')
                log.log_traceback(self.logger_list)

            try:
                title = node.xpath('.//div[@class="info-main"]/h3[@itemprop="name"]/a')
                # //text() '\nEnergizer - Disney ', '<b>Cars</b>', ' LED Handheld Flashlight - Red/Black'
                if title:
                    titles.append(title[0].text_content().lstrip('\n'))
                    urls.append(title[0].get('href'))
                else:
                    titles.append('')
                    urls.append('')
            except:
                titles.append('')
                urls.append('')
                log.log_traceback(self.logger_list)

            try:
                manufacturer = node.xpath('.//div[@class="info-main"]/span[@itemprop="manufacturer"]/span/@content')
                if manufacturer:
                    manufacturers.append(manufacturer[0])
                else:
                    manufacturers.append('')
            except:
                manufacturers.append('')
                log.log_traceback(self.logger_list)

            try:
                model = node.xpath('.//div[@class="info-main"]/div[@class="attributes"]//strong[@itemprop="model"]/text()')
                if model:
                    models.append(model[0])
                else:
                    models.append('')
            except:
                models.append('')
                log.log_traceback(self.logger_list)

            try:
                desc = node.xpath('.//div[@class="info-main"]/div[@class="description"]')
                if desc:
                    description.append(desc[0].text_content())
                else:
                    description.append('')
            except:
                description.append('')
                log.log_traceback(self.logger_list)

            try:
                rate = node.xpath('.//div[@class="info-main"]/div[@class="rating"]')
                if rate:
                    # [u'\nCustomer Reviews:\n\xa0\nBe\nthe first to write a review.\n']
                    rate_ = rate[0].text_content().split('\n', 2)[-1].strip()
                    r_ = rate_.split('\n')
                    if r_[0] == u'Be':
                        # u'Be\nthe first to write a review.'
                        rating.append('')
                        review.append('')
                    else:
                        # '3  of 5\n\n(2 reviews)'
                        rating.append(r_[0])
                        review.append(r_[-1].lstrip('(').rstrip(')'))
                else:
                    # combination, monitor and a host
                    rating.append(None)
                    review.append(None)
            except:
                rating.append('')
                review.append('')
                log.log_traceback(self.logger_list)

            try:
                avail = node.xpath('.//div[@class="info-main"]/div[@class="availHolder"]//div[@class="tooltip-contents"]/p/text()')
                # ['  Usually leaves our warehouse in 1 business day ', '\n\n', u'\xa0\n\n\n\n\n\n\n', '\n'], [' Not available', '\n\n\n', u' Not Available\xa0\n', 'Find it at a  Best Buy store.\n', '\n'], ['\n', ': Seller usually ships within 1-2 business days'], ['\n', '  Usually leaves our warehouse in 1 business day'], ['\n', ' You will schedule your delivery date in the next step.\n\n\n\n\n\n', '\n', '\n\n\n', u' Not Available\xa0\n'], ['\n', ' You will schedule your delivery date in the next step.\n\n\n\n\n\n', '\n', '\n\n\n', u' Not Available\xa0\n\n', 'Find it at a  Best Buy store.', '\n'], [' ', 'Not Available for Shipping ', '\n\n\n', u'\xa0\n\n\n\n\n\n\n', '\n']]
                if not avail:
                    avail = node.xpath('.//div[@class="info-main"]/div[@class="availHolder"]/a/span/text()')
                if not avail:
                    available.append('')
                else:
                    if avail[0] == '\n' or avail[0] == ' ':
                        available.append(avail[1].split(':')[-1].strip())
                    else:
                        available.append(avail[0].strip())
            except:
                available.append('')
                log.log_traceback(self.logger_list)

            try:
                mrkpl = node.xpath('.//div[@class="info-main"]/div[@class="mrkpl"]//dd[@class="seller_info "]/a/text()')
                # [], ['\nBuy.com\n']
                if mrkpl:
                    marketplace.append(mrkpl[0].strip('\n'))
                else:
                    marketplace.append('')
            except:
                marketplace.append('')
                log.log_traceback(self.logger_list)

        log.log_print('{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}'.format(len(images),len(prices),len(titles),len(urls),len(manufacturers),len(models),len(sku),len(description),len(rating),len(review),url), self.logger_list)
        update_now = datetime.utcnow()
        for i in xrange(item_num):
            try:
                best_sell = item_per_page * (page_num-1) + i + 1
                self.conn.update_listing(sku[i], images[i], prices[i], titles[i], urls[i], manufacturers[i], models[i], description[i], rating[i], review[i], best_sell, catstr, update_now, detail_parse=False)
            except:
                log.log_traceback(self.logger_list, '{0} item of {1} items'.format(i, item_num))
        

    

    def parse_product(self, sku, url, content):
        tree = lxml.html.fromstring(content.decode('utf-8','replace'))
        try:
            node = tree.xpath('//div[@id="content"]/div[@id="pdpcenterwell"]')[0]
        except:
            log.log_traceback(self.logger_product, 'Product have problem when parsing: {0}'.format(url))
            return

        #item = node.xpath('.//div[@id="productsummary"]/div[@id="financing"]//li/a/text()') # will add a \n to the tail of every field
        offer= node.xpath('.//div[@id="productsummary"]/div[@id="financing"]//li/a')
        #['\n18-Month Financing', '\nGet 4% Back in Rewards: See How']
        if offer:
            offers = [a.text_content().strip() for a in offer]
        else:
            offers = []

        specifications = []
        try:
            specifications = node.xpath('.//div[@id="productdetail"]/div[@id="pdptabs"]/div[@id="tabbed-specifications"]//li/div//text()')
#            if specification:
#
#                spec = []
#                for a in specification:
#                    if 'Customer Reviews' in a:
#                        break
#                    if a != '\n':
#                        spec.append( a.strip('\n') )
#
#                length = len(spec)
#                i = 0 
#                key = ''
#                while i < length:
#                    if i + 2 < length and spec[i+2] == ' ':
#                        # mulit value pair: ['software include', 'vim', ' ', 'emacs', ' ', 'process', 'intel']
#                        if key:
#                            specifications[key].append(spec[i+1])
#                        else:
#                            specifications[ spec[i] ] = [ spec[i+1] ]
#                            key = spec[i]
#                        # print key, specifications[key]
#                    else:
#                        # normal pair: ['cpu', 'amd', 'brand', 'dell']
#                        key = ''
#                        if spec[i] is ' ' or spec[i] is '':
#                            # ['Estimated Yearly Operating Cost', '$17', '', 'UPC', '600603146435', ' ', '']
#                            i += 1
#                            if i >= length: # last item is ' '
#                                break
#                            continue
#                        else:
#                            specifications[ spec[i] ] = spec[i+1]
#                            # print spec[i], specifications[ spec[i] ]
#                    i += 2
        except:
            log.log_traceback(self.logger_product, 'Product specifications parsing problem: {0}'.format(url))

        self.conn.update_product(sku, offers, specifications)


if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
    server.run()
