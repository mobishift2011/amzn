#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.amazon.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for Amazon
"""
DB = 'bluefly'
from settings import MONGODB_HOST
from mongoengine import *
connect(db=DB, alias=DB, host=MONGODB_HOST)
from crawlers.common.models import BaseCategory, BaseProduct

class Category(BaseCategory):
    """ we generates category by catn identifier """
    key =   StringField(unique=True)
    name = StringField()
    url = StringField()

    def url(self):
        return self.url
    
    meta        =   {
        "db_alias": DB,
    }

class Product(BaseProduct):
    catns               =   ListField(StringField())
    sales_rank          =   StringField()
    vartitle            =   StringField()

    def url(self):
        return "http://www.amazon.com/{slug}/dp/{key}/".format(slug=self.slug, key=self.key)

    meta                =   {
        "db_alias": "amazon",
    }
