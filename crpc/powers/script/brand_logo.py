#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import env
from admin.models import Brand
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from PIL import Image, ImageChops
from cStringIO import StringIO
from datetime import datetime, timedelta
from hashlib import md5

import boto
import requests
import json
import os, sys
import urllib
import time
import traceback

reload(sys)
sys.setdefaultencoding('utf8')

__AWS_ACCESS_KEY      =   'AKIAIQC5UD4UWIJTBB2A'
__AWS_SECRET_KEY      =   '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'
S3_IMAGE_BUCKET     =   'favbuy-logo' if env == 'PRODUCTION' else 'favbuy-logo-test'
S3_IMAGE_URL           =   'https://s3.amazonaws.com/{bucket}'.format(bucket=S3_IMAGE_BUCKET)

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

s3conn = None
BUCKET = None
ROOT_DIR = None
no_match = []

print u'Begin connecting to the s3...'

s3conn = S3Connection(__AWS_ACCESS_KEY, __AWS_SECRET_KEY)
try:
    BUCKET = s3conn.get_bucket(S3_IMAGE_BUCKET)
    print u'S3 bucket {} inited!'.format(BUCKET)
except boto.exception.S3ResponseError, e:
    if '404' in repr(e):
        BUCKET = s3conn.create_bucket(S3_IMAGE_BUCKET)
        BUCKET.set_policy(json.dumps(policy))
    else:
        s3conn = None
        BUCKET = None
        raise

class Imager():
    def __init__(self):
        self.bk = None

    @property
    def bucket_key(self):
        if self.bk is None:
            self.bk = Key(BUCKET)
        return self.bk

    def upload2s3(self, image, key):
        """ upload image to s3 in key 

        :param image: fileobj for an image
        :param key: s3 key name

        Returns None
        """
        print u'uploading {0}'.format(key)
        self.bucket_key.key = key
        self.bucket_key.set_contents_from_file(image, headers={'Content-Type':'image/jpeg', 'Cache-Control':'max-age=31536000, public'})

    def save(self, filepath):
        name, appendix = os.path.splitext(filepath)
        key = self.bucket_key
        key.key = name
        abspath = ROOT_DIR + '/' + filepath

        with open(abspath) as f:
            if not key.exists():
                self.upload2s3(f, key.key)
        
        return '{0}/{1}'.format(S3_IMAGE_URL, key.key)


def upload(filepath):
    name, appendix = os.path.splitext(filepath)
    print name, appendix

    brand = Brand.objects(title_edit=name, is_delete=False).first()
    if not brand:
        brand = Brand.objects(title=name, is_delete=False).first()

    if not brand:
        no_match.append(name)
        return

    imager = Imager()
    url = imager.save(filepath)

    if url:
        brand.icon = url
        brand.save()
        print brand.icon


if __name__ == '__main__':
    from optparse import OptionParser

    global ROOT_DIR
    parser = OptionParser(usage='usage: %prog [options]')
    parser.add_option('-d', dest='directory_path', help="Image directory path.", default='')
    parser.add_option('-f', dest='file_path', help="Image file path.", default='')

    options, args = parser.parse_args(sys.argv[1:])
    if len(sys.argv) == 1:
        parser.print_help()

    if options.directory_path:
        ROOT_DIR = options.directory_path
        for filepath in os.listdir(ROOT_DIR):
            upload(filepath)

    elif options.file_path:
        upload(options.file_path)

    print 'no matches: ', no_match
