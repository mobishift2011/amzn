#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawlers.ecost.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for ecost
"""
DB = 'ecost'

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
    shipping = StringField()
    available = StringField()
    sell_rank = IntField()
    description = StringField()
    also_like = ListField()
    catstrs = ListField(StringField())
    meta = {
        "indexes": ["updated"]
    }

    def url(self):
        return 'http://www.ecost.com/p/{0}~pdp.{1}'.format(self.key, self.ecost_str)
