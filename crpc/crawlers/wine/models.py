#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ethan <ethan@favbuy.com>
"""
crawlers.wine.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product for wine
"""

from mongoengine import *
from settings import MONGODB_HOST
DB = 'wine'
connect(db=DB, alias=DB, host=MONGODB_HOST)

from crawlers.common.models import LuxuryProduct


class Product(LuxuryProduct):
    deal_type = True
    hit_time = DateTimeField()
    
    meta = {
        "db_alias": DB,
    }
    
    def url(self):
        return self.combine_url
