# -*- coding: utf-8 -*-
"""
Tools for server to process images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""
from configs import *

import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection

from hashlib import md5
import os
import json
import requests
from PIL import Image, ImageChops
from cStringIO import StringIO

from helpers.log import getlogger
imglogger = getlogger('powertools', filename='/tmp/powerserver.log')

CURRDIR = os.path.dirname(__file__)

from imglib import scale, trim, crop

policy = {
  "Version": "2008-10-17",
  "Statement": [{
    "Sid": "AllowPublicRead",
    "Effect": "Allow",
    "Principal": { "AWS": "*" },
    "Action": ["s3:GetObject"],
    "Resource": ["arn:aws:s3:::{0}/*".format(S3_IMAGE_BUCKET) ]
  }]
}

class ImageTool:
    """
    The class about images to power image data to the front-end.
    * Grab the picture from the url of other websites and uplaod it to storage server, such as S3.
    * Thumbnail the picture and uplaod it to the storage server, such as S3 .
    * Provide the picture url to the front-end after dealt wit.
    
    * To use PIL in ubuntu, several steps as followed should be done:
    # sudo apt-get install libjpeg8-dev
    # sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so ~/.virtualenvs/crpc/lib/
    # pip install Pillow
    """
    def __init__(self, connection=None, bucket_name=S3_IMAGE_BUCKET):
        if connection is None:
            connection = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
        self.__s3conn = connection
        try:
            bucket = self.__s3conn.get_bucket(bucket_name)
        except boto.exception.S3ResponseError, e:
            if '404' in repr(e):
                bucket = self.__s3conn.create_bucket(bucket_name)
                bucket.set_policy(json.dumps(policy))
            else:
                imglogger.error('Connect to bucket {0} exception: {1}'.format(bucket_name, str(e)))
                raise
        self.__bucket = bucket
        self.__key = Key(bucket)
        self.__image_path = []
        self.__image_complete = False

    # @property
    # def image_resolutions(self):
    #     return self.__image_resolutions

    @property
    def image_complete(self):
        return self.__image_complete

    @property
    def image_path(self):
        return self.__image_path
  
    def crawl(self, image_urls=[], site='', doctype='', key='', timeline=0, thumb=False):
        """ process all the image stuff """
        if len(image_urls) == 0:
            self.__image_complete = True
            return
        
        for image_url in image_urls:
            imglogger.debug("processing {0}".format(image_url))
            path, filename = os.path.split(image_url)
            index = image_urls.index(image_url)
            image_name = '%s_%s_%s' % (md5(filename).hexdigest(), index, timeline)

            self.__key.key = os.path.join(site, doctype, key, image_name)
            image_content = None

            exist_keys = list(k.key for k in self.__bucket.list(prefix=self.__key.key))
            if not exist_keys:
                try:
                    image_content = self.download(image_url)
                    if not image_content:
                        imglogger.error('download image {0}.{1}.{2}.{3} not exist'.format(site, doctype, key, image_url))
                        continue
                except Exception, e:
                    imglogger.error('download image {0}.{1}.{2}.{3} exception: {4}'.format(site, doctype, key, image_url, str(e)))
                    continue

                try:
                    self.upload2s3(StringIO(image_content), self.__key.key)
                except Exception, e:
                    imglogger.error('upload image {0}.{1}.{2}.{3} exception: {4}'.format(site, doctype, key, image_url, str(e)))
                    return

            resolutions = []
            s3_url = '{0}/{1}'.format(S3_IMAGE_URL, self.__key.key)
            if thumb:
                if doctype.capitalize() == 'Product' or \
                    (doctype.capitalize() == 'Event' and not self.__image_path):
                        resolutions = self.thumbnail_and_upload(doctype, image_content, self.__key.key, exist_keys)

            self.__image_path.append({'url':s3_url, 'resolutions':resolutions})

        self.__image_complete = bool(self.__image_path)

    def download(self, image_url):
        """ download image from image_url

        :param image_url: an url to the image
        
        Returns the content of the image
        """
        r = requests.get(image_url)
        r.raise_for_status()
        # Sometimes the picture does not exist and \
        # the site response a 200 html page to indicate the error.
        if 'text/html' in r.headers.get('Content-Type', ''):
            return None
        return r.content

    def upload2s3(self, image, key):
        """ upload image to s3 in key 

        :param image: fileobj for an image
        :param key: s3 key name

        Returns None
        """
        self.__key.key = key
        self.__key.set_contents_from_file(image, headers={'Content-Type':'image/jpeg', 'Cache-Control':'max-age=31536000, public'})
        # self.__key.make_public()

    def thumbnail_and_upload(self, doctype, image, s3key, exist_keys):
        """ creates thumbnail and upload them to s3

        :param doctype: either 'event' or 'product'
        :param image: an fileobj of image
        :param s3key: a (s3) path/key to image
        :param exist_keys: exist keys prefix in s3key
    
        Returns resolutions of thumbnails
        """
        s3_url = '{0}/{1}'.format(S3_IMAGE_URL, s3key)
        imglogger.info("thumbnail&upload @ {0}".format(s3key))

        im = Image.open(StringIO(image)) if image else None

        resolutions = []
        for size in IMAGE_SIZE[doctype.capitalize()]:
            width, height = size['width'], size['height']
            policy, color = size['thumbnail-policy'], size['background-color']

            skip = False
            for key in exist_keys:
                if '_{0}x'.format(width) in key:
                    rwidth, rheight = key.rsplit('_',1)[-1].split('x')
                    rwidth, rheight = int(rwidth), int(rheight)
                    if height == 0 or height == rheight:
                        resolutions.append((int(rwidth), int(rheight)))
                        skip = True
                        break
            if skip:
                continue

            if not im:
                im = Image.open(StringIO(self.download(s3_url)))

            fileobj, realsize = self.create_thumbnail(im, (width, height), policy, color)
            width, height = realsize
            resolutions.append(realsize)

            path, name = os.path.split(s3key)
            thumbnail_name = '{name}_{width}x{height}'.format(width=width, height=height, name=name)
            self.__key.key = os.path.join(path, thumbnail_name)
            self.upload2s3(fileobj, self.__key.key)

        return resolutions

    def create_thumbnail(self, im, size, policy, color):
        """ create thumbnail from a size
            
        :param im: an Image object opened by PIL
        :param size: a tuple (width, height)
    
        Returns a fileobj(an StringIO instance))
        """
        width, height = size

        if policy == 'scale-trim':
            # im = trim(im)
            if height == 0:
                height = int(round(1. * im.size[1] * width/im.size[0]))
            im = scale(im, (width, height), bgcolor=color)
        elif policy == 'crop':
            im = crop(im, size)
        else:
            raise ValueError("unsupported thumbnail policy")

        fileobj = StringIO()
        try:
            im.save(fileobj, 'JPEG', quality=95)
        except IOError, e:
            if im.mode != "RGB":
                imglogger.debug('{0} mode require RGB mode to save as JPEG.'.format(im.mode))
                im = im.convert("RGB")
                im.save(fileobj, 'JPEG', quality=95)
        fileobj.seek(0)

        return fileobj, (width, height)


def test_image(site, doctype, key):
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    doctype = doctype.capitalize()
    m = __import__('crawlers.'+site+'.models', fromlist=[doctype])
    params = {
        'Event': {
            'event_id': key,
        },
        'Product': {
            'key': key,
        }
    }
    urls = getattr(m, doctype).objects(**params[doctype]).first()['image_urls']
    print 'image urls:'
    for url in urls:
        print url
    print

    it = ImageTool(connection = conn)
    it.crawl(urls, site, doctype, key, thumb=True)
    print 'image path ---> {0}'.format(it.image_path)
    print 'complete ---> {0}\n'.format(it.image_complete)


if __name__ == '__main__':
    import sys
    from optparse import OptionParser

    parser =  OptionParser(usage='usage: %prog [options]')
    parser.add_option('-t', '--test', dest='test_image', action='store_true', help='test image upload', default=False)

    option, args = parser.parse_args(sys.argv[1:])
    if option.test_image:
        site, doctype, key = args
        test_image(site, doctype, key)
