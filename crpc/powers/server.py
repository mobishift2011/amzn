# -*- coding: utf-8 -*-
"""
crawlers.common.rpcserver
~~~~~~~~~~~~~~~~~~~~~~~~~

Provides a image processed workflow for all callers

"""

from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool

import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection

from configs import SITES, AWS_ACCESS_KEY, AWS_SECRET_KEY
from Image import ImageTool

def get_models():
    ret = []
    for db in SITES:
        model = __import__("crawlers."+db+'.models', fromlist=['Event', 'Product'])
        ret.append((model.Event, model.Product))
    return

def spout_events(Event):
    events = Event.objects(image_done=False)
    for event in events:
        return {
            'site': site,
            'event_id': event.event_id,
            'image_urls': event.image_urls,
        }
        

def spout_products(Product):
    products = Product.objects(image_done=False)
    for product in products:
        return {
            'key': product.key,
            ''
        
        }

def serve():
    imgTool = ImageTool(S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY))
    for Event, Product in get_models():
        events = 
        products = Product.objects(image_done=False)
        imgTool.crawl(product, dbname)