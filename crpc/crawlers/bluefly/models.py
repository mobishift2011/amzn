#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.bluefly.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for Amazon
"""
DB = 'bluefly'
from settings import MONGODB_HOST
from mongoengine import *
connect(db=DB, alias=DB, host=MONGODB_HOST)
from crawlers.common.models import BaseCategory, BaseProduct, BaseReview, LuxuryProduct

class Category(BaseCategory):
    """ we generates category by catn identifier
    """
    key   =     StringField(unique=True)

    meta  =     {
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.bluefly.com/_/N-{0}/list.fly'.format(self.key)


class Product(LuxuryProduct):
    return_policy  = StringField()
    color = StringField()


    meta  =   {
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.bluefly.com/{0}/p/{1}/detail.fly'.format(self.slug, self.key)


class  Review(BaseReview):
    product_key = StringField()
    meta  =   {
        "db_alias": DB,
    }
