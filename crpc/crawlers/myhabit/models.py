#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawlers.myhabit.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for myhabit 
"""

from datetime import datetime, timedelta
from crawlers.common.models import BaseEvent, BaseProduct
from mongoengine import *


class Category(BaseEvent):
    sale_id = StringField(unique=True)
    dept = ListField(StringField())
    upcoming_title_img = ListField()

    def url(self):
        return 'http://www.myhabit.com/homepage#page=b&dept={0}&sale={1}'.format(self.dept, self.sale_id)


class Product(BaseProduct):
#    key = StringField(unique=True, spare=True)
    sale_id = StringField()
    asin = StringField()
    listprice = StringField()
    soldout = BooleanField()

    list_info = ListField(StringField())
    color = StringField()
    sizes = ListField(StringField())

    video = StringField()
    international_shipping = StringField()
    returned = StringField()
    scarcity = StringField()

    meta = {
        "indexes": ["updated"]
    }

    def url(self):
        return 'http://www.myhabit.com/homepage#page=d&dept={0}&sale={1}&asin={2}&cAsin={3}'.format(self.dept, self.sale_id, self.asin, self.key)
