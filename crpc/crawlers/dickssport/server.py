#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.dickssport.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""

import os
import re
import sys
import time
import zerorpc
import traceback
import lxml.html
import Queue

from urllib import quote, unquote
from datetime import datetime, timedelta
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *


def url2catid(url):
    """ 1. top category: http://www.dickssportinggoods.com/category/index.jsp;jsessionid=31VQQy9V1m7Gwyxn9zjLPGLh7pKQyvSfwVLmmppY2nZZpGhPJLCr!248088961?ab=TopNav_Footwear&categoryId=4413987&sort=%26amp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bquot%3B].passthru%28%27id%27%29.exit%28%29.%24a[%26amp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bquot%3B
        2. category http://www.dickssportinggoods.com/category/index.jsp?categoryId=4413987
        3. leaf category: http://www.dickssportinggoods.com/family/index.jsp?categoryId=12150078
    """
    m = re.compile(r'http://www.dickssportinggoods.com/(category|family|shop|info)/index.jsp(.*)categoryId=(\d+)').match(url)
    if not m:
        print url
    return m.group(1), m.group(3)


class Server:
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    def __init__(self):
        self.site = 'dickssport'
        self.caturl = 'http://www.dickssportinggoods.com'

    def url2tree(self, url, err_msg, is_category=None):
        content = fetch_page(url)
        if not content:
            if is_category == True:
                category_failed.send(sender=err_msg, site=self.site, url=url, reason="download page error")
            elif is_category == False:
                product_failed.send(sender=err_msg, site=self.site, url=url, reason="download page error")
            else:
                debug_info.send(sender=err_msg)
            return
        return lxml.html.fromstring(content)
         

    def get_main_category(self):
        """.. :py:method::
            put top category into queue
        """
        tree = self.url2tree(url, 'dickssport.main_category.download.error', True)
        if not tree:
            return
        nodes = tree.xpath('//div[@class="mainNavigation"]/ul/li/a')
        links, names = [], []
        for node in nodes:
            link = node.get('href')
            if not link.startswith('http'):
                link = self.caturl + link
            links.append(link)
            name = node.text_content().strip()
            names.append(name)

            catname, catn = url2catid(link)
            c = Category.objects(catn=catn)
            if catname == 'family':
                c.is_leaf = True
            c.catname = name
            c.cats = [name]
            c.update_time = datetime.utcnow()
        self.mainCategory = dict(zip(names, links))


    def crawl_category(self):
        """.. :py:method::
            crawl category
        """
        debug_info.send(sender="dickssport.category.begin" )
        self.queue = Queue.Queue()
        self.get_main_category()

        for top_category, url in self.mainCategory.items():
            self.queue.put(([top_category], url))
        self.cycle_crawl_category(TIMEOUT)
        debug_info.send(sender="dickssport.category.end" )

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


    def parse_category(self, category_list_path, url, content):
        """
        http://www.dickssportinggoods.com/shop/index.jsp?categoryId=13342544&ab=ACLN1_Link_ShopCategory_TradeIn
        http://www.dickssportinggoods.com/category/index.jsp?categoryId=4414069

        http://www.dickssportinggoods.com/category/index.jsp?categoryId=4414427
        http://www.dickssportinggoods.com/category/index.jsp?categoryId=12137921
        http://www.dickssportinggoods.com/category/index.jsp?categoryId=4414021
        """
        tree = lxml.html.fromstring(content)

        # parse leaf category, leaf node saved before.
        catname, catn = url2catid(url)
        if catname == 'shop' or catname == 'info':
            log.log_print('Invalid url {0}'.format(url), self.logger_category, logging.INFO)
            return

        # parse category
        nodes = tree.xpath('//div[@id="wrapper"]/div[@id="frame"]/div[@id="contentLeft"]/div[@class="leftNavNew "]/ul[@id="leftNavUL"]/li/a')
        if not nodes:
            nodes = tree.xpath('//div[@id="wrapper"]/div[@id="frame"]/div[@id="catLeftContent"]/div[@id="left1"]//ul/li/a')
        if not nodes:
            log.log_traceback(self.logger_category, 'Url can not be parsed {0}'.format(url))
            redis_SERVER.hincrby(redis_KEY, 'num_parse_error', 1)
            return

        for node in nodes:
            link = node.get('href')
            name = node.text_content()
            if name in category_list_path: # avoid trap loop
                continue
            if not link.startswith('http'):
                link = self.caturl + link
            
            catname, catn = url2catid(link)
            if name.startswith("View All"):
                if catname == 'family':
                    # equal to all other categories
                    continue

            cate = Category.objects(catn=catn).first() # without first() it return a list
            if cate is None:
                cate = Category(catn=catn)
                redis_SERVER.hincrby(redis_KEY, 'num_new_crawl', 1)
            else:
                redis_SERVER.hincrby(redis_KEY, 'num_new_update', 1)

            # in case name updated, deassign
            cate.catname = name
            if name == 'View All':
                # if it's 'View All', don't add it as category path
                cate.cats = category_list_path
            else:
                cate.cats = category_list_path + [name]
            if catname == 'family':
                cate.is_leaf = True
            cate.update_time = datetime.utcnow()
            cate.save()

            log.log_print('category ==> {0}'.format(cate.cats), self.logger_category)
            log.log_print('queue size ==> {0}'.format(self.queue.qsize()), self.logger_category)
            if not cate.is_leaf:
                # if it is leaf node, not need to enqueue
                self.queue.put((cate.cats, link))


    def crawl_listing(self, url, catstr, *targs):
        content = self.fetch_page(url)
        if not content:
            log.log_traceback(self.logger_list, 'page url can not be downloaded {0}'.format(url))
        try:
            tree = lxml.html.fromstring(content)
        except:
            log.log_print('{0} only have space!! {1}'.format(url, content), self.logger_list, logging.CRITICAL)
            return

        number = tree.xpath('//div[@id="wrapper"]/div[@id="frame"]/div[@id="contentRight"]//span[@class="searchPagination_numItems"]/text()')
        if not number:
            redis_SERVER.hincrby(redis_KEY, 'num_parse_error', 1)
            log.log_traceback(self.logger_list, 'Leaf url do not have numbers {0}'.format(url))
            return
        number = int(number[0].split()[0].replace(',', ''))
        catid = url2catid(url)[1]
        Category.objects(catn=catid).first().num = number

        num_page = (number - 1) // ITEM_PER_PAGE + 1
        for page in xrange(1, num_page+1):
            link = '{0}&pg={1}&s=A-UnitRank-DSP'.format(url, page)
            if page == num_page:
                self.parse_listing(link, catstr, page, number % ITEM_PER_PAGE)
            else:
                self.parse_listing(link, catstr, page, ITEM_PER_PAGE)

        
    def crawl_product(self, url):
        content = self.fetch_page(url)
        if not content:
            log.log_traceback(self.logger_product, 'page url can not be downloaded {0}'.format(url))
        try:
            tree = lxml.html.fromstring(content)
        except:
            log.log_traceback(self.logger_product, 'Page {0} can not build xml tree {1}'.format(url, content))
            return
        self.parse_product(url, tree)

        
    def fetch_page(self, url):
        try:
            ret = s.get(url)
        except:
            # page not exist or timeout
            redis_SERVER.hincrby(redis_KEY, 'num_not_exist', 1)
            return

        if ret.ok: return ret.content
        else: redis_SERVER.hincrby(redis_KEY, 'num_not_exist', 1)
    

    def parse_listing(self, url, catstr, page_num, num_in_this_url):
        """ ITEM_PER_PAGE: 12 in settings.py """
        content = self.fetch_page(url)
        if not content:
            log.log_traceback(self.logger_list, 'Page url can not be downloaded {0}'.format(url))
        tree = lxml.html.fromstring(content)

        try:
            nodes = tree.xpath('//div[@id="wrapper"]/div[@id="frame"]/div[@id="contentRight"]/ul[@id="productLoopUL"]/li')
        except:
            redis_SERVER.hincrby(redis_KEY, 'num_parse_error', 1)
            log.log_traceback(self.logger_list, 'List url can not parse node: {0}'.format(url))
#            log.log_print('content: {0}'.format(content), self.logger_list, logging.DEBUG)
            return
        if len(nodes) != num_in_this_url:
            log.log_print('{0} num_in_this_url: {1}, actual_num: {2}'.format(url, num_in_this_url, len(nodes)), self.logger_list, logging.WARNING)

        timenow = datetime.utcnow()

        for j in xrange(len(nodes)):
            # ourPrice2: $94.99, ourPrice: $89.99 to $99.99
            price = nodes[j].xpath('./div[@class="prodloopText"]/div[@class="prodPriceWrap"]/div[starts-with(@class, "ourPrice")]/p/text()')
            if not price:
                # Our Price: $34.99 to $39.99
                price = nodes[j].xpath('./div[@class="prodloopText"]/div[@class="prodPriceWrap"]/span[@class="ourPrice"]/nobr/text()')
            if not price:
                price = ''
                log.log_traceback(self.logger_list, 'Can not get price {0} {1}'.format(url, j))
            else:
                price = price[0]

            link_name = nodes[j].xpath('./div[@class="prodloopText"]/h2/a')[0]
            title = link_name.text_content().strip()
            l = link_name.get('href')
            if not title:
                title = ''
                log.log_traceback(self.logger_list, 'Can not get title {0} {1}'.format(url, j))
            if not l:
                log.log_traceback(self.logger_list, '!!* Can not get link {0} {1}'.format(url, j))
                continue
            else:
                link = l if l.startswith('http') else self.caturl + l

            # http://www.dickssportinggoods.com/family/index.jsp?categoryId=11967855&pg=1&s=A-UnitRank-DSP
            # http://www.dickssportinggoods.com/config/index.jsp?productId=11326588
            m = re.compile(r'http://www.dickssportinggoods.com/(product|config)/index.jsp.*productId=(\d+).*').match(link)
            if m:
                itemNO = m.group(1)
            else:
                log.log_traceback(self.logger_list, '!!* Can not get itemNO from link {0} {1}'.format(url, j))
                continue

            # This rank changes all the time.If some product updated,some not, same rank on two products will happen!
            sell_rank = ITEM_PER_PAGE * (page_num-1) + j + 1

            product = Product.objects(key=itemNO).first()
            if not product:
                redis_SERVER.hincrby(redis_KEY, 'num_new_crawl', 1)
                product = Product(key=itemNO)
            else:
                redis_SERVER.hincrby(redis_KEY, 'num_new_update', 1)

            product.title = title
            product.sell_rank = sell_rank
            product.list_update_time = timenow
            product.price = price.replace('$', '').replace(',', '') # '$34.99 to $44.99'
            product.updated = False
            if catstr not in product.cats:
                product.cats.append(catstr)
            product.save()



    def parse_product(self, url, tree):
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
        if reviews:
            comment_all = node.xpath('./div[@id="rCol"]/div[@id="FieldsetCustomerReviews"]//div[starts-with(@id, "pr-contents-")]//div[@class="pr-review-wrap"]')
            for comm in comment_all:
                rate = comm.xpath('.//span[@class="pr-rating pr-rounded"]/text()')[0]
                head = comm.xpath('.//p[@class="pr-review-rating-headline"]/text()')[0]
                text = comm.xpath('./div[@class="pr-review-main-wrapper"]//p[@class="pr-comments"]/text()')[0]
                comment.append( (rate, head, text) )


        itemNO = re.compile(r'http://www.dickssportinggoods.com/product/index.jsp.*productId=(\d+).*').match(url).group(1)
        product = Product.objects(key=itemNO).first()
        if not product:
            product = Product(key=itemNO)
            redis_SERVER.hincrby(redis_KEY, 'num_new_crawl', 1)
        else:
            redis_SERVER.hincrby(redis_KEY, 'num_new_update', 1)

        product.title = title
        if also_like: product.also_like = also_like
        if price and '$' in price[0]:
            product.price = price[0].split(':')[1].strip().replace('$', '').replace(',', '')
        if shipping: product.shipping = shipping[0].strip()
        if img and img[0] not in product.image_urls:
            product.image_urls.append( img[0] )
        if description: product.summary = description
        if model: product.model = model
        if available: product.available = available
        if rating: product.rating = rating[0]
        if reviews: product.num_reviews = reviews[0].replace(',', '')
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
                product.rating = rating[0]

        if 'reviews' in targs:
            reviews = node.xpath('./div[@id="rCol"]/div[@id="FieldsetCustomerReviews"]//div[@class="pr-snapshot-rating rating"]//span[@class="count"]/text()')
            if reviews:
                product.num_reviews = reviews[0].replace(',', '')

        product.save()


if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(CRAWLER_PORT))
    server.run()
