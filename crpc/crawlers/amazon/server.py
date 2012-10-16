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

from urllib import quote, unquote
from datetime import datetime, timedelta

from models import *
from settings import *

s = requests.session(headers={'User-Agent':'Mozilla 5.0/b'})
    
class Server:
    def crawl_listing(self, url):
        content = self.fetch_page(url)
        self.parse_listing(url, content)
        
    def crawl_product(self, url):
        content = self.fetch_page(url)
        self.parse_product(url, content)
        
    def fetch_page(self, url):
        r = s.get(url)
        if r.status_code == 200:
            return r.content
        elif r.status_code == 404:
            return ''
        else:
            raise ValueError('the crawler seems to be banned!!')
    
    def parse_listing(self, url, content):
        """ index info about each product -> db """
        t = lxml.html.fromstring(content)
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
    
                is_new = False
                p = Product.objects(asin=asin).first()
                if not p:
                    p = Product(asin=asin)
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
                try:
                    p.price = float(block.xpath('.//div[@class="newPrice"]')[0].xpath(".//span")[-1].text_content().strip()[1:].replace(',',''))
                except:
                    try:
                        p.pricestr = block.xpath('.//div[@class="newPrice"]')[0].text_content().strip()
                    except:
                        pass
    
                p.save()
    
    def parse_product(self, url, content):
        if url.endswith('/'):
            asin = url.split('/')[-2] 
        else:
            asin = url.split('/')[-1] 

        is_new = False
        p = Product.objects(asin=asin).first()
        if not p:
            p = Product(asin=asin)
            is_new = True

        # might not available
        if not content:
            try:
                p.delete()
            except:
                pass
            return

        t = lxml.html.fromstring(content)

        p.title = t.xpath('//*[@id="btAsinTitle"]')[0].text_content()
    
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
        p.updated = True
    
        p.save()

if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
    server.run()
