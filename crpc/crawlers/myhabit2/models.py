#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from mongoengine import *
from datetime import datetime, timedelta

class Brand(Document):
    dept = StringField()
    brand_name = StringField()
    brand_link = StringField()
    brand_info = StringField()

    leaf = BooleanField(default=False)
    update_time = DateTimeField(default=datetime.utcnow)
    spout_time = DateTimeField()
    catn = IntField(unique=True)
    num = IntField()
    meta = {
        "indexes": ["leaf", "catn"],
    }

    def url(self):
        if self.leaf:
            return 'http://www.dickssportinggoods.com/family/index.jsp?categoryId={0}'.format(self.catn)
        return 'http://www.dickssportinggoods.com/category/index.jsp?categoryId={0}'.format(self.catn)


class Product(Document):
    itemNO = StringField(primary_key=True)
    list_update_time = DateTimeField(default=datetime.utcnow)
    full_update_time = DateTimeField()
    title = StringField()
    image = StringField()
    price = StringField()
    shipping = StringField()
    available = StringField()
    rating = FloatField()
    reviews = IntField()
    sell_rank = IntField()
    description = StringField()
    model = StringField()
    updated = BooleanField()
    also_like = ListField()
    comment = ListField()
    catstrs = ListField(StringField())
    meta = {
        "indexes": ["updated"]
    }

    def url(self):
        return 'http://www.dickssportinggoods.com/product/index.jsp?productId={0}'.format(self.itemNO)
