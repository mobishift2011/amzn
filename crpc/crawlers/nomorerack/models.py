#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.bluefly.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for Amazon
"""
DB = 'nomorerack'
from settings import MONGODB_HOST
from mongoengine import *
connect(db=DB, alias=DB, host=MONGODB_HOST)
from crawlers.common.models import BaseCategory, BaseProduct,BaseReview,LuxuryProduct,BaseEvent

class Event(BaseEvent):
    event_id = StringField(unique=True)
    meta        =   {
        "db_alias": DB,
    }

    def url(self):
        return 'http://nomorerack.com/events/view/%s' %self.event_id[0]

class Product(LuxuryProduct):
    event_id = StringField()
    dept = StringField()
    listprice = StringField()
    return_policy  = StringField()
    color = StringField()
    end_time = DateTimeField()

    def url(self):
        return 'http://nomorerack.com/daily_deals/view/%d-product' %self.key

    meta                =   {
        "db_alias": DB,
    }

