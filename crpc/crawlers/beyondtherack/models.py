#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawlers.beyondtherack.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Event Model for beyondtherack 
"""


from mongoengine import *
from settings import MONGODB_HOST
DB = "beyondtherack"
connect(db=DB, alias=DB, host=MONGODB_HOST)

from crawlers.common.models import BaseEvent, LuxuryProduct

class Event(BaseEvent):
    meta    =   { "db_alias": DB, }

    def url(self):
        return 'http://www.beyondtherack.com/event/showcase/{0}'.format(self.event_id)

class Product(LuxuryProduct):
    meta    =   { "db_alias": DB, }

    def url(self):
        return self.combine_url
        # return 'http://www.beyondtherack.com/event/sku/{0}/{1}'.format(self.event_id[0], self.key)
