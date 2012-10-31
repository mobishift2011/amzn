#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawlers.myhabit.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for myhabit 
"""

from datetime import datetime, timedelta
from crawlers.common.models import BaseEvent, LuxuryProduct

from mongoengine import *
from settings import MONGODB_HOST
DB = 'myhabit'
connect(db=DB, alias='myhabit', host=MONGODB_HOST)

class Event(BaseEvent):
    is_leaf = BooleanField(default=True)
    sale_id = StringField(unique=True)
    dept = ListField(StringField())
    brand_link = StringField()
    upcoming_title_img = ListField()

    meta = {
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.myhabit.com/homepage#page=b&dept={0}&sale={1}'.format(self.dept, self.sale_id)


class Product(LuxuryProduct):
#    key = StringField(unique=True, spare=True)
    asin = StringField()

    color = StringField()
    video = StringField()
    international_shipping = StringField()
    sizes = ListField(StringField())
    scarcity = StringField()

    meta = {
        "indexes": ["updated"],
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.myhabit.com/homepage#page=d&sale={0}&asin={1}&cAsin={2}'.format(self.sale_id[0], self.asin, self.key)
