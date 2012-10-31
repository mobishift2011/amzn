#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.bluefly.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for Amazon
"""
DB = 'nomorerack-test'
from settings import MONGODB_HOST
from mongoengine import *
connect(db=DB, alias=DB, host=MONGODB_HOST)
from crawlers.common.models import BaseCategory, BaseProduct,BaseReview,LuxuryProduct,BaseEvent
class Event(BaseEvent):
    sale_id = StringField(unique=True)
    meta        =   {
        "db_alias": DB,
    }

class Category(BaseCategory):
    """ we generates category by catn identifier """
    key =   StringField(unique=True)

    def url(self):
        return 'http://nomorerack.com/daily_deals/category/%s' %key
    
    meta        =   {
        "db_alias": DB,
    }

class Product(LuxuryProduct):
    sale_id = StringField()
    category_key = StringField()

    url = StringField()
    listprice = StringField()
    return_policy  = StringField()
    color = StringField()

    def url(self):
        return self.url

    meta                =   {
        "db_alias": DB,
    }

class  Review(BaseReview):
    product_key = StringField()
    meta                =   {
        "db_alias": DB,
    }
