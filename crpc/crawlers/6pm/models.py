#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ethan <ethan@favbuy.com>
"""
crawlers.6pm.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product for 6pm
"""

from mongoengine import *
from settings import MONGODB_HOST
DB = '6pm'
connect(db=DB, alias=DB, host=MONGODB_HOST)

from crawlers.common.models import LuxuryProduct

class Product(LuxuryProduct):
    deal_type = True
    
    meta = {
        "db_alias": DB,
    }
    
    def url(self):
        return self.combine_url
