#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawlers.ideeli.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Event Model for ideeli
"""

from mongoengine import *
from settings import MONGODB_HOST
DB = 'ideeli'
connect(db=DB, alias=DB, host=MONGODB_HOST)

from crawlers.common.models import BaseEvent, LuxuryProduct

class Event(BaseEvent):
    meta = { "db_alias": DB, }

    def url(self):
        return 'http://www.ideeli.com/events/{0}/latest_view_colors?force_cache_write=1'.format(self.event_id)

class Product(LuxuryProduct):
    offer_id = IntField()

    meta = { "db_alias": DB, }

    def url(self):
        return self.combine_url
        # return 'http://www.ideeli.com/events/{0}/offers/{1}/latest_view/{2}'.format(self.event_id[0], self.offer_id, self.key)
