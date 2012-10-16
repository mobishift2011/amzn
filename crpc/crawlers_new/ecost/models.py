#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from mongoengine import *
from datetime import datetime, timedelta

class Category(Document):
    cats = ListField(StringField())
    catstr = StringField(primary_key=True)
    leaf = BooleanField(default=False)
    update_time = DateTimeField(default=datetime.utcnow)
    spout_time = DateTimeField()
    catname = StringField()
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
    ecost = StringField(primary_key=True)
    ecost_str = StringField()
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
    comments = ListField()
    catstrs = ListField(StringField())
    meta = {
        "indexes": ["updated"]
    }

    def url(self):
        return 'http://www.ecost.com/p/{0}~pdp.{1}'.format(self.ecost, self.ecost_str)
