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
import logging
import log
import Queue

from urllib import quote, unquote
from datetime import datetime, timedelta

from settings import *
from models import *


headers = {
    'User-Agent': 'Mozilla 5.0/Firefox 15.0.1',
}

config = { 
    'max_retries': 3,
    'pool_connections': 10, 
    'pool_maxsize': 10, 
}

s = requests.Session(prefetch=True, timeout=15, config=config, headers=headers)

def url2catname2catn(url):
    """ catname, catn = m.groups() """
    m = re.compile(r'http://www.cabelas.com/catalog/browse/(.*?)/?_/N-(\d+)').match(url)
    return m.groups()

class Server:
    def __init__(self):
        self.logger_category = log.init(DB + '_category', DB + '_category.txt')
        self.logger_list = log.init(DB + '_list', DB + '_list.txt')
        self.logger_product = log.init(DB + '_product', DB + '_product.txt')


    def get_main_category(self):
        """ get the top categories """
        caburl = 'http://www.cabelas.com'
        content = self.fetch_page(caburl)
        tree = lxml.html.fromstring(content)
        nodes = tree.xpath('//div[@id="siteHeader"]//div[@id="defaultHeader"]/div[@id="MegaMenuHeader"]//li[@class="js-navLink"]')
        links, names = [], []
        for node in nodes:
            link = node.xpath('./a/@href')
            if not link[0].startswith('http'):
                link[0] = caburl + link[0]
            links.append(link[0])
            name = node.xpath('./a/img/@alt')
            catstr = name[0].replace('and', '&')
            names.append(catstr)

            catname, catn = url2catname2catn(link[0])
            c = Category.objects(catn=catn)
            if catname:
                c.catname = catname
            c.cats = [catstr]
        self.mainCategory = dict(zip(names, links))


    def crawl_category(self):
        """ crawl category """
        self.get_main_category()

        log.log_print('Initialization of cabelas category cralwer.', self.logger_category, logging.INFO)
        self.queue = Queue.Queue()
        for top_category, url in self.mainCategory.items():
            self.queue.put(([top_category], url))
        self.cycle_crawl_category(TIMEOUT)
        log.log_print('Close cabelas category cralwer.', self.logger_category, logging.INFO)

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


    def get_orm_category(self, url):
        """ used by parse_category() """
        catname, catn = url2catname2catn(url)
        cate = Category.objects(catn=catn).first()
        # without first() it return a list
        if cate is None:
            cate = Category(catn=catn)
            if catname:
                cate.catname = catname
        cate.update_time = datetime.utcnow()
        return cate

    def parse_category(self, category_list_path, url, content):
        tree = lxml.html.fromstring(content)
        node = tree.xpath('//div[@id="siteContent"]//div[@class="layoutLeftColumn"]//div[@class="leftnav_content"]')
        if node:
            node = node[0]
        else:
            log.log_traceback(self.logger_category, 'Url can not be parsed {0}'.format(url))
            return

        while node.xpath('./ul/li[@class="active"]'):
            node = node.xpath('./ul/li[@class="active"]')[0]
        items = node.xpath('./ul/li')
        if not items:
            showing = tree.xpath('//div[@id="siteContent"]//div[@class="layoutCenterColumn"]/div[@class="pagination"]//td[@class="showing"]/text()')[0]
            num = showing.split('of')[-1].split('total')[0].strip()
            cate = self.get_orm_category(url)
            cate.num = int(num)
            cate.leaf = True
            cate.save()
        else:
            for item in items:
                l = item.xpath('./a/@href')[0]
                link = l if l.startswith('http') else 'http://www.cabelas.com' + l
                category = item.xpath('./a/text()')[0]

                cate = self.get_orm_category(link)
                cate.cats = category_list_path + [category]
                cate.save()

                log.log_print('category ==> {0}'.format(cate.cats), self.logger_category)
                log.log_print('queue size ==> {0}'.format(self.queue.qsize()), self.logger_category)
                self.queue.put((cate.cats, link))


    def crawl_listing(self, url, catstr, page_num, num_in_this_url=ITEM_PER_PAGE):
        content = self.fetch_page(url)
        tree = lxml.html.fromstring(content)
        self.parse_listing(url, catstr, tree, page_num, num_in_this_url)
        
    def crawl_product(self, url, itemID):
        content = self.fetch_page(url)
        self.parse_product(url, content, itemID)
        
    def fetch_page(self, url):
        return s.get(url).content
    
    def parse_listing(self, url, catstr, tree, page_num, num_in_this_url):
        """ ITEM_PER_PAGE: 48 in settings.py """
        try:
            nodes = tree.xpath('//div[@id="siteContent"]//div[@class="layoutCenterColumn"]/div[@class="itemsWrapper"]/div[@class="resultsColumn"]//div[@class="itemEntryInner"]')
        except:
            log.log_traceback(self.logger_list, 'Did not parse node: {0}'.format(url))
#            log.log_print('content: {0}'.format(content), self.logger_list, logging.DEBUG)
            return
        if len(nodes) != num_in_this_url:
            log.log_traceback(self.logger_list, '{0} num_in_this_url: {1}, actual_num: {2}'.format(url, num_in_this_url, len(nodes)) )

        timenow = datetime.utcnow()

        for j in xrange(len(nodes)):
            price = nodes[j].xpath('.//div[@class="price"]/div/div[@class="textSale"]/text()')
            if not price:
                price = nodes[j].xpath('.//div[@class="price"]/div/div/text()')
            if not price:
                price = ''
                log.log_traceback(self.logger_list, 'do not get price {0} {1}'.format(url, j))
            else:
                price = price[0]

            t = nodes[j].xpath('.//id/a[@class="itemName"]')[0]
            title = t.text_content()
            if not title:
                title = ''
                log.log_traceback(self.logger_list, 'do not get title {0} {1}'.format(url, j))
            l = t.get('href')
            if not l:
                link = ''
                log.log_traceback(self.logger_list, 'do not get link {0} {1}'.format(url, j))
            else:
                link = l if l.startswith('http') else 'http://www.cabelas.com' + l

            # This rank changes all the time.If some product updated,some not, same rank on two products will happen!
            sell_rank = ITEM_PER_PAGE * (page_num-1) + j + 1

            itemID = re.compile(r'.*/(\d+).uts?.*').match(link).group(1)
            product = Product.objects(itemID=itemID).first()
            if not product:
                product = Product(itemID=itemID)

            product.title = title
            product.sell_rank = sell_rank
            product.list_update_time = timenow
            product.price = price.replace('$', '').replace(',', '')
            product.updated = False
            if product.catstrs == []:
                product.catstrs.append(catstr)
            elif catstr not in product.catstrs:
                product.catstrs.append(catstr)
            product.save()



    def parse_product(self, url, content, itemID):
        tree = lxml.html.fromstring(content)
        try:
            node = tree.xpath('//div[@id="siteContent"]//div[@id="productDetailsTemplate"]/div[@class="layoutWithRightColumn"]')[0]
        except:
            log.log_traceback(self.logger_product, 'Parsing page problem: {0}'.format(url))

        timenow = datetime.utcnow()

        also_like = []
        like = node.xpath('./div[@class="layoutRightColumn"]/div[@class="youMayAlsoLike"]//div[@class="item"]//a[@class="itemName"]')
        for l in like:
            link = l.get('href') if l.get('href').startswith('http') else 'http://www.cabelas.com' + l.get('href')
            also_like.append( (l.text_content(), link) )

#        img = node.xpath('./div[@class="layoutCenterColumn"]/div[@class="js-itemImageViewer itemImageInclude"]/img/@src')
        img = tree.xpath('/html/head/meta[@property="og:image"]/@content')
        if not img:
            log.log_traceback(self.logger_product, 'Page donot have a image: {0}'.format(url))

        info = node.xpath('./div[@class="layoutCenterColumn"]/div[@id="productInfo"]')
        if not info:
            log.log_traceback(self.logger_product, 'Page donot have a info: {0}'.format(url))
            return
        else:
            info = info[0]

        available = info.xpath('.//div[@class="variantConfigurator"]//div[@class="stockMessage"]/span/text()')
        if not available:
            if info.xpath('.//div[@class="variantConfigurator"]//div[@class="js-availabilityMessage"]'):
                m = re.compile(r"ddWidgetEntries\['js-vc13280170'] =(.*), values ").search(content)
                # http://www.cabelas.com/product/746407.uts
                if m:
                    jsid = m.group(1).split(':')[-1].strip()
                    post_data = { 
                        'productVariantId': jsid,
                    }   
                    jsurl = 'http://www.cabelas.com/catalog/includes/availabilityMessage_include.jsp'
                    sess = requests.Session()
                    resp_cont = sess.post(jsurl, data=post_data).content
                    available = re.compile(r'<span class="availabilityMessage">(.*)</span>').search(resp_cont).group(1)

        price = info.xpath('.//div[@class="price"]/dl[@class="salePrice"]/dd[1]/text()')
        if not price:
            price = info.xpath('.//div[@class="price"]/dl[1]/dd[1]/text()')
        if not price:
            avail = info.xpath('.//div[@class="variantConfigurator"]/span[@class="soldOut"]/text()')
            if avail == ['Sold Out']:
                available = 'Sold Out'
                log.log_print('Page donot have a price: {0}'.format(url), self.logger_product, logging.WARNING)

        itemNO = info.xpath('.//div[@class="variantConfigurator"]//span[@class="itemNumber"]/text()') # this xpath need strip()
        if not itemNO:
            itemNO = tree.xpath('//div[@id="siteContent"]//div[@class="w100"]/meta[1]/@content')
        if not itemNO:
            log.log_traceback(self.logger_product, 'Page donot have a itemNO: {0}'.format(url))
        else:
            itemNO = itemNO[0].strip()

        ship = info.xpath('.//div[@class="bottomNote"]//td/img/@alt')
        if ship and ship[0] == 'In-Store Pick Up':
            shipping = 'free shipping'
        else:
            shipping = ''

        desc = node.xpath('./div[@class="layoutCenterColumn"]/div[@id="tabsCollection"]//div[@id="description"]')

        rating, reviews = '', ''
        if node.xpath('./div[@class="layoutCenterColumn"]/div[@id="tabsCollection"]//div[@class="panel"]//div[@id="RRQASummaryBlock"]/div[@id="BVRRSummaryContainer"]'):
            jsurl = 'http://reviews.cabelas.com/8815/{0}/reviews.djs?format=embeddedhtml'.format(itemNO.split('-')[-1])
            rating_content = self.fetch_page(jsurl)
            m = re.compile(r'<span class=\\"BVRRNumber BVRRRatingNumber\\">(.*?)<\\/span>').search(rating_content)
            if m:
                rating = float(m.group(1))
            m = re.compile(r'<span class=\\"BVRRNumber BVRRBuyAgainTotal\\">(.*?)<\\/span>').search(rating_content)
            if m:
                reviews = float(m.group(1).replace(',', ''))

        model = []
        models = node.xpath('./div[@class="layoutCenterColumn"]/div[@id="productChart"]//tbody/tr/td[1]/text()')
        for m in models:
            model.append(m)
            

        product = Product.objects(itemID=itemID).first()
        if not product:
            product = Product(itemID=itemID)

        product.full_update_time = timenow
        product.also_like = also_like
        product.image = img[0] if img else ''
        if price:
            product.price = price[0].replace('$', '').replace(',', '')
        product.itemNO = itemNO
        product.shipping = shipping
        if available:
            product.available = available[0]
        product.description = desc[0].text_content() if desc else ''
        if rating:
            product.rating = rating
        if reviews:
            product.reviews = reviews
        if model:
            product.model = model
        product.updated = True

        product.save()


if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
    server.run()
