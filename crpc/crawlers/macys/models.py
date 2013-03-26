#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ethan <ethan@favbuy.com>
"""
crawlers.macys.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product for macys
"""

from mongoengine import *
from settings import MONGODB_HOST
DB = 'macys'
connect(db=DB, alias=DB, host=MONGODB_HOST)

from crawlers.common.models import BaseCategory, LuxuryProduct


class Category(BaseCategory):
    key = StringField(unique=True)
    combine_url = StringField()

    meta = {
        'db_alias': DB,
    }

    def url(self):
        return self.combine_url + '&viewall=true'


class Product(LuxuryProduct):
    meta = {
        "db_alias": DB,
    }
    
    def url(self):
        return self.combine_url
