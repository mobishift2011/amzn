#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawlers.hautelook.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for hautelook
"""

from datetime import datetime, timedelta
from crawlers.common.models import BaseEvent, LuxuryProduct

from mongoengine import *
from settings import MONGODB_HOST
DB = 'hautelook'
connect(db=DB, alias=DB, host=MONGODB_HOST)

class Event(BaseEvent):
    event_id = StringField(unique=True)
    sort_order  = StringField()
    tagline     = StringField()

    meta = {
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.hautelook.com/v3/catalog/{0}/availability'.format(self.event_id)


class Product(LuxuryProduct):
    color = StringField()
    scarcity = StringField()

    meta = {
        "indexes": ["updated"],
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.hautelook.com/v2/product/{0}'.format(self.key)
