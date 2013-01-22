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
    tagline     = ListField(StringField(), default=list)

    meta = {
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.hautelook.com/v3/catalog/{0}/availability'.format(self.event_id)


class Product(LuxuryProduct):
    additional_info = ListField(StringField())
    care_info = StringField()
    fiber = StringField()
    arrives = StringField()

    delivery_date = StringField()
    choke_hazard = StringField()

    meta = {
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.hautelook.com/v2/product/{0}'.format(self.key)
