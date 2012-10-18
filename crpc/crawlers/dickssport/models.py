#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawlers.dickssport.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for dickssport 
"""

DB = "dickssport"
TIMEOUT = 60

from mongoengine import *
from datetime import datetime, timedelta
from settings import MONGODB_HOST
from mongoengine import *
connect(db=DB, host=MONGODB_HOST)

from crawlers.common.models import BaseCategory, BaseProduct

class Category(BaseCategory):
    """.. :py:class:: Category
    """
    catname = StringField()
    catn = IntField(unique=True)
    meta = {
        "indexes": ["catn"],
    }

    def url(self):
        if self.is_leaf:
            return 'http://www.dickssportinggoods.com/family/index.jsp?categoryId={0}'.format(self.catn)
        return 'http://www.dickssportinggoods.com/category/index.jsp?categoryId={0}'.format(self.catn)


class Product(BaseProduct):
    """.. :py:class:: Category
    """
#    itemNO = StringField(primary_key=True)
    also_like = ListField()
    comment = ListField()
    meta = {
        "indexes": ["updated"]
    }

    def url(self):
        return 'http://www.dickssportinggoods.com/product/index.jsp?productId={0}'.format(self.key)
