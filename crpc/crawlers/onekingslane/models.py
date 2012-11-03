#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawlers.zulily.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for zulily 
"""

from datetime import datetime, timedelta
from crawlers.common.models import BaseEvent, LuxuryProduct

from mongoengine import *
from settings import MONGODB_HOST
DB = 'zulily'
connect(db=DB, alias='zulily', host=MONGODB_HOST)

class Event(BaseEvent):
    event_id = StringField(unique=True)
    short_desc = StringField()
    start_end_date = StringField()

    meta = {
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.zulily.com/e/{0}.html'.format(self.event_id)


class Product(LuxuryProduct):
    also_like = ListField()

    meta = {
        "indexes": ["updated"],
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.zulily.com/p/{0}.html'.format(self.key)
