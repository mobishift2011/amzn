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

from configs import *

import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection

from hashlib import md5
import os
import re
import requests
import urllib
from PIL import Image
from StringIO import StringIO
from datetime import datetime

from helpers.log import getlogger
txtlogger = getlogger('powertools', filename='/tmp/textserver.log')
imglogger = getlogger('powertools', filename='/tmp/powerserver.log')

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
    def __init__(self, connection=None, bucket_name=S3_IMAGE_BUCKET):
        self.__s3conn = connection
        try:
            bucket = self.__s3conn.get_bucket(bucket_name)
        except boto.exception.S3ResponseError, e:
            if str(e).find('404 Not Found'):
                bucket = self.__s3conn.create_bucket(bucket_name)
            else:
                raise
        self.__key = Key(bucket)
        self.__image_path = []
        self.__thumbnail_complete = False
        self.__image_complete = False
        # self.__pool = Pool(10)
        # self.s3_upload_lock = Semaphore(1)

    @property
    def image_complete(self):
        return self.__image_complete

    @property
    def image_path(self):
        return self.__image_path

    @property
    def thumbnails(self):
        return self.__thumbnails
  
    def crawl(self, image_urls=[], site='', doctype='', key='', thumb=False):
        print "images crawling ---> {0}.{1}.{2}\n".format(site, doctype, key)

        if len(image_urls) == 0:
            self.__image_complete = True
            return

        for image_url in image_urls:
            path, filename = os.path.split(image_url)
            index = image_urls.index(image_url)
            image_name = '%s_%s' % (index, md5(filename).hexdigest())
            # s3key= os.path.join(site, doctype, key, image_name)
            # TO backward test
            s3key= os.path.join(site, doctype, key, image_name)

            self.__key.key = s3key

            if self.__key.exists():
                image_content = None
                self.__key.make_public()
                s3_url = '{0}/{1}'.format(S3_IMAGE_URL, self.__key.key)
                print 'grab existing image from s3 ---> {0}\n'.format(s3_url)
                self.__image_path.append(s3_url)
            else:
                try:
                    image_content = self.download(image_url)
                    if not image_content:
                        continue
                except Exception, e:
                    imglogger.error('download image {0} exception'.format(image_url))
                    return
                s3_url = self.upload2s3(StringIO(image_content), self.__key.key)
                if s3_url:
                    self.__image_path.append(s3_url)
                else:
                    self.__image_complete = False
                    return

            if thumb:
                if doctype.capitalize() == 'Product' or \
                    (doctype.capitalize() == 'Event' and index == 0):
                        if not image_content:
                            image_content = self.download(s3_url)
                        self.thumbnail(doctype, StringIO(image_content), self.__key.key)

        self.__image_complete = self.__thumbnail_complete if thumb else True

    def download(self, image_url):
        print 'downloading image ---> {0}'.format(image_url)
        r = requests.get(image_url)
        if r.status_code == 403 or r.status_code == 404:
            return None
        else:
            r.raise_for_status()
        return r.content

    def upload2s3(self, image, key):
        print 'upload2s3 ---> {0}'.format(key)
        self.__key.key = key
        self.__key.set_contents_from_file(image, headers={'Content-Type':'image/jpeg'})
        self.__key.make_public()

        image_url = '{0}/{1}'.format(S3_IMAGE_URL, self.__key.key)
        print 'generate s3 image url ---> {0}\n'.format(image_url)
        return image_url

    def thumbnail(self, doctype, image, image_name):
        im = Image.open(image)
        for size in IMAGE_SIZE[doctype.capitalize()]:
            width = size.get('width')
            height = size.get('height')
            fluid = size.get('fluid')

            width_rate = 1.0 * width / im.size[0]
            height_rate = 1.0 * height / im.size[1]
            rate = max(width_rate, height_rate)

            print 'thumbnail %s to size ---> (%s, %s)' % (im.size, width, height)
            path, name = os.path.split(image_name)
            thumb_name = '%sx%s_%s' % (width, height, name)
            key = os.path.join(path, thumb_name)
            self.__key.key = key

            if self.__key.exists():
                s3_url = '{0}/{1}'.format(S3_IMAGE_URL, self.__key.key)
                print 'thumbnail already exists on s3 ---> {0}\n'.format(s3_url)
            else:      
                thumb_pict = self.resize_by_rate(rate, im) \
                        if fluid == True or width == 0 or height == 0 \
                            else self.resize_by_crop(width=width, height=height, im=im)
                self.upload2s3(thumb_pict, self.__key.key)

        self.__thumbnail_complete = True

    def resize(self, box, im):
        thumbnail = im.resize(box, Image.ANTIALIAS)
        tempfile = StringIO()
        thumbnail.save(tempfile, 'JPEG', quality=95)
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
        thumnail = im.resize( tuple( [int(i*rate) for i in im.size] ), Image.ANTIALIAS )
        left = (thumnail.size[0] - width) / 2  if (thumnail.size[0] - width) > 0 else 0
        upper = (thumnail.size[1] - height) / 2 if (thumnail.size[1] - height) > 0 else 0
        right = left + width
        lower = upper + height
        box = (left, upper, right, lower)
        region = thumnail.crop(box)

        tempfile = StringIO()
        region.save(tempfile, 'JPEG', quality=95)
        tempfile.seek(0)
        return tempfile


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
                        __import__('crawlers.{0}.models'.format(site), fromlist=['Event', 'Product'])
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
            return self.event

        event_brands = set()
        tags = set()
        depts = set()
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
                    depts = depts.union([ product.favbuy_dept[0] ])

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
                price = parse_price(product.price)
                listprice = parse_price(product.listprice) or price
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
        if self.event.dept:
            depts.add(self.classifier.classify('\n'.join(self.event.dept))[0])
        self.event.favbuy_dept = list(depts)
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
    it.crawl(urls[0:2], 'venteprivee', 'event', 'abc123', thumb=True)
    print 'image path ---> {0}'.format(it.image_path)
    print 'complete ---> {0}\n'.format(it.image_complete)

    it = ImageTool(connection = conn)
    it.crawl(urls[2:], 'venteprivee', 'product', '123456', thumb=True)
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
    pass

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
