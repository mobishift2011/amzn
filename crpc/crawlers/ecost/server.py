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
from models import *

sys.path.insert(0, os.path.abspath( os.path.dirname(__file__) ))
from common.events import *
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
        self.ecosturl = 'http://www.ecost.com'

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
        debug_info.send(sender="ecost.category.begin" )
        self.queue = Queue.Queue()
        self.get_main_category()

        self.cycle_crawl_category(TIMEOUT)
        debug_info.send(sender="ecost.category.end" )


    def cycle_crawl_category(self, timeover=60):
        """.. :py:method::
            read (category, link) tuple from queue, crawl sub-category, insert into the queue

        :param timeover: timeout in queue.get
        """
        while not self.queue.empty():
            try:
                job = self.queue.get(timeout=timeover)
                utf8_content = fetch_page(job[1])
                if not utf8_content:
                    page_download_failed.send(sender="ecost.category.download.error", category_list=job[0], url=job[1])
                    continue
                self.parse_category(job[0], job[1], utf8_content)
            except Queue.Empty:
                debug_info.send(sender="ecost.category:Queue waiting {0} seconds without response!".format(timeover))
            except:
                debug_info.send(sender="ecost.category", tracebackinfo=sys.exc_info())


    def set_leaf_to_db(self, catstr, total_num=None):
        """.. :py:method::
            insert/update leaf node information to db

        :param catstr: primary key in collection Category
        :param total_num: product number in this leaf category
        """
        c, is_new = Category.objects.get_or_create(pk=catstr)
        c.is_leaf = True
        if total_num: c.num = total_num
        c.update_time = datetime.utcnow()
        c.save()
        category_saved.send(sender='ecost.category', site='ecost', key=catstr, is_new=is_new)

    def parse_category(self, category_list_path, url, content):
        """.. :py:method::
            parse the category in the page source

        :param category_list_path: category path in list data type
        :param url: category url need to find sub-category
        :param content: content in this url
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
                    self.set_leaf_to_db(' > '.join(category_list_path))
                    debug_info.send(sender='ecost.category', info='special leaf page {0}'.format(url))
                    return

            for category in categories:
                link = category.get('href')
                name = category.text_content()
                if not link.startswith('http'):
                    link = self.ecosturl + link

                # trap "Household Insulation":
                # ['Electronics & Entertainment', 'Audio & Video', 'Accessories', 'Receivers', 'Accessories', 'Receivers', ...
                if name in category_list_path:
                    continue

                cats = category_list_path + [name]
                debug_info.send(sender='ecost.category', cats=cats, queue_size=self.queue.qsize())
                c, is_new = Category.objects.get_or_create( pk=' > '.join(category_list_path) )
                if is_new:
                    c.cats = cats
                    c.catstr = ' > '.join(cats)
                    c.url = link
                c.update_time = datetime.utcnow()
                c.save()
                category_saved.send(sender='ecost.category', site='ecost', key=' > '.join(category_list_path), is_new=is_new)
                self.queue.put((cats, link))
        else:
            # leaf node
            num = tree.xpath('//div[@class="searchHeaderDisplayTitle"]/span[1]/text()')
            if num:
                total_num = int(num[0])
                self.set_leaf_to_db(' > '.join(category_list_path))
            else:
                debug_info.send(sender='ecost.category', info='Not a valid page {0}'.format(url))
#                log.log_print('content: {0}'.format(content), self.logger_category, logging.DEBUG)
                return


    def crawl_listing(self, url, catstr, num=None):
        """.. :py:method::
            crawl list page to get part of products' info

        :param url: listing page url
        :param catstr: listing page's category path in string data type
        :param num: porduct number in this leaf category
        """
        content = fetch_page(url)
        if not content:
            page_download_failed.send(sender="ecost.list.download.error", url=url)
            return
        self.parse_listing(catstr, url, content, num)
        
    def crawl_product(self, url, ecost=''):
        """.. :py:method::
            crawl the detail page to get another part of products' info

        :param url: product url
        :param ecost: product's ecost number
        """
        content = fetch_page(url)
        if not content:
            page_download_failed.send(sender="ecost.product.download.error", url=url)
            return
        self.info = {'ecost': '', 'model':'', 'shipping': '', 'available': '', 'platform': '', 'manufacturer': '', 'upc': '', 'review': 0, 'rating': ''}
        self.parse_product(url, content, ecost)
        
    def parse_listing(self, catstr, url, content, num):
        """.. :py:method::
            only for price. some special page don't have an item number.
            ITEM_PER_PAGE: 25 in models.py

        :param catstr: listing page's category path in string data type
        :param url: listing page url
        :param content: this url's content
        :param num: porduct number in this leaf category
        """
        tree = lxml.html.fromstring(content)

        if not num:
            # special page, have 'BROWSE CATEGORIES', but is leaf node
            # price in listing page is not the same in product page.
            price = tree.xpath('//div[@class="noDisplayPricen"]//span[@class="itemFinalPrice wt14"]')
            prices = [p.text_content().strip().replace('$','').replace(',','') for p in price]
            links = tree.xpath('//span[@class="itemName wcB1"]/a')
            if len(prices) != len(links):
                warning_info.send(sender='ecost.listing', msg='prices number != links number', url=url)
            for j in xrange( len(links) ):
                href = links[j].get('href')
                if not href or not links[j].text_content().strip():
                    continue
                if not href.startswith('http'):
                    href = self.ecosturl + href
                self.conn.title_link(links[j].text_content().strip(), href, prices[j])
            return

        total_num = int(tree.xpath('//div[@class="searchHeaderDisplayTitle"]/span[1]/text()')[0])
        page_num = (total_num - 1) // ITEM_PER_PAGE + 1

        if page_num == 1:
            self.get_info(url, catstr, total_num, page_num)
        else:
            for i in xrange(1, page_num):
                self.get_info('{0}&op=zones.SearchResults.pageNo&pageNo={1}'.format(url, i), catstr, ITEM_PER_PAGE, i)
            self.get_info('{0}&op=zones.SearchResults.pageNo&pageNo={1}'.format(url, page_num), catstr, total_num % ITEM_PER_PAGE, page_num)

    def url2ecoststr(self, url, ecost):
        """.. :py:method::
            from the url to get the ecost_str

        :param url: product page url
        :param ecost: product ecost id
        """
        return re.compile(r'http://www.ecost.com/p/.*/product~dpno~{0}~pdp.(\w+)'.format(ecost)).match(url).group(1)

    def get_info(self, url, catstr, total_num, page_num):
        """.. :py:method::
            get some of the product detail from the listing page

        :param url: listing page url
        :param catstr: listing page's category in string datatype
        :param total_num: product number in this leaf category
        :param page_num: page number in this leaf category
        """
        content = fetch_page(url)
        if not content:
            page_download_failed.send(sender="ecost.parse_list.download.error", url=url)
            return
        tree = lxml.html.fromstring(content)
        nodes = tree.xpath('//div[@id="searchResultList"]/div[@class="sr-table_content"]')

        ecost, models, prices, links = [], [], [], []
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
                links.append( l if l.startswith('http') else self.ecosturl + l )

        if total_num != len(ecost):
            warning_info.send(sender='ecost.list:', url=url, total_num=total_num, ecost_num=len(ecost), page_num=page_num)

        debug_info.send(sender='ecost.list', ecost_num=len(ecost), models_num=len(models), prices_num=len(prices), links_num=len(links), url=url)
        timenow = datetime.utcnow()

        for j in xrange( len(ecost) ):
            # This rank changes all the time.If some product updated, some not, same rank on two products will happen!
            sell_rank = ITEM_PER_PAGE * (page_num-1) + j + 1
            p, is_new = Product.objects.get_or_create(pk=ecost[j])
            if catstr.decode('utf-8') not in p.cats:
                p.cats.append(catstr)
            if is_new:
                p.ecost_str = self.url2ecoststr(links[j], ecost[j])
                p.model = models[j]
            p.price = prices[j]
            p.sell_rank = sell_rank
            p.updated = False
            p.list_update_time = timenow
            p.save()
            product_saved.send(sender='ecost.list', site='ecost', key=ecost[j], is_new=is_new)
    

    def parse_product(self, url, content, ecost):
        """.. :py:method::
            get product detail

        :param url: product page url
        :param content: this url contents
        :param ecost: ecost number
        """
        tree = lxml.html.fromstring(content)

        title = tree.xpath('//h1[@class="prodInfo wt"]/text()')[-1]
        image = tree.xpath('//td[@width]/img[@src]/@src')[0]
        if image.startswith('//'):
            image = 'http' + image
        price = tree.xpath('//td[@class="leftPane"]//td[starts-with(@class, "infoPrice infoBorderContent")]//text()')
        if not price:
            price = tree.xpath('//td[@class="leftPane"]//td[@class="infoContent infoPrice wt15"]/text()')
        price = price[0].replace('$', '').replace(',', '') if price else ''

        node = tree.xpath('//td[@class="rightPane"]/table//tr')
        for tr in node:
            name = tr.xpath('./td[@class="infoLabel"]/text()')
            if name:
                self.label_value(name, tr)

        tables = tree.xpath('//div[@class="simpleTab06 wt11 wcGray1"]/div[@id="pdpTechSpecs"]//tr[@class="dtls"]')
        specifications = dict(t.text_content().strip().split('\n\t\t\t\t') for t in tables)

        p, is_new = Product.objects.get_or_create(pk=ecost)
        p.title = title
        p.image_urls.append(image)
        p.price = price
        p.model = self.info['model']
        p.shipping = self.info['shipping']
        p.available = self.info['available']
        p.platform = self.info['platform']
        p.manufacturer = self.info['manufacturer']
        p.upc = self.info['upc']
        p.num_reviews = self.info['review']
        p.rating = self.info['rating']
        p.specifications = specifications
        p.updated = True
        p.full_update_time = datetime.utcnow()
        p.save()
        product_saved.send(sender='ecost.product', site='ecost', key=ecost, is_new=is_new)


    def label_value(self, name, tr):
        """.. :py:method::
            based on the name(key) of the field, get its value. put the information into self.info

        :param name: name of the field in web page
        :param tr: xml node, use xpath to get the value based on the name
        """

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
