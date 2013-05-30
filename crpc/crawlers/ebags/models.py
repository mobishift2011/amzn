#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from mongoengine import *
from settings import MONGODB_HOST
DB = 'ebags'
connect(db=DB, alias=DB, host=MONGODB_HOST)

from crawlers.common.models import BaseCategory, LuxuryProduct

class Category(BaseCategory):
    key = StringField(unique=True)

    meta = {
        'db_alias': DB,
    }

    def url(self):
        return self.combine_url

class Product(LuxuryProduct):
    discount = FloatField()

    meta = {
        'db_alias': DB,
    }

    def url(self):
        return self.combine_url
