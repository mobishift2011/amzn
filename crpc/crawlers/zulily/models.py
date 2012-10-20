#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawlers.zulily.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for zulily 
"""

from datetime import datetime, timedelta
from crawlers.common.models import BaseEvent, BaseProduct

from mongoengine import *
from settings import MONGODB_HOST
DB = 'zulily'
connect(db=DB, alias='zulily', host=MONGODB_HOST)

class Category(BaseEvent):
    lug = StringField(unique=True)
    dept = ListField(StringField())
    short_desc = StringField()
    start_end_date = StringField()
    upcoming_title_img = ListField()

    meta = {
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.zulily.com/e/{0}'.format(self.lug)


class Product(BaseProduct):
#    key = StringField(unique=True, spare=True)
    dept = StringField()
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
        "indexes": ["updated"],
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.myhabit.com/homepage#page=d&dept={0}&sale={1}&asin={2}&cAsin={3}'.format(self.dept, self.sale_id, self.asin, self.key)
