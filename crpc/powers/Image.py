# -*- coding: utf-8 -*-
"""
crawlers.myhabit.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""

import os
from StringIO import StringIO
import requests
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
    def __init__(self):
        map(self.query, DBS)
    
    def query(self, dbname=None):
        db = connection[dbname]
        products = db.product.find({'updated': True})
        for product in products:
            if product.get('image_urls'):
                for p in product.get('image_urls'):
                    print p
                product['image_urls_s3'] = map(lambda x: self.grab(x, os.path.join(IMAGE_ROOT, dbname)), product.get('image_urls'))
                for p in product.get('image_urls_s3'):
                    print p
            return # TO REMOVE
    
    def grab(self, image_url, folder):
        path, filename = os.path.split(image_url)
        with open(os.path.join(folder, filename), 'wb') as f:
            image = requests.get(image_url).content
            f.write(image)
        # TO POST IMAGE TO S3
        return f.name
    
    def thumnail(self):
        pass
    
    def power(self):
        pass

ImageTool()