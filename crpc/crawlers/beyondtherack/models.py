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
        pass

class Product(LuxuryProduct):
    meta    =   { "db_alias": DB, }

    def url(self):
        pass
