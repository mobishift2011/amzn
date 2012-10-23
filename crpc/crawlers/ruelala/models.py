#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawlers.myhabit.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for myhabit 
"""

DB = 'ruelala'
TIMEOUT = 60

from datetime import datetime, timedelta
from mongoengine import *
from settings import MONGODB_HOST
connect(db=DB, host=MONGODB_HOST)

from crawlers.common.models import BaseBrand, BaseProduct

class Event(BaseBrand):
    sale_id = IntField(primary_key=True)
    category_name = StringField()
    meta = {
        "indexes": ["soldout"],
    }

    def url(self):
        return 'http://www.ruelala.com/event/%s' %self.sale_id

    def img_url(self):
        return 'http://www.ruelala.com/images/content/events/%s_doormini.jpg' %self.sale_id

class Product(BaseProduct):
    sale_id = StringField()
    fall_name = StringField()
    url = StringField()
    left = IntField()
    listprice = StringField()
    list_info = ListField(StringField())
    sizes = ListField(StringField())

    meta = {
        "indexes": ["updated"]
    }

    def url(self):
        return 'http://www.ruelala.com/event/%s/product/%s/1/DEFAULT' %(sale_id,product_id)
