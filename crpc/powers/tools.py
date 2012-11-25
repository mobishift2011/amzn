# -*- coding: utf-8 -*-
"""
crawlers.myhabit.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""

import os
import requests
from StringIO import StringIO

import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection

from configs import *

CURRDIR = os.path.dirname(__file__)

class ImageTool:
    """
    The class about images to power image data to the front-end.
    * Grab the picture from the url of other websites and save it to the local env, such as S3.
    * Thumnail the picture.
    * Provide the picture url to the front-end after dealt wit.
    """
    def __init__(self, s3conn=None, bucket_name=IMAGE_S3_BUCKET):
        self.__s3conn = s3conn or S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
        try:
            bucket = self.__s3conn.get_bucket(bucket_name)
        except boto.exception.S3ResponseError, e:
            if str(e).find('404 Not Found'):
                bucket = self.__s3conn.create_bucket(bucket_name)
            else:
                raise
        self.__key = Key(bucket)
    
    def crawl(self, image_urls=[], site=None, key=None):
        print "%s.%s.images_crawling.start" % (site, key)
        image_path = []
        for image_url in image_urls:
            s3_url = self.grab(image_url, site, key, image_urls.index(image_url))
            if s3_url:
                image_path.append(s3_url)
            else:
                image_path = []
                break
        
        print "%s.%s.images_crawling.end" % (site, key)
        return image_path
    
    def grab(self, image_url, site=None, key=None, index=0):
#        print "\n%s.%s.image_url.save_as_temp_file:" % (site, key)
        path, filename = os.path.split(image_url)
        image_name = '%s_%s_%s_%s' % (site, key, index, filename)
        
        # TODO update the temp file to memory based image, not through the disk.
        image = requests.get(image_url).content
        image_content = StringIO(image)
        ret = ''
        try:
            ret = self.upload2s3(image_content, os.path.join(site, image_name)) # post image file to S3, and get back the url.
        except:
            print 's3 upload failed! %s' %image_name
        return ret
    
    def thumnail(self):
        pass
    
    def upload2s3(self, image_content, key):
        print "%s.upload2s3:" % (key)
        self.__key.key = key
        self.__key.set_contents_from_file(image_content)
        return self.__key.generate_url(URL_EXPIRES_IN)


if __name__ == '__main__':
    pass