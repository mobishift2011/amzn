#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawlers.common.imageprocess
~~~~~~~~~~~~~~~~~~~

This is the image process library to download image url from website, then save the image to amazon s3.
We can cut image later in this library.

"""

import os
import time
import boto
import boto.s3.key
import boto.s3.connection
import requests
from StringIO import StringIO
from stash import *

AWS_ACCESS_KEY = "AKIAIQC5UD4UWIJTBB2A"
AWS_SECRET_KEY = "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"
IMAGE_S3_BUCKET = 'favbuy'
IMAGE_ROOT = ''
URL_EXPIRES_IN = 60 * 60 * 24 * 365 * 25    # S3 has an epoch time of 03:14 UTC on Tuesday, 19 January 2038.

@singleton
class ImageToS3(object):
    """.. :py:class:: ImageToS3
    
    Download the images from website urls, then save the images to amazon s3.
    The url of images in s3 save to our DB.

    """

    def __init__(self, s3conn=None, bucket_name=IMAGE_S3_BUCKET):
        self.s3_connection = s3conn or boto.s3.connection.S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
        try:
            bucket = self.s3_connection.get_bucket(bucket_name)
        except boto.exception.S3ResponseError, e:
            if str(e).find('404 Not Found'):
                bucket = self.s3_connection.create_bucket(bucket_name)
            else:
                raise
        self.s3_key = boto.s3.key.Key(bucket)


    def download_images(self, image_urls, site, doctype, obj_id):
        """.. :py:method::

        :param image_urls: the image urls of that site
        :param site: site for crawler to crawl
        :param dectype: `category` or `event` or `product` 
        :param obj_id: event_id or product_id
        """
        image_path = []
        image_urls = [image_urls] if not isinstance(image_urls, list) else image_urls
        for image_url in image_urls:
            ret_content = fetch_page(image_url)
            if ret_content is None:
                image_path.append('')
            else:
                upload_key = '{0}_{1}_{2}_{3}_{4}'.format(site, doctype, int(time.time()), obj_id, image_url.rsplit('/', 1)[-1])
                s3_url = self.upload_to_s3(StringIO(ret_content), upload_key)
                image_path.append(s3_url)
        return image_path

    def upload_to_s3(self, image_hex, upload_key):
        """.. :py:method::

            upload image string stream to unique address in amazon s3
        :param image_hex: the image in StringIO stream
        :param upload_key: unique key of this image in amazon s3
        """
        self.s3_key.key = upload_key
        self.s3_key.set_contents_from_file(image_hex)
        return self.s3_key.generate_url(URL_EXPIRES_IN)


@singleton 
class ImageCut(object):
    def __init__(self):
        pass

def process_image(image_urls, site, doctype, obj_id):
    """.. :py:method::

        Download the images that crawlers crawled, upload them to s3.
        Cutting images and other process
    :param image_urls: the image urls of that site
    :param site: site for crawler to crawl
    :param dectype: `category` or `event` or `product` 
    :param obj_id: event_id or product_id
    """
    image_to_s3 = ImageToS3()
    image_to_cut = ImageCut()
    s3_path = image_to_s3.download_images(image_urls, site, doctype, obj_id)

    # add image cut code here maybe
    return s3_path
