# -*- coding: utf-8 -*-
"""
crawlers.myhabit.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""
from configs import *

import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection

import os
import requests
from PIL import Image
from StringIO import StringIO

CURRDIR = os.path.dirname(__file__)

class ImageTool:
    """
    The class about images to power image data to the front-end.
    * Grab the picture from the url of other websites and uplaod it to storage server, such as S3.
    * Thumbnail the picture and uplaod it to the storage server, such as S3 .
    * Provide the picture url to the front-end after dealt wit.
    
    * To use PIL in ubuntu, several steps as followed should be done:
    # sudo apt-get install libjpeg8-dev
    # sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so ~/.virtualenvs/crpc/lib/
    # pip install PIL
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
        path, filename = os.path.split(image_url)
        image_name = '%s_%s_%s_%s' % (site, key, index, filename)
        
        image = requests.get(image_url).content
        image_content = StringIO(image)
        ret = ''
        try:
            ret = self.upload2s3(image_content, os.path.join(site, image_name)) # post image file to S3, and get back the url.
        except:
            print 's3 upload failed! %s' % image_name

        if index == 0:
            self.thumbnail('Product', StringIO(image), image_name)    # TODO add doctype

        return ret
    

    def upload2s3(self, image, key):
        print "%s.upload2s3:" % (key)
        self.__key.key = key
        self.__key.set_contents_from_file(image)
        return self.__key.generate_url(URL_EXPIRES_IN)


    def thumbnail(self, doctype, image, image_name):
        thumb_picts = {}
        im = Image.open(image)
        for size in IMAGE_SIZE[doctype.capitalize()]:
            width = size.get('width')
            height = size.get('height')
            fluid = size.get('fluid')

            width_rate = 1.0 * width / im.size[0]
            height_rate = 1.0 * height / im.size[1]
            rate = max(width_rate, height_rate)

            print 'thumbnail %s with size width: %s, heigh: %s' % (im.size, width, height)           
            pict = self.resize_by_rate(rate, im) \
                    if fluid == True or width == 0 or height == 0 \
                        else self.resize_by_crop(width=width, height=height, im=im)

            thumbnail_url = self.upload2s3(pict, '%sx%s_%s' % (width, height, image_name))
            if thumbnail_url:
                thumb_picts['%sx%s' % (width, height)] = thumbnail_url

        return thumb_picts


    def resize(self, box, im):
        thumbnail = im.resize(box)
        tempfile = StringIO()
        thumbnail.save(tempfile, im.format)
        tempfile.seek(0)
        return tempfile


    def resize_by_rate(self, rate, im):
        width, height = im.size
        size = tuple([int(i * rate) for i in im.size])
        return self.resize(size, im)


    def resize_by_crop(self, width=0, height=0, im=None):
        width_rate = 1.0 * width / im.size[0]
        height_rate = 1.0 * height / im.size[1]
        rate = max(width_rate, height_rate)

        (im.size[0]*rate, im.size[1]*rate)
        thumnail = im.resize( tuple( [int(i*rate) for i in im.size] ) )
        left = (thumnail.size[0] - width) / 2  if (thumnail.size[0] - width) > 0 else 0
        upper = (thumnail.size[1] - height) / 2 if (thumnail.size[1] - height) > 0 else 0
        right = left + width
        lower = upper + height
        box = (left, upper, right, lower)
        region = thumnail.crop(box)

        tempfile = StringIO()
        region.save(tempfile, im.format)
        tempfile.seek(0)
        return tempfile


if __name__ == '__main__':
    pass
    urls = ['http://cdn1.gilt.com/images/share/uploads/0000/0001/7211/172111475/orig.jpg', 'http://cdn1.gilt.com/images/share/uploads/0000/0001/2432/124321099/1080x1440.jpg','http://cdn1.gilt.com/images/share/uploads/0000/0001/2978/129781958/1080x1440.jpg']
    url = 'http://cdn1.gilt.com/images/share/uploads/0000/0001/2978/129781958/1080x1440.jpg'
    image_content = StringIO(requests.get(url).content)

    import time
    start = time.time()
    it = ImageTool()
    thum_picts = it.thumbnail('Product', image_content, 'lala')
    print thum_picts

    print time.time() - start, 's'
