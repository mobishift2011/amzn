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

from crawlers.common.models import BaseCategory, BaseProduct

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

ROOT_CATN = {
    'Electronics':              'n:172282',
    'Appliances':               'n:2619525011',
    'Patio, Lawn & Garden':     'n:2972638011',
    'Tools & Home Improvement': 'n:228013',
    'Health & Personal Care':   'n:3760901',
    'Sports & Outdoors':        'n:3375251',
    'Video Games':              'n:468642',
    'Toys & Games':             'n:165793011',
}

class Category(BaseCategory):
    """ we generates category by catn identifier """
    catn        =   StringField(unique=True)

    def url(self):
        return catn2url(self.catn)+'&page={0}'

class Product(BaseProduct):
    catns               =   ListField(StringField())
    sales_rank          =   StringField()
    vartitle            =   StringField()

    def url(self):
        return "http://www.amazon.com/{slug}/dp/{key}/".format(slug=self.slug, key=self.key)
