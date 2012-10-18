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
import pickle
import logging
import requests
import traceback
import lxml.html
from zlib import compress, decompress

from urllib import quote, unquote
from mongoengine import *
from datetime import datetime, timedelta

#############################
# setup worker's common vars
#############################

DB_HOST = 'ec2-54-245-3-3.us-west-2.compute.amazonaws.com'
#DB_HOST = '127.0.0.1'
DB = 'amazon'

connect(db=DB, host=DB_HOST)


def catn2url(catn): 
    return 'http://www.amazon.com/s?ie=UTF8&rh=' + quote(catn.encode("utf-8"))

def url2catn(url): 
    m = re.compile(r'(n%3A.*?)&').search(url)
    if not m:
        m = re.compile(r'(n%3A.*)').search(url)
        if not m:
            return ''
    catn = unquote(m.group(1)).decode('utf-8')
    catn = [x for x in catn.split(',') if x.startswith('n:')][-1]
    return catn

class Category(Document):
    cats        =   ListField(StringField()) 
    is_leaf     =   BooleanField(default=False)
    updated     =   BooleanField(default=False)
    update_time =   DateTimeField(default=datetime.utcnow)
    spout_time  =   DateTimeField()
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
    updated             =   BooleanField(default=False)
    cover_image_url     =   StringField()
    list_update_time    =   DateTimeField(default=datetime.utcnow)
    full_update_time    =   DateTimeField(default=datetime.utcnow)
    cats                =   ListField(StringField()) 
    like                =   IntField()
    manufactory         =   StringField()
    brand               =   StringField()
    model               =   StringField()
    price               =   FloatField()
    pricestr            =   StringField()
    salesrank           =   StringField()
    stars               =   FloatField()
    reviews_count       =   IntField()
    title               =   StringField()
    slug                =   StringField()
    summary             =   StringField() 
    vartitle            =   StringField()
    meta                =   {
        "indexes":  ["asin", "cats", "list_update_time", "full_update_time", "model", "brand", ],
    }
    def url(self):
        return "http://www.amazon.com/{slug}/dp/{asin}/".format(slug=self.slug, asin=self.asin)
    def catstr(self):
        return " > ".join(self.cats)

######################################
#  testing functions
######################################

def fetch_indexes():
    print 'testing index fetching speed'
    fetch_indexes.counter = 0
    s = requests.Session()
    r = redis.Redis(host=DB_HOST)
    key = 'amazon_index_pages'
    r.delete(key)
    t = time.time()
    num_spawns = 0
        
    def fetch_page(url):
        content = compress(s.get(url).content)
        sys.stdout.write('.')
        sys.stdout.flush()
        fetch_indexes.counter += 1
        r.hset(key, url, content)
    
    pool = Pool(20)

    for c in Category.objects(is_leaf=True):
        pages = (c.num-1)/c.pagesize+1
        for p in range(1, min(pages+1,401)):
            url = c.url()+'&page={0}'.format(p)
            pool.spawn(fetch_page, url)
            num_spawns += 1
        if num_spawns > 100:
            break

    pool.join()
    
    print '\nfetching index page qps: ', fetch_indexes.counter/(time.time()-t)

def process_indexes():
    print 'testing indexes processing speed'
    r = redis.Redis(host=DB_HOST)
    d = r.hgetall('amazon_index_pages')
    counter = 0
    t = time.time()
    for k,v in d.items():
        _process_index(k, v)
        counter += 1
        sys.stdout.write('.')
        sys.stdout.flush()
        if counter > 200:
            break
    print '\nprocessing index page qps: ', counter/(time.time()-t)

def _process_index(url, content):
    """ index info about each product -> db """
    t = lxml.html.fromstring(decompress(content))
    for block in t.xpath('//div[starts-with(@id,"result_")]'):
        try:
            link = block.xpath(".//a")[0].get("href")
        except:
            continue

        m = re.compile(r'http://www.amazon.com/(.*)/dp/(.*?)/').search(link)
        if not m:
            m = re.compile(r'http://www.amazon.com/(.*)/dp/(.*)').search(link)

        if m:
            slug, asin = m.group(1), m.group(2)  

            p, is_new = Product.objects.get_or_create(pk=asin)
                
            c = Category.objects(catn=url2catn(url)).first()
            if c:
                p.cats = c.cats

            # some infomation we just update once and kept it forever
            if is_new:
                p.slug = slug
                p.cover_image_url = block.xpath(".//img")[0].get('src')
                p.list_update_time = datetime.utcnow()

            # others we might want to update it more frequently
            try:
                p.price = float(block.xpath('.//div[@class="newPrice"]')[0].xpath(".//span")[-1].text_content().strip()[1:].replace(',',''))
            except:
                try:
                    p.pricestr = block.xpath('.//div[@class="newPrice"]')[0].text_content().strip()
                except:
                    pass

            p.save()

def fetch_products():
    print 'testing product fetching speed'
    fetch_products.counter = 0
    s = requests.Session()
    r = redis.Redis(host=DB_HOST)
    key = 'amazon_product_pages'
    r.delete(key)
    t = time.time()
    num_spawns = 0
        
    def fetch_page(url):
        content = compress(s.get(url).content)
        sys.stdout.write('.')
        sys.stdout.flush()
        fetch_products.counter += 1
        r.hset(key, url, content)

    pool = Pool(20)

    for p in Product.objects():
        pool.spawn(fetch_page, p.url())
        num_spawns += 1
        if num_spawns > 100:
            break

    pool.join()
    print '\nfetching product page qps: ', fetch_products.counter/(time.time()-t)
    
def process_products():
    print 'testing products processing speed'
    r = redis.Redis(host=DB_HOST)
    d = r.hgetall('amazon_product_pages')
    counter = 0
    t = time.time()
    for k,v in d.items():
        _process_index(k, v)
        counter += 1
        sys.stdout.write('.')
        sys.stdout.flush()
        if counter > 1000:
            break
    print '\nprocessing product page qps: ', counter/(time.time()-t)

def _process_index(url, content):
    t = lxml.html.fromstring(decompress(content))
        
    asin = url.split('/')[-1] 
    p, is_new = Product.objects.get_or_create(pk=asin)

    try:
        p.manufactory = t.xpath('//h1[@class="parseasinTitle "]/following-sibling::*/a[@href]')[0].text_content().strip()
        p.vartitle = t.xpath('//span[@id="variationProductTitle"]')[0].text_content().strip()
    except:
        pass
        #traceback.print_exc()

    # like
    try:
        p.stars = float(t.xpath('//*[@id="handleBuy"]/div[2]/span[1]/span/span/a/span')[0].get('title').split()[0])
        p.reviews_count = int(t.xpath('//div[@class="jumpBar"]//span[@class="crAvgStars"]/a')[0].text_content().replace(',','').split()[0])
        p.like = int(t.xpath('//span[@class="amazonLikeCount"]')[0].text_content().replace(',',''))
    except:
        pass
        #traceback.print_exc()

    # summary & model & salesrank
    try:

        pd = t.xpath('//td[h2="Product Details"]//div[@class="content"]//ul')[0]
        summarys = []
        for l in pd.xpath(".//li"):
            lc = l.text_content()
            if 'Shipping' in lc or 'Review' in lc or 'Rank' in lc:
                continue
            summarys.append(lc.strip())
        p.summary = '\n'.join(summarys) 
        p.model = pd.xpath('li[contains(b, "model")]')[0].text_content().split()[-1]
        p.salesrank = pd.xpath('li[@id="SalesRank"]')[0].text_content().replace('\n','').split(':',1)[1]
        p.salesrank = re.sub('\(.*(}|\))', '', p.salesrank).strip()
    except:
        pass
        #traceback.print_exc()

    p.full_update_time = datetime.utcnow()

    p.save()

if __name__ == '__main__':
    fetch_indexes()
    process_indexes()
    fetch_products()
    process_products()
