#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import time
import storm
import pickle
import requests
import lxml.html
from zlib import compress, decompress

from urllib import quote, unquote
from mongoengine import *
from datetime import datetime, timedelta

#############################
# setup worker's common vars
#############################

DB_HOST = 'ec2-54-245-3-3.us-west-2.compute.amazonaws.com'
DB_HOST = '127.0.0.1'
DB = 'amazon'

connect(db=DB, host=DB_HOST)

ROOT_CATN = {
    'Electronics':              'n:172282',
    'Appliances':               'n:2619525011',
    'Patio, Lawn & Garden':     'n:2972638011',
    'Tools & Home Improvement': 'n:228013',
    'Health & Personal Care':   'n:3760901',
    'Sports & Outdoors':        'n:3375251',
    'Video Games':              'n:468642',
    'Toys & Games':             'n:165793011',
}

def catn2url(catn): 
    return 'http://www.amazon.com/s/?rh=' + quote(catn)

def url2catn(url): 
    m = re.compile(r'(n%3A.*?)&').search(url)
    if not m:
        m = re.compile(r'(n%3A.*)').search(url)
    return unquote(m.group(1))

class Category(Document):
    cats        =   ListField(StringField()) 
    is_leaf     =   BooleanField(default=False)
    updated     =   BooleanField(default=False)
    update_time =   DateTimeField(default=datetime.utcnow)
    catn        =   StringField(unique=True)
    num         =   IntField() 
    pagesize    =   IntField()
    meta        =   {
        "indexes":  ["cats", ("is_leaf", "update_time"), "num", ],
    }
    def url(self):
        return catn2url(self.catn)
    def catstr(self):
        return " > ".join(self.cats)

class Product(Document):
    asin                =   StringField(primary_key=True)
    list_update_time    =   DateTimeField(default=datetime.utcnow)
    full_update_time    =   DateTimeField(default=datetime.utcnow)
    cats                =   ListField(StringField()) 
    like                =   StringField()
    manufactory         =   StringField()
    model               =   StringField()
    price               =   FloatField()
    poprank             =   IntField()
    review_star         =   FloatField()
    review_num          =   IntField()
    title               =   StringField()
    slug                =   StringField()
    summary             =   StringField() 
    vartitle            =   StringField()
    meta                =   {
        "indexes":  ["asin", "cats", "list_update_time", "full_update_time", "model", ],
    }
    def url(self):
        return "http://www.amazon.com/{slug}/dp/{asin}".format(slug=self.slug, asin=self.asin)
    def catstr(self):
        return " > ".join(self.cats)

################################
# setup amazon's building blocks
################################
class AmazonCategorySpout(storm.Spout):
    """ spout urls to fetch """
    def execute(self):
        for k, v in ROOT_CATN.items():
            url = catn2url(v)
            ret = {"url":url+'&page=2'}
            self.logger.debug("spouting: {0}".format(repr(ret)))
            yield ret

        for c in Category.objects(updated=False):
            if c.catn not in ROOT_CATN.values():
                page = 1
            else:
                page = 2
            ret = {"url":c.url()+'&page='+str(page)}
            yield ret

        for c in Category.objects(update_time__lt=datetime.utcnow()-timedelta(days=7)):
            if c.catn not in ROOT_CATN.values():
                page = 1
            else:
                page = 2
            ret = {"url":c.url()+'&page='+str(page)}
            yield ret

        time.sleep(10)

class AmazonCategoryFetcher(storm.SimpleFetcher):
    """ fetches amazon category """
    def setup(self):
        self.session = requests.Session(
            prefetch = True,
            timeout = 15,
            headers = {
                'User-Agent': 'Mozilla 5.0/Firefox 15.0.1 FavBuyBot',
            },
            config = {
                'max_retries': 3,
                'pool_connections': 10,
                'pool_maxsize': 10,
            }
        )
        self.cache = {}

    def execute(self, url):
        self.logger.info("extracting info from {0}".format(url))
        if url in self.cache and time.time() - self.cache.get(url) < 86400:
            return
        else:
            self.cache[url] = time.time()

        text = self.session.get(url).text
        t = lxml.html.fromstring(text)

        catn = url2catn(url)
        c = Category.objects(catn=catn).first()
        if not c:
            c = Category(catn=catn)
        c.update_time = datetime.utcnow()
        
        delimitter = u'\xa0'
        catlist = t.xpath('//div[@id="leftNavContainer"]//ul[@data-typeid="n"]//li')
        if delimitter not in catlist[-1].text_content():
            c.is_leaf = True
        
        # format1: Showing 25 - 48 of 496 Results
        # format2: Showing 4 Results
        try:
            resultcount = t.xpath('//*[@id="resultCount"]/span')[0].text_content()
        except:
            # format3: Should Get Page2 to get this info
            url = url[:-1]+'2'
            text = self.session.get(url).text
            t = lxml.html.fromstring(text)
            resultcount = t.xpath('//*[@id="resultCount"]/span')[0].text_content()

        m = re.compile(r'Showing \d+ - (\d+) of ([0-9,]+) Results').search(resultcount)
        if not m:
            m = re.compile(r'Showing (\d+) Results?').search(resultcount)
            c.num = int(m.group(1))
            c.pagesize = 24
        else:
            c.pagesize = int(m.group(1))/2
            c.num = int(m.group(2).replace(',',''))

        c.cats = []
        for cat in catlist:
            catraw = cat.text_content().strip()
            if delimitter in catraw:
                c.cats.append(catraw[catraw.find(delimitter)+1:])
            else:
                c.cats.append(catraw)
                break

        c.updated = True
        c.save()
        self.logger.info("saved category <catn:{0}>".format(c.catn))
    
        # adding all incomplete categories that can be found in this page
        for cat in catlist:
            a = cat.xpath(".//a")
            if a:
                url = a[0].get("href")
                catn = url2catn(url)
                if not Category.objects(catn=catn):
                    Category(catn=catn).save()

class AmazonCrawler(object):
    def __init__(self):
        self.running_category = False
        self.category_topology = None

        self.running_product = False
        self.product_topology  = None

        self._load()

    @property
    def logger(self):
        return logging.getLogger("amazoncrawler.AmazonCrawler")

    def _load(self):
        if os.path.exists("amazoncrawler.dump"):
            self = pickle.loads(open("amazoncrawler.dump"))
    
    def _dump(self):
        pickle.dump(self, open("amazoncrawler.dump","w"))

    def crawl_category(self):
        if self.running_category:
            self.logger.warning("crawl_cateogry already running, exiting")
            return

        t = storm.Topology(os.path.abspath(__file__)) 
    
        # nodes
        s = storm.Node(AmazonCategorySpout, 1, storm.FIELD_GROUPING, ('url',))
        f = storm.Node(AmazonCategoryFetcher, 5)
    
        # connect them
        t.add_root(s).chain(f)

        # create and run 
        t.create() 
    
        self.category_topology = t
        self.running_category = True

    def stop_category(self):
        if self.running_category and self.category_topology:
            self.category_topology.destroy()
            self.running_category = False

if __name__ == "__main__":
    a = AmazonCrawler()
    a.crawl_category()
