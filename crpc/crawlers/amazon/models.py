#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.amazon.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for Amazon
"""
from settings import MONGODB_HOST

from mongoengine import *
connect(db="amazon", host=MONGODB_HOST)

import re
from urllib import quote, unquote
from datetime import datetime, timedelta

from crawlers.common.models import Category, Product

def catn2url(catn): 
    return 'http://www.amazon.com/s?ie=UTF8&rh=' + quote(catn.encode("utf-8"))

def url2catn(url): 
    m = re.compile(r'(n%3A.*?)&').search(url)
    if not m:
        m = re.compile(r'(n%3A.*)').search(url)
        if not m:
            return ''
    catn = unquote(m.group(1)).decode('utf-8')
    catn = [x for x in catn.split(',') if x.startswith('n:')][-1]
    return catn

class Category(Category):
    """ we generates category by catn identifier """
    catn        =   StringField(unique=True)

    def url(self):
        return catn2url(self.catn)

class Product(Product):
    catns               =   ListField(StringField())
    sales_rank          =   StringField()
    vartitle            =   StringField()

    def url(self):
        return "http://www.amazon.com/{slug}/dp/{asin}/".format(slug=self.slug, asin=self.asin)

