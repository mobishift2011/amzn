#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawlers.ecost.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for ecost
"""
DB = 'ecost'
ITEM_PER_PAGE = 25

from datetime import datetime, timedelta
from settings import MONGODB_HOST
from mongoengine import *
connect(db=DB, host=MONGODB_HOST)

from crawlers.common.models import BaseCategory, BaseProduct

class Category(BaseCategory):
    """.. :py:class:: Category
    """
    cat_str = StringField(primary_key=True)
    link = StringField()
    meta = {
        "indexes": ["leaf", "catn"],
    }


class Product(BaseProduct):
    """.. :py:class:: Product
    """
#    ecost = StringField(primary_key=True)
    ecost_str = StringField()
    platform = StringField()
    manufacturer = StringField()
    upc = StringField()
    specifications = DictField()
    special_page = BooleanField()
#    description = StringField()
#    also_like = ListField()
    meta = {
        "indexes": ["updated"]
    }

    def url(self):
        return 'http://www.ecost.com/p/{0}~pdp.{1}'.format(self.key, self.ecost_str)
