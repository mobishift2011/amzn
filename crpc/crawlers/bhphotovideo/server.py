#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool

import os
import re
import sys
import time
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

class Server:
    def __init__(self):
        self.conn = conn_mongo.conn_mongo(DB, DB_HOST)
        self.product = self.conn.get_product_col('product')
        self.conn.index_unique(self.product, 'bah')
        self.logger_category = log.init('bhphotovideo_category', 'bhphotovideo_category.txt')
        self.logger_list = log.init('bhphotovideo_list', 'bhphotovideo_list.txt')
        self.logger_product = log.init('bhphotovideo_product', 'bhphotovideo_product.txt')

    def clear(self):
        self.conn.close_mongo()

    def get_main_category(self):
        bhurl = 'http://www.bhphotovideo.com'
        content = self.fetch_page(bhurl)
        tree = lxml.html.fromstring(content)
        links = tree.xpath('//div[@class="mainCategoryLinks"]//li/a/@href')
        names = tree.xpath('//div[@class="mainCategoryLinks"]//li/a/span/text()')
        self.mainCategory = dict(zip(names, links))


    def crawl_category(self):
        """ crawl category """
        self.get_main_category()

        self.queue = Queue.Queue()
        self.category = self.conn.get_category_col('category')
        self.conn.index_unique(self.category, 'catstr')
        log.log_print('Initialization of bhphotovideo category cralwer.', self.logger_category, logging.INFO)
        for top_category, url in self.mainCategory.items():
            self.conn.set_update_flag(top_category)
            self.queue.put(([top_category], url))
        self.cycle_crawl_category(TIMEOUT)
        log.log_print('Close bhphotovideo category cralwer.', self.logger_category, logging.INFO)

    def cycle_crawl_category(self, timeover=60):
        while not self.queue.empty():
            try:
                job = self.queue.get(timeout=timeover)
                utf8_content = self.fetch_page(job[1])
                self.parse_category(job[0], job[1], utf8_content)
                time.sleep(0.5)
            except Queue.Empty:
                log.log_traceback(self.logger_category, 'Queue waiting {0} seconds without response!'.format(timeover))
            except:
                log.log_traceback(self.logger_category)


    def parse_category(self, category_list_path, url, content):
        tree = lxml.html.fromstring(content)

        items = tree.xpath('//div[@class="tMain"]//div[@class="column"]//li/a')
        if not items:
            # second kind of category page
            items = tree.xpath('//div[@class="tMain"]//table[@class="catColumn"]//tr[@valign="top"]//a')

        if items:
            links = [item.get('href') for item in items]
            names = [item.text_content() for item in items]
        else:
            # third kind of category page
            items = tree.xpath('//div[@id="mainContent"]//div[@class="categoryGroup staticBody"]/div/a')
            if items:
                links = [item.get('href') for item in items]
                names = [item.xpath('.//img')[0].get('alt') for item in items]
            else:
                links, names = [], []

                try:
                    # listing page
                    num = tree.xpath('//div[@class="tMain"]//div[@id="Plistbar"]/div[@id="PfirstRow"]/span[@id="PitemNum"]/text()')[0]
                    total_num = int(num.replace('\t', '').strip().split('\n')[-1].split()[0])

                    self.conn.set_leaf_category(category_list_path, total_num)
                except:
                    log.log_traceback( self.logger_category, '!! {0} neither a category nor a listing page.Or other errors.'.format(url) )
                    log.log_print('content: {0}'.format(content), self.logger_category, logging.DEBUG)
                    return

        pairs = []
        if len(links) != len(names):
            log.log_traceback(self.logger_category, '!! links num: {0}; names num: {1}. {2}'.format(len(links), len(names), url))
            return
        else:
            pairs = zip(names, links)

        for category, link in pairs:

            # trap "Household Insulation":
            # http://www.amazon.com/s/ref=sr_ex_n_1?rh=n%3A228013%2Cn%3A!468240%2Cn%3A551240%2Cn%3A495346&bbn=495346&ie=UTF8&qid=1344909516
            if category_list_path[-1] == category:
                continue

            cats = category_list_path + [category]
            log.log_print('category ==> {0}'.format(cats), self.logger_category)
            if self.conn.category_updated(' > '.join(cats)):
                continue

            log.log_print('queue size ==> {0}'.format(self.queue.qsize()), self.logger_category)
            self.conn.insert_update_category(cats, link)
            self.queue.put((cats, link))


    def crawl_listing(self, url, catstr):
        content = self.fetch_page(url)
        self.parse_listing(catstr, url, content)
        
    def crawl_product(self, bah, url):
        content = self.fetch_page(url)
        self.parse_product(bah, url, content)
        
    def fetch_page(self, url):
        return s.get(url).content
    
    def parse_listing(self, catstr, url, content):
        """ ITEM_PER_PAGE: 25 in setting.py """
        tree = lxml.html.fromstring(content)
        try:
            num = tree.xpath('//div[@class="tMain"]//div[@id="Plistbar"]/div[@id="PfirstRow"]/span[@id="PitemNum"]/text()')[0]
            total_num = int(num.replace('\t', '').strip().split('\n')[-1].split()[0])
        except:
            log.log_traceback(self.logger_list, '!* Do not get item numbers of category [{0}]: {1}'.format(catstr, url))
#            print content
            time.sleep(30)
            return

        log.log_print('{0} items in {1}'.format(total_num, url), self.logger_list)

        page_num = (total_num - 1) // ITEM_PER_PAGE + 1
        if page_num == 0:
            log.log_print('Listing page do not have any items! -- {0}'.format(url), self.logger_list, logging.ERROR)
        elif page_num == 1:
            self.get_info(url, catstr, total_num, page_num)
        else:
            part1 = '/'.join( url.split('/')[:-2] )
            part2 = '/'.join( url.split('/')[-2:] )
            for i in xrange(1, page_num):
                self.get_info(part1 + '/pn/{0}/'.format(i) + part2, catstr, ITEM_PER_PAGE, i)
                time.sleep(0.5)
            self.get_info(part1 + '/pn/{0}/'.format(page_num) + part2, catstr, total_num % ITEM_PER_PAGE, page_num)
        time.sleep(0.5)


    def get_info(self, url, catstr, item_num, page_num):
        """  """
        content = self.fetch_page(url)
        tree = lxml.html.fromstring(content)
        try:
            iter_ret = tree.xpath('//div[@class="tMain"]//div[starts-with(@class, "productBlock clearfix ")]')
        except:
            log.log_traceback(self.logger_list, 'Error xpath or page: {0}'.format(url))
            return

        timenow = datetime.utcnow()
        time_diff = timedelta(1)

        bahs = []
        best_sell_ranks = []
        images = []
        urls = []
        reviews = []
        brands = []
        titles = []
        highlights = []
        available = []
        models = []
        prices = []
        shippings = []

        if len(iter_ret) != item_num:
            log.log_traceback(self.logger_list, '{0} item_num: {1}, actual_num: {2}, page_num: {3}'.format(url, item_num, len(iter_ret), page_num) )
            if len(iter_ret) == 0:
                time.sleep(30)
                return

        for j in xrange(len(iter_ret)):

            try:
                bah = iter_ret[j].xpath('.//div[@class="productBlockCenter"]/div[@class="points"]//li[1]/span[@class="value"]/text()')[0]
            except:
                log.log_traceback(self.logger_list, '!* {0} of {1} did not get b&h number {2}'.format(j+1, item_num, url))
                log.log_print('content: {0}'.format(content), self.logger_list, logging.DEBUG)
                continue

            # product exist and without update less than 1 day, continue without update
            product = self.conn.get_product(bah)
            if product:
                if time_diff > (timenow - product['update_time']):
                    continue

            bahs.append(bah)
            # This rank changes all the time.If some product updated,some not, same rank on two products will happen!
            best_sell_ranks.append( ITEM_PER_PAGE * (page_num-1) + j + 1 )

            try:
                node = iter_ret[j].xpath('.//div[@class="productBlockLeft"]')[0]
                try:
                    image = node.xpath('./a/img/@src')[0]
                    if image:
                        images.append('http://www.bhphotovideo.com' + image)
                    else:
                        images.append('')
                except:
                    images.append('')
                    log.log_traceback(self.logger_list)

                try:
                    link = node.xpath('./a/@href')[0]
                    if link:
                        urls.append(link)
                    else:
                        urls.append('')
                except:
                    urls.append('')
                    log.log_traceback(self.logger_list)

                try:
                    review = node.xpath('./div[@class="ratingBox"]/a[@class="info"]/text()')
                    if review:
                        m =re.compile('\d+').search(review[0])
                        reviews.append(m.group())
                    else:
                        reviews.append('')
                except:
                    reviews.append('')
                    log.log_traceback(self.logger_list)
            except:
                log.log_traceback(self.logger_list)


            try:
                node = iter_ret[j].xpath('.//div[@class="productBlockCenter"]')[0]
                try:
                    brand = node.xpath('./div[@class="clearfix"]/div[@class="brandTop"]/text()')[0]
                    if brand:
                        brands.append(brand)
                    else:
                        brands.append('')
                except:
                    brands.append('')
                    log.log_traceback(self.logger_list)

                try:
                    title = node.xpath('./div[@id="productTitle"]//a/text()')[0]
                    if title:
                        titles.append(title)
                    else:
                        titles.append('')
                except:
                    titles.append('')
                    log.log_traceback(self.logger_list)

                try:
                    desc = node.xpath('./ul/li')
                    desc = [d.text_content() for d in desc]
                    if desc:
                        highlights.append(desc)
                    else:
                        highlights.append([])
                except:
                    highlights.append([])
                    log.log_traceback(self.logger_list)

                try:
                    avail = node.xpath('.//div[@class="availability"]//text()')
                    avail = [a.strip() for a in avail if not a.isspace()]
                    if avail:
                        available.append(avail)
                    else:
                        available.append([])
                except:
                    available.append([])
                    log.log_traceback(self.logger_list)

            except:
                log.log_traceback(self.logger_list)

            try:
                model = iter_ret[j].xpath('.//div[@class="productBlockCenter"]/div[@class="points"]//li[2]/span[@class="value"]/text()')
                if model:
                    models.append(model[0])
                else:
                    models.append('')
            except:
                models.append('')
                log.log_traceback(self.logger_list)

            try:
                price = iter_ret[j].xpath('.//div[@id="productRight"]/ul[starts-with(@class, "priceList ")]/li[@class]/span[@class="value"]/text()')
                if price:
                    price = price[0].replace(',', '').replace('$', '') 
                else:
                    price = iter_ret[j].xpath('.//div[@id="productRight"]/ul[@class="priceList "]/li[@class="map youPay"]/span[@class="value"]/text()')
                    if price:
                        price = price[0].strip().replace(',', '').replace('$', '')
                    else:
                        data_href = iter_ret[j].xpath('.//div[@id="productRight"]/ul[@class="priceList priceContainer"]/li[contains(@class, "cartLinkPrice")]/@data-href')
                        if data_href:
                            param0, param1 = ['string:{0}'.format(i) for i in data_href[0].split('_')]
                            page = '/' + '/'.join(url.split('/')[3:])
                            cinum = url.split('/')[7]
                            param3 = 'string:cat@__{0}@__type@__PrdLst'.format(cinum)
                            param4 = 'string:' + cinum
                            post_data = { 
                                'c0-methodName': 'addToCart',
                                'c0-scriptName': 'DWRHelper',
                                'c0-id': '0',
                                'batchId': '10',
                                'callCount': '1',
                                'windowName': 'bhmain',
                                'page': page,
                                'httpSessionId': 'wwh9QYSPBd!-1310320805',
                                'scriptSessionId': '60F4DF55163FC3A41DF6C7B70D572C73',
                                'c0-param0': param0,
                                'c0-param1': param1,
                                'c0-param2': 'string:1',
                                'c0-param3': param3,
                                'c0-param4': param4
                            }       
                            jsurl = 'http://www.bhphotovideo.com/bnh/dwr/call/plaincall/DWRHelper.addToCart.dwr'
                            sess = requests.session()
                            resp_cont = sess.post(jsurl, data=post_data).content
                            m = re.compile(r'<span class=\\"atcLayerPricePrice\\">(.*?)</span>').search(resp_cont)
                            price = m.group(1).replace('\\n', '').replace(' ', '').replace(',', '').replace('$', '')

                if price:
                    prices.append(price)
                else:   
                    prices.append('')
            except:
                prices.append('')
                log.log_traceback(self.logger_list)


            try:
                shipping = iter_ret[j].xpath('.//div[@id="productRight"]/ul[contains(@class, "priceList ")]/li[last()]/a/text()')
                if shipping:
                    shippings.append(shipping[0])
                else:
                    shippings.append('')
            except:
                shippings.append('')
                log.log_traceback(self.logger_list)


        log.log_print('{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12}'.format(len(bahs),len(best_sell_ranks),len(images),len(urls),len(reviews),len(brands),len(titles),len(highlights),len(available),len(models),len(prices),len(shippings),url), self.logger_list)
        update_now = datetime.utcnow()
        try:
            for i in xrange(len(bahs)):
                self.conn.update_listing(bahs[i], images[i], urls[i], reviews[i], brands[i], titles[i], highlights[i], available[i], models[i], prices[i], shippings[i], best_sell_ranks[i], catstr, update_now, detail_parse=False)
        except:
            log.log_traceback(self.logger_list, '{0} item of {1} items'.format(i, item_num))
        

    

    def parse_product(self, bah, url, content):
        tree = lxml.html.fromstring(content)
        try:
            node = tree.xpath('//div[@class="tMain"]//div[@id="productAllWrapper"]/div[@id="productMainWrapper"]')
            if node: node = node[0]
            else: return
        except:
            log.log_traceback(self.logger_product, 'Product have problem when parsing: {0}'.format(url))

        bill_later = node.xpath('.//div[@id="productRight"]//div[contains(@class, "altPayment findLast")]//li/a//text()')
        bill_later = [a.strip() for a in bill_later]

        info = []
        buy_together = tree.xpath('.//div[@class="productInfoArea adm findLast"]/a/@href')
        if buy_together:
            content = self.fetch_page(buy_together[0])
            intree = lxml.html.fromstring(content)
            ones = intree.xpath('//div[@class="ui-dialog-content"]//div[@class="col titleDetails"]')
            for one in ones:
                title = one.xpath('./div[@class="title"]/span//text()')
                info = [t.strip() for t in title if t.strip()]
                model = one.xpath('./div[@class="details"]/p/text()')
                info.append(model[0])
        buy_together = info

        specifications = {}
        tables = node.xpath('.//div[@id="bottomWrapper"]//div[@id="Specification"]//table[@class="specTable"]')
        for table in tables:
            key = table.xpath('.//tr/td[@class="specTopic"]')
            value = table.xpath('.//tr/td[@class="specDetail"]')
            k = [k.text_content().strip() for k in key]
            v = [v.text_content().strip().replace('\n', '') for v in value]
            specifications.update( dict(zip(k, v)) )

        in_box = node.xpath('.//div[@id="bottomWrapper"]//div[@id="WhatsInTheBox"]/ul/li')
        in_box = [a.text_content().strip() for a in in_box]

        rating = node.xpath('.//div[@id="bottomWrapper"]//div[@id="costumerReview"]//div[@class="pr-snapshot-rating rating"]/span/text()')
        if rating:
            rating = rating[0]
        else:
            rating = ''

#        items = node.xpath('.//div[@id="bottomWrapper"]//div[@class="accGroup "]//form[@class="addToCartForm"]//div[@class="accDetails"]')
#        for item in items:
#            title = item.xpath('./div[1]')
#            title[0].text_content()
#            model = item.xpath('./div[@class="ItemNum"]/span')
#            model[0].text_content()



        self.conn.update_product(bah, bill_later, specifications, in_box, rating, buy_together)
        time.sleep(1)


if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(CRAWLER_PORT))
    server.run()
