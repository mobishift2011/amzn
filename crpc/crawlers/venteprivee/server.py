# -*- coding: utf-8 -*-
'''
crawlers.venteprivee.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

Created on 2012-11-16

@author: ethan
'''

from crawlers.common.events import *
from crawlers.common.crawllog import debug_info
from crawlers.common.stash import config, headers
from models import *

import datetime, time
import pytz
import random
from lxml import html
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import zerorpc

DEBUG = False

class Server(object):
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    def __init__(self):
        self.__is_auth = False
        self.request = None
    
    def auth(self):
        return self.__is_auth
    
    def login(self):
        accounts = (('ethan@favbuy.com', '200591qq'), ('huanzhu@favbuy.com', 'abcd1234'))
        email, password = random.choice(accounts)
        
        url = 'https://us.venteprivee.com/api/membership/signin'
        data = {
            'email': email,
            'password': password,
            'rememberMe': False,
        }
        self.request = requests.Session(prefetch=True, timeout=30, config=config, headers=headers)
        res = self.request.post(url, data=data)
        res.raise_for_status()
        self.__is_auth = True

    def crawl_category(self, ctx):
        """.. :py:method::
            from self.event_url get all the events
        """
        sales = vclient.sales()
        for sale in sales:
            debug_info.send(sender=DB+'.event.{0}.start'.format(sale.get('name').encode('utf-8')))
            
            is_updated = False
            event, is_new = Event.objects.get_or_create(event_id = str(sale.get('operationId')))
            event.combine_url = 'https://us.venteprivee.com/main/#/catalog/%s' % event.event_id
            event.sale_title = sale.get('name')
            for media in ['home', 'icon', 'preview']:
                image_url = "http://pr-media04.venteprivee.com/is/image/VPUSA/{0}".format(sale.get('media').get(media))
                if image_url not in event.image_urls:
                    event.image_urls.append(image_url)
            event.sale_description = sale.get('brandDescription')
            event.events_begin = datetime.datetime.strptime(sale.get('startDate'), '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.utc)
            event.events_end = datetime.datetime.strptime(sale.get('endDate'), '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.utc)
            event.type = sale.get('type')
            event.dept = [] # TODO cannot get the info
            event.urgent = is_new or event.urgent
            event.save()
            
            debug_info.send(sender=DB+'.event.{0}.end'.format(sale.get('name').encode('utf-8')))
            common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=(not is_new) and is_updated)

    def crawl_listing(self, url, ctx):
        """.. :py:method::
            not useful
        :param url: event url with event_id 
        """
        debug_info.send(sender=DB+'.listing.{0}.start'.format(url))
        if not self.auth():
            self.login()
        
        response = self.request.get(url)
        if int(response.status_code) != 200:
            common_failed.send(sender=ctx, key='', url=url, reason="%s: upcoming events has no products to crawl" % response.status_code)
            return
        res = response.json
        
        event_id = str(res.get('operationId'))
        products = res.get('productFamilies')
        for prodNode in products:
            is_updated = False
            key = str(prodNode['productFamilyId'])
            product, is_new = Product.objects.get_or_create(key=key)
            
            if not is_new:
                is_updated = (product.price != prodNode.get('formattedPrice')) or is_updated
                is_updated = (product.soldout != prodNode.get('isSoldOut')) or is_updated
            
            product.title =  prodNode.get('name')
            product.price = prodNode.get('formattedPrice')
            product.listprice = prodNode.get('formattedMsrp')
            product.soldout =  prodNode.get('isSoldOut')
            if event_id not in product.event_id:
                product.event_id.append(event_id)
            if is_new:
                product.combine_url = 'https://us.venteprivee.com/main/#/product/%s/%s' % (event_id, product.key)
                product.updated = False
            product.save()
            
            debug_info.send(sender=DB+'.listing.product.{0}.crawled'.format(product.key))
            common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=url, is_new=is_new, is_updated=(not is_new) and is_updated)
        
        ready = False
        event = Event.objects.get(event_id=event_id)
        if event and event.urgent:
            event.urgent = False
            ready = True
            event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=False, is_updated=False, ready=ready)
        
        debug_info.send(sender=DB+'.listing.{0}.end'.format(url))

    def crawl_product(self, url, ctx):
        """.. :py:method::
            Got all the product information and save into the database
        :param url: product url, with product id
        """
        debug_info.send(sender=DB+'.product.{0}.start'.format(url))
        if not self.auth():
            self.login()
        
        is_updated = False
        ready = False
        res = self.request.get(url).json
        key = str(res.get('productFamilyId'))
        
        product, is_new = Product.objects.get_or_create(key=key)
        if not is_new:
            is_updated = (product.price != res.get('formattedPrice')) or is_updated
            is_updated = (product.soldout != res.get('isSoldOut')) or is_updated
        
        product.title = res.get('name')
        product.brand = res.get('operationName')
#        if is_new:
#            # TODO
#            product.combine_url = 'https://us.venteprivee.com/main/#/product/%s/%s' % (event_id, product.key)
        product.listprice = res.get('formattedMsrp')
        product.price = res.get('formattedPrice')
        for det in res.get('media').get('det'):
            image_url = 'http://pr-media01.venteprivee.com/is/image/VPUSA/%s' % det.get('fileName')
            if image_url not in product.image_urls:
                product.image_urls.append(image_url)
        product.list_info = [] # TODO
        product.soldout = res.get('isSoldOut')
        breadCrumb = res.get('breadCrumb').get('name')
        if breadCrumb not in product.dept:
            product.dept.append(breadCrumb)
        product.returned = res.get('returnPolicy')
        product.sizes = []#res.get('sizes')    # TODO
        product.sizes_scarcity = [] # TODO
        temp_updated = product.updated
        product.updated = False if is_new else True
        if product.updated:
            product.full_update_time = datetime.datetime.utcnow()
            if not temp_updated and product.updated:
                ready = True
        product.save()
        
        common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=url, is_new=is_new, is_updated=(not is_new) and is_updated, ready=ready)
        debug_info.send(sender=DB+'.product.{0}.end'.format(url))

if __name__ == '__main__':
#    server = zerorpc.Server(Server())
#    server.bind("tcp://0.0.0.0:{0}".format(CRAWLER_PORT))
#    server.run()

    start = time.time()
    
    s = Server()
    s.crawl_category('venteprivee')
    events = Event.objects(urgent=True)
    for event in events:
        s.crawl_listing(event.url(), 'venteprivee')
    products = Product.objects.filter(updated=False)
    for product in products:
        s.crawl_product(product.url(), 'ventiprivee')
    
    print 'total costs: %s (s)' % (time.time() - start)
