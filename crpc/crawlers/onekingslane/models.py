#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawlers.onekingslane.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for onekingslane 
"""

from datetime import datetime, timedelta
from crawlers.common.models import BaseEvent, LuxuryProduct

from mongoengine import *
from settings import MONGODB_HOST
DB = 'onekingslane'
connect(db=DB, alias='onekingslane', host=MONGODB_HOST)

class Event(BaseEvent):
    event_id = StringField(unique=True)
    short_desc = StringField()

    meta = {
        "db_alias": DB,
    }

    def url(self):
        return 'https://www.onekingslane.com/sales/{0}'.format(self.event_id)


class Product(LuxuryProduct):
    also_like = ListField()

    meta = {
        "indexes": ["updated"],
        "db_alias": DB,
    }

    def url(self):
        return 'https://www.onekingslane.com/product/{0}/{1}'.format(self.event_id[0], self.key)
