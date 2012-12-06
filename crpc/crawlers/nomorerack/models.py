#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.nomorerack.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for Amazon
"""

from crawlers.common.models import BaseCategory, BaseProduct, BaseReview, LuxuryProduct, BaseEvent

from mongoengine import *
from settings import MONGODB_HOST
DB = 'nomorerack'
connect(db=DB, alias=DB, host=MONGODB_HOST, connecttimeoutms=1e10)

class Category(BaseCategory):
    key = StringField(unique=True)

    meta = { 
        "db_alias": DB, 
    }

    def url(self):
        if self.key == '#':
            return 'http://nomorerack.com'
        return 'http://nomorerack.com/daily_deals/category/{0}'.format(self.key)


class Event(BaseEvent):

    meta = { 
        "db_alias": DB, 
    }

    def url(self):
        return 'http://nomorerack.com/events/view/{0}'.format(self.event_id)

class Product(LuxuryProduct):
    color = StringField()

    def url(self):
        return 'http://nomorerack.com/daily_deals/view/{0}'.format(self.key)

    meta = { 
        "db_alias": DB, 
    }

