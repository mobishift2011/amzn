# -*- coding: utf-8 -*-
"""
crawlers.myhabit.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""

import os
import time
from StringIO import StringIO
import requests

import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection

from configs import *
from pymongo import Connection
connection = Connection()


class ImageTool:
    """
    The class about images to power image data to the front-end.
    * Grab the picture from the url of other websites and save it to the local env, such as S3.
    * Thumnail the picture.
    * Provide the picture url to the front-end after dealt wit.
    """
    def __init__(self, s3conn):
        self.__s3conn = s3conn
    
    def query(self, dbname=None):
        db = connection[dbname]
        return db.product.find({'updated': True})
    
    def crawl(self, product, site):
        if product.get('image_urls') and not product.get('s3_image_urls'):
            product['s3_image_urls'] = map(lambda x: self.grab(x, os.path.join(IMAGE_ROOT, site), site, product), product.get('image_urls'))
            product.save()
    
    def grab(self, image_url, folder, site, product):
        path, filename = os.path.split(image_url)
        image_name = '%s_%s_%s' % (site, product['_id'], filename)
        with open(os.path.join(folder, image_name), 'wb') as f:
            image = requests.get(image_url).content
            f.write(image)
        return self.upload2s3(open(f.name), os.path.join(site, image_name)) # post image file to S3, and get back the url. 

    def thumnail(self):
        pass

    def upload2s3(self, image, key, bucket_name=IMAGE_S3_BUCKET):
        try:
            bucket = self.__s3conn.get_bucket(bucket_name)
        except boto.exception.S3ResponseError, e:
            if str(e).find('404 Not Found'):
                bucket = self.__s3conn.create_bucket(bucket_name)
            else:
                raise
        k = Key(bucket)
        k.key = key
        return k.generate_url(URL_EXPIRES_IN)


if __name__ == '__main__':
    imgTool = ImageTool(S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY))
    for dbname in DBS:
        db = connection[dbname]
        products = db.product.find({'updated': True})
        for product in products:
            imgTool.crawl(product, dbname)
            product.get('_id')
            break # TO REMOVE