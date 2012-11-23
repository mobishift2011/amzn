#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from gevent.queue import Queue

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
import lxml.etree

from urllib import quote, unquote
from datetime import datetime, timedelta

from models import *
from settings import *


headers = {
    'User-Agent': 'Mozilla 5.0/Firefox 15.0.1',
}

config = {
    'max_retries': 3,
    'pool_connections': 10,
    'pool_maxsize': 10,
}

s = requests.session(prefetch=True, timeout=15, config=config, headers=headers)

def url2itemid(url):
    #http://www.newegg.com/Product/Product.aspx?Item=N82E16834131323
    try:
        return re.compile(r'http://www.newegg.com/Product/Product.aspx\?Item=([^&]*)').search(url).group(1)
    except:
        return None

class Server:
    def __init__(self):
        self.fetched_urls = set()
        self.fetch_queue = Queue()

    def find_all_categories(self):
        home = 'http://www.newegg.com/Index.aspx?name=Home'
        self.fetch_queue.put( (1, home) )
        pool = Pool(50)

        while True:
            try:
                depth, url = self.fetch_queue.get(timeout=30)
            except:
                break

            if depth <= 10 and url not in self.fetched_urls:
                self.fetched_urls.add(url)
                pool.spawn(self.fetch_page, depth, url) 
                #self.fetch_page(depth, url)

        pool.join()
        
    def fetch_page(self, depth, url):
        # fetching
        #print 'fetching', url
        content = s.get(url).content

        # generating urls to fetch
        urls_to_fetch = re.compile(r'"(http://www.newegg.com/Store.*?)"').findall(content)
        urls_to_fetch = set(urls_to_fetch) - self.fetched_urls
        
        for u in urls_to_fetch:
            self.fetch_queue.put( (depth+1, u) )

        # saving category info into db
        #http://www.newegg.com/Store/SubCategory.aspx?SubCategory=20&name=LCD-Monitors
        m = re.compile(r'http://www.newegg.com/Store/SubCategory.aspx\?SubCategory=(\d+)&name=(.+)').search(url)
        if m:
            catid, catname = int(m.group(1)), m.group(2)
            c = Category.objects(catid=catid).first()
            if not c:
                c = Category(catid=catid)
                c.save()

            try:
                num = int(re.compile(r'span id="RecordCount[^>]*>(\d+)').search(content).group(1))
                c.num = num
            except:
                print 'error', url
                return
        
            c.catname = catname.split('&')[0]
            c.update_time = datetime.utcnow()
        
            print 'saved', c.catname, c.catid
            c.save()
         
    def crawl_listing(self, url):
        content = s.get(url).content
        itemids = set(re.compile(r'"http://www.newegg.com/Product/Product.aspx\?Item=(.*?)"').findall(content))
        for itemid in itemids:
            p = Product.objects(itemid=itemid).first()
            if not p:
                p = Product(itemid=itemid)

            #http://www.newegg.com/Store/SubCategory.aspx?SubCategory=32&name=Laptops-Notebooks 
            m = re.compile(r'http://www.newegg.com/Store/SubCategory.aspx\?SubCategory=(\d+)&name=(.+)').search(url)
            if m and (int(m.group(1)) not in p.catids):
                p.catids.append(int(m.group(1)))
            p.updated = False
            p.list_update_time = datetime.utcnow()
            p.save()
    
    def crawl_product(self, url):
        content = s.get(url).content
        itemid = url2itemid(url)
        
        p = Product.objects(itemid=itemid).first()
        if not p:
            p = Product(itemid=itemid)

        t = lxml.html.fromstring(content)

        
        try:
            p.title = t.xpath('//h1')[0].text_content().strip()
            p.description = t.xpath('//div[@class="grpBullet"]')[0].text_content().strip()
        except:
            # this might be a wrong itemid that redirects us to some category page
            try:
                p.delete()
            except:
                pass
            return
        

        p.details = lxml.etree.tostring(t.xpath('//*[@id="Details_Content"]')[0])

        m = re.compile('<dt>Brand.*?<dd>([^<]*)</dd>').search(p.details)
        if m:
            p.brand = m.group(1)

        m = re.compile('<dt>Model.*?<dd>([^<]*)</dd>').search(p.details)
        if m:
            p.model = m.group(1)

        p.cover_image_url = t.xpath('//*[@id="A2"]')[0].xpath('.//img')[0].get('src')

        if not p.comments:
            for cm in t.xpath('//*[@id="Community_Content"]/table/tbody/tr'):
                msg = cm.xpath('.//td')[0].text_content().strip()[:-100]
                p.comments.append(msg)

        # extra info from 
        extraurl = 'http://content.newegg.com/LandingPage/ItemInfo4ProductDetail.aspx?Item={0}&v2=2012'.format(itemid)
        content = s.get(extraurl).content
        if not content:
            # sometimes product has incomplete info
            # http://www.newegg.com/Product/Product.aspx?Item=9SIA00Y0E85234&SortField=1
            try:
                p.delete()
            except:
                pass
            return
        content = content.replace('var ','').replace(';', '').replace('\r','').replace('null','None').strip()
        content = content.split('\n')[1]
        exec(content)
        p.price = rawItemInfo['finalPrice']
        p.promote = rawItemInfo['promotionText']
        p.extrainfo = rawItemInfo

        # related items
        relateurl = 'http://content.newegg.com/Common/Ajax/RelationItemInfo.aspx?item={0}&type=Newegg&v2=2012'.format(itemid)
        content = s.get(relateurl).content
        p.suggests = list(set(re.compile(r'http://www.newegg.com/Product/Product.aspx\?Item=([^\\]*)').findall(content)))

        p.updated = True
        p.full_update_time = datetime.utcnow()
    
        p.save()

if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(CRAWLER_PORT))
    server.run()
