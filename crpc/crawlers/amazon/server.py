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
import requests
import lxml.html

from urllib import quote, unquote
from datetime import datetime, timedelta

from models import *
from settings import *

from crawlers.common.events import category_saved, category_failed, category_deleted
from crawlers.common.events import product_saved, product_failed, product_deleted

    
class Server:
    def __init__(self):
        self.s = requests.session(headers={'User-Agent':'Mozilla 5.0/b'})
        self.site = "amazon"
        
    def crawl_category(self):
        """ crawl all category info """
        pass

    def crawl_listing(self, url):
        """ crawl listing page """
        content = self.fetch_page(url)
        self.parse_listing(url, content)
        
    def crawl_product(self, url):
        """ crawl product page """
        content = self.fetch_page(url)
        self.parse_product(url, content)
        
    def fetch_page(self, url):
        r = s.get(url)
        if r.status_code == 200:
            return r.content
        elif r.status_code == 404:
            raise ValueError('page not found')
        else:
            raise ValueError('the crawler seems to be banned!!')
    
    def parse_listing(self, url, content):
        """ index info about each product -> db """
        t = lxml.html.fromstring(content)
        for block in t.xpath('//div[starts-with(@id,"result_")]'):
            self._parse_block(block, url)

    def _parse_block(self, block, url):
        """ parse and save product info for a block of listing page """
        try:
            link = block.xpath(".//a")[0].get("href")
        except:
            continue
    
        m = re.compile(r'http://www.amazon.com/(.*)/dp/(.*?)/').search(link)
        if not m:
            m = re.compile(r'http://www.amazon.com/(.*)/dp/(.*)').search(link)
   
        if m:
            slug, key = m.group(1), m.group(2)  
  
            is_new = False
            p = Product.objects(key=key).first()
            if not p:
                p = Product(key=key)
                is_new = True
                
            # deal with multiple category
            catn = url2catn(url)
            if catn not in p.catns:
                p.catns.append(catn)

            c = Category.objects(catn=catn).first()
            if c:
                p.cats = c.cats

            # some infomation we just update once and kept it forever
            if is_new:
                p.slug = slug
                p.cover_image_url = block.xpath(".//img")[0].get('src')
                p.list_update_time = datetime.utcnow()
                p.updated = False

            # others we might want to update it more frequently
            is_updated = False
            try:
                price = block.xpath('.//div[@class="newPrice"]')[0].xpath(".//span")[-1].text_content().strip()[1:].replace(',','')
                if price != p.price:
                    p.price = price
                    is_updated = True
            except:
                pass

            try:
                p.save()
            except Exception as e:
                raise ValueError("validation failed")
            else:
                product_saved.send(sender = "amazon.parse_listing", 
                                    site = self.site,
                                    key = p.key,
                                    is_new = is_new,                        
                                    is_updated = is_updated)
    
    def parse_product(self, url, content):
        if url.endswith('/'):
            key = url.split('/')[-2] 
        else:
            key = url.split('/')[-1] 

        is_new = False
        p = Product.objects(key=key).first()
        if not p:
            p = Product(key=key)
            is_new = True

        t = lxml.html.fromstring(content)

        p.title = t.xpath('//*[@id="btAsinTitle"]')[0].text_content()
        is_updated = False
    
        try:
            p.brand = t.xpath('//h1[@class="parseasinTitle "]/following-sibling::*/a[@href]')[0].text_content().strip()
            p.vartitle = t.xpath('//span[@id="variationProductTitle"]')[0].text_content().strip()
        except:
            pass
    
        # like
        try:
            rating = t.xpath('//*[@id="handleBuy"]/div[2]/span[1]/span/span/a/span')[0].get('title').split()[0]
            like = t.xpath('//span[@class="amazonLikeCount"]')[0].text_content().replace(',','')
            num_reviews = t.xpath('//div[@class="jumpBar"]//span[@class="crAvgStars"]/a')[0].text_content().replace(',','').split()[0]
        except:
            rating, like, num_reviews = "", "", ""
    
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
            sales_rank = pd.xpath('li[@id="SalesRank"]')[0].text_content().replace('\n','').split(':',1)[1]
            sales_rank = re.sub('\(.*(}|\))', '', sales_rank).strip()
        except:
            sales_rank = ""
    
        p.full_update_time = datetime.utcnow()
        p.updated = True
    
        for name in ['rating','like','num_reviews','sales_rank']:
            if getattr(p, name) != locals()[name]:
                setattr(p, name, locals()[name])
                is_updated = True
    
        try:
            p.save()
        except Exception as e:
            raise ValueError("validation failed")
        else:
            product_saved.send(sender = "amazon.parse_listing", 
                                site = self.site,
                                key = p.key,
                                is_new = is_new,                        
                                is_updated = is_updated)

if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
    server.run()
