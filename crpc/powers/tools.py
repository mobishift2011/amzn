# -*- coding: utf-8 -*-
"""
Tools for server to processing data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""
from gevent import monkey; monkey.patch_all()
from gevent.coros import Semaphore
from gevent.pool import Pool
from functools import partial
from collections import Counter

from configs import *

import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection

from hashlib import md5
import os
import re
import json
import requests
import urllib
import Image, ImageChops
from cStringIO import StringIO
from datetime import datetime

from helpers.log import getlogger
txtlogger = getlogger('powertools', filename='/tmp/textserver.log')
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
    # pip install PIL
    """
    def __init__(self, connection=None, bucket_name=S3_IMAGE_BUCKET):
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
  
    def crawl(self, image_urls=[], site='', doctype='', key='', thumb=False):
        """ process all the image stuff """
        if len(image_urls) == 0:
            self.__image_complete = True
            return

        for image_url in image_urls:
            imglogger.debug("processing {0}".format(image_url))
            path, filename = os.path.split(image_url)
            index = image_urls.index(image_url)
            image_name = '%s_%s' % (md5(filename).hexdigest(), index)

            self.__key.key = os.path.join(site, doctype, key, image_name)
            image_content = None

            exist_keys = list(k.key for k in self.__bucket.list(prefix=self.__key.key))
            if not exist_keys:
                try:
                    image_content = self.download(image_url)
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
                    (doctype.capitalize() == 'Event' and index == 0):
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
        return r.content

    def upload2s3(self, image, key):
        """ upload image to s3 in key 

        :param image: fileobj for an image
        :param key: s3 key name

        Returns None
        """
        self.__key.key = key
        self.__key.set_contents_from_file(image, headers={'Content-Type':'image/jpeg'})
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
                    width, height = key.rsplit('_',1)[-1].split('x')
                    resolutions.append((int(width), int(height)))
                    skip = True
                    break
            if skip:
                continue

            if not im:
                im = Image.open(StringIO(self.download(s3_url)))

            if height == 0:
                height = int(round(1. * im.size[1] * width/im.size[0]))
                
            resolutions.append((width, height))

            path, name = os.path.split(s3key)
            thumbnail_name = '{name}_{width}x{height}'.format(width=width, height=height, name=name)
            self.__key.key = os.path.join(path, thumbnail_name)

            fileobj = self.create_thumbnail(im, (width, height), policy, color)
            self.upload2s3(fileobj, self.__key.key)

        return resolutions

    def create_thumbnail(self, im, size, policy, color):
        """ create thumbnail from a size
            
        :param im: an Image object opened by PIL
        :param size: a tuple (width, height)
    
        Returns a fileobj(an StringIO instance))
        """
        if policy == 'scale-trim':
            im = scale(trim(im), size, bgcolor=color)
        elif policy == 'crop':
            im = crop(im, size)
        else:
            raise ValueError("unsupported thumbnail policy")
        fileobj = StringIO()
        im.save(fileobj, 'JPEG', quality=95)
        fileobj.seek(0)
        return fileobj
         
def parse_price(price):
    amount = 0
    pattern = re.compile(r'^\$?(\d+(,\d{3})*(\.\d+)?)')
    match = pattern.search(price)
    if match:
        amount = (match.groups()[0]).replace(',', '')
    return float(amount)

class Propagator(object):
    def __init__(self, site, event_id, extractor, classifier, module=None):
        print 'init propogate %s event %s' % (site, event_id)

        self.site = site
        self.extractor = extractor
        self.classifier = classifier
        
        self.__module = module if module else \
                        __import__('crawlers.{0}.models'.format(site), fromlist=['Event', 'Product', 'Category'])
        self.event = self.__module.Event.objects(event_id=event_id).first()

    def propagate(self):
        """
        * Tag, Dept extraction and propagation
        * Event brand propagation
        * Event (lowest, highest) discount, (lowest, highest) price propagation
        * Event & Product begin_date, end_date
        * Event soldout
        """
        if not self.event:
            return

        event_brands = set()
        tags = set()
        depts = Counter()
        lowest_price = 0
        highest_price = 0
        lowest_discount = 0
        highest_discount = 0
        events_begin = self.event.events_begin or None
        events_end = self.event.events_end or None
        soldout = True

        products = self.__module.Product.objects(event_id=self.event.event_id)
        print 'start to propogate %s event %s' % (self.site, self.event.event_id)

        counter = 0
        for product in products:
            if True:
            #try:
                print 'start to propogate from  %s product %s' % (self.site, product.key)

                # Tag, Dept extraction and propagation
                if product.favbuy_tag:
                    tags = tags.union(product.favbuy_tag)
                if product.favbuy_dept:
                    depts[product.favbuy_dept[0]] += 1

                # Event brand propagation
                if hasattr(product, 'favbuy_brand') and product.favbuy_brand:
                    event_brands.add(product.favbuy_brand)

                # Event & Product begin_date, end_date
                if not hasattr(product, 'products_begin') \
                    or not product.products_begin:
                        product.products_begin = events_begin
                if not hasattr(product, 'products_end') \
                    or not product.products_end:
                        product.products_end = events_end

                if not events_begin and product.products_begin:
                    events_begin = product.products_begin
                if not events_end and product.products_end:
                    events_end = product.products_end

                if events_begin and product.products_begin:
                    events_begin = min(events_begin, product.products_begin)
                if events_end and product.products_end:
                    events_end = max(events_end, product.products_end)

                # (lowest, highest) discount, (lowest, highest) price propagation
                try:
                    price = parse_price(product.price)
                except Exception, e:
                    txtlogger.error('{0}.product.{1} parse price -> {2} exception: {3}'.format(self.site, product.key, product.price, str(e)))
                    price = 0
                try:
                    listprice = parse_price(product.listprice) or price
                except Exception, e:
                    txtlogger.error('{0}.product.{1} parse listprice -> {2} exception: {3}'.format(self.site, product.key, product.listprice, str(e)))
                    listprice = price

                product.favbuy_price = str(price)
                product.favbuy_listprice = str(listprice)
                
                highest_price = max(price, highest_price) if highest_price else price
                lowest_price = (min(price, lowest_price) or lowest_price) if lowest_price else price

                discount = 1.0 * price / listprice if listprice else 0
                lowest_discount = max(discount, highest_discount)
                highest_discount = min(discount, lowest_discount) or discount

                # soldout
                if soldout and ((hasattr(product, 'soldout') and not product.soldout) \
                    or (product.scarcity and int(product.scarcity))):
                        soldout = False

                product.save()
                counter += 1
            #except Exception, e:
            #    txtlogger.error('{0}.{1} product propagation exception'.format(self.site, product.key))

        if not counter:
            return self.event.propagation_complete

        self.event.favbuy_brand = list(event_brands)
        self.event.brand_complete = True
        
        self.event.favbuy_tag = list(tags)
        self.event.favbuy_dept = depts.keys()[0]
        self.event.lowest_price = str(lowest_price)
        self.event.highest_price = str(highest_price)
        self.event.lowest_discount = str(1.0 - lowest_discount)
        self.event.highest_discount = str(1.0 - highest_discount)
        self.event.events_begin = self.event.events_begin or events_begin
        self.event.events_end = self.event.events_end or events_end
        self.event.soldout = soldout
        self.event.propagation_complete = True
        self.event.propagation_time = datetime.utcnow()
        self.event.save()

        return self.event.propagation_complete


def test_image():
    conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    urls = [
        'http://3.icdn.ideeli.net/attachments/147066986/430115381280-1_grid_image_zoom_largegrid_image_zoom_large900x1275.jpg',
        'http://1.icdn.ideeli.net/attachments/147067318/430115381280-2_grid_image_zoom_largegrid_image_zoom_large900x1275.jpg',
        'http://cdn03.mbbimg.cn/1307/13070129/01/480/01.jpg',
        'http://cdn08.mbbimg.cn/1310/13100015/03/480/02.jpg',
    ]

    it = ImageTool(connection = conn)
    it.crawl(urls[0:2], 'venteprivee', 'event', 'abc123457', thumb=True)
    print 'image path ---> {0}'.format(it.image_path)
    print 'complete ---> {0}\n'.format(it.image_complete)

    it = ImageTool(connection = conn)
    it.crawl(urls[2:], 'venteprivee', 'product', '123456790', thumb=True)
    print 'image path ---> {0}'.format(it.image_path)
    print 'complete ---> {0}\n'.format(it.image_complete)

def test_propagate(site='venteprivee', event_id=None):
    import time
    from mongoengine import Q
    from backends.matching.extractor import Extractor
    from backends.matching.classifier import SklearnClassifier
    extractor = Extractor()
    classifier = SklearnClassifier()
    classifier.load_from_database()
    
    m = __import__('crawlers.{0}.models'.format(site), fromlist=['Event', 'Product'])
    start = time.time()

    if event_id:
        p = Propagator(site, event_id, extractor, classifier, module=m)
        p.propagate()
    else:
        now = datetime.utcnow()
        events = m.Event.objects(Q(propagation_complete = False) & (Q(events_begin__lte=now) | Q(events_begin__exists=False)) & (Q(events_end__gt=now) | Q(events_end__exists=False)) )
        counter = len(events)
        for event in events:
            print '\n', counter, ' left.'
            p = Propagator(site, event.event_id, extractor, classifier, module=m)
            p.propagate()

            counter -= 1

    print 'cost ', time.time() - start, ' s'

if __name__ == '__main__':
    import time, sys
    start = time.time()
    if len(sys.argv) > 1:
        if sys.argv[1] == '-i':
            test_image()
        elif sys.argv[1] == '-p':
            f = test_propagate
            event_id = sys.argv[3] if len(sys.argv)>3 else None
            f(sys.argv[2], event_id)
    print time.time() - start, 's'
