# -*- coding: utf-8 -*-
'''
crawlers.venteprivee.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

Created on 2012-11-16

@author: ethan
'''

from crawlers.common.events import *
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
        pass

    def crawl_category(self, ctx):
        """.. :py:method::
            from self.event_url get all the events
        """
        sales = vclient.sales()
        for sale in sales:
            print(DB+'.event.{0}.start'.format(sale.get('name').encode('utf-8')))
            
            is_updated = False
            event, is_new = Event.objects.get_or_create(event_id = str(sale.get('operationId')))
            event.combine_url = 'https://us.venteprivee.com/main/#/catalog/%s' % event.event_id
            event.sale_title = sale.get('name')
            event.image_urls = []#"http://pr-media04.venteprivee.com/is/image/VPUSA/%s" # TODO
            event.sale_description = sale.get('brandDescription')
            event.events_begin = datetime.datetime.strptime(sale.get('startDate'), '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.utc)
            event.events_end = datetime.datetime.strptime(sale.get('endDate'), '%Y-%m-%dT%H:%M:%S').replace(tzinfo=pytz.utc)
            event.type = sale.get('type')
            event.dept = []# TODO cannot get the info
            event.urgent = True
            event.save()
            
            print(DB+'.event.{0}.end'.format(sale.get('name').encode('utf-8')))
            common_saved.send(sender=ctx, key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=(not is_new) and is_updated)

    def crawl_listing(self, url, ctx):
        """.. :py:method::
            not useful
        :param url: event url with event_id 
        """
        print(DB+'.listing.{0}.start'.format(url))
        
        event_id = url.split('/')[-1]
        event = Event.objects.get(event_id = event_id)
        if  not event or event.type == 'upcoming':
            print(DB+'.listing.{0}.end'.format(url))
            return
        
        accounts = (('ethan@favbuy.com', '200591qq'), ('huanzhu@favbuy.com', '4110050209'))
        e, p = random.choice(accounts)
        driver = webdriver.Firefox() if DEBUG else webdriver.Chrome()
        
        # Signin with email as username and password to get the access to the api.
        sign_url = 'https://us.venteprivee.com/main/#/signin'
        driver.get(sign_url)
        email = driver.find_elements_by_id('sign_in_email')[0]
        email.send_keys(e)
        password = driver.find_elements_by_id('sign_in_password')[0]
        password.send_keys(p)
        submit = driver.find_element_by_xpath('//button[@type="submit"]')
        submit.click()
        time.sleep(2)
        
        driver.get(url)
        dom = html.fromstring(driver.page_source)
        driver.close()
        
        productsNode = dom.xpath('//dto_productfamily')
        for pNode in productsNode:
            is_updated = False
            key = pNode.xpath('./productfamilyid')[0].text
            product, is_new = Product.objects.get_or_create(key=key)
            product.title =  pNode.xpath('./name')[0].text
            product.price = pNode.xpath('./formattedmsrp')[0].text
            product.listprice = pNode.xpath('./formattedprice')[0].text
            product.soldout =  pNode.xpath('./issoldout')[0].text == "true"
            if event_id not in product.event_id:
                product.event_id.append(event_id)
            if is_new:
                product.combine_url = 'https://us.venteprivee.com/main/#/product/%s/%s' % (event_id, product.key)
                product.updated = False
            product.save()
            
            print(DB+'.listing.product.{0}.crawled'.format(product.key))
            common_saved.send(sender=ctx, key=product.key, url=url, is_new=is_new, is_updated=(not is_new) and is_updated)
        
        print(DB+'.listing.{0}.end'.format(url))

    def crawl_product(self, url, ctx):
        """.. :py:method::
            Got all the product information and save into the database
        :param url: product url, with product id
        """
        print(DB+'.product.{0}.start'.format(url))
        
        res = vclient.request(url)
        is_updated = False
        
        split_url = url.split('/')
        key = split_url[-1]
        event_id = split_url[-2]
        product, is_new = Product.objects.get_or_create(key=key)
        
        product.title = res.get('name')
        product.brand = res.get('operationName')
        if is_new:
            product.combine_url = 'https://us.venteprivee.com/main/#/product/%s/%s' % (event_id, product.key)
        product.listprice = res.get('formattedPrice')
        product.price = res.get('formattedMsrp')
        product.image_urls = [] # TODO
        product.list_info = [] # TODO
        product.soldout = res.get('isSoldOut')
        product.returned = res.get('returnPolicy')
        product.sizes = res.get('sizes')
        product.sizes_scarcity = [] #TODO
        product.updated = False if is_new else True
        product.full_update_time = datetime.datetime.utcnow()
        product.save()
        
        print(DB+'.product.{0}.end'.format(url))
        common_saved.send(sender=ctx, key=product.key, url=url, is_new=is_new, is_updated=(not is_new) and is_updated)

if __name__ == '__main__':
#    server = zerorpc.Server(Server())
#    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
#    server.run()
    
    start = time.time()
    
    s = Server()
    s.crawl_category('venteprivee')
    events = Event.objects(urgent=True).order_by('-update_time').timeout(False)
    for event in events:
        s.crawl_listing(event.url(), 'venteprivee')
    products = Product.objects.filter(updated=False)
    for product in products:
        s.crawl_product(product.url(), 'gilt')
    
    print 'total costs: %s (s)' % (time.time() - start) 
