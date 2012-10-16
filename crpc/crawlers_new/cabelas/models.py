#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from mongoengine import *
from datetime import datetime, timedelta

class Category(Document):
    cats = ListField(StringField())
    leaf = BooleanField(default=False)
    update_time = DateTimeField(default=datetime.utcnow)
    spout_time = DateTimeField()
    catname = StringField()
    catn = IntField(unique=True)
    num = IntField()
    meta = {
        "indexes": ["leaf"],
    }

    def catstr(self):
        return ' > '.join(self.cats)

    def url(self, page_item_NO):
        if self.catname:
            if page_item_NO:
                return 'http://www.cabelas.com/catalog/browse/{0}/_/N-{1}/No-{2}'.format(self.catname, self.catn, page_item_NO)
            return 'http://www.cabelas.com/catalog/browse/{0}/_/N-{1}/'.format(self.catname, self.catn)
        return 'http://www.cabelas.com/catalog/browse/_/N-{0}'.format(self.catn)


class Product(Document):
    itemID = StringField(primary_key=True)
    itemNO = StringField()
    list_update_time = DateTimeField(default=datetime.utcnow)
    full_update_time = DateTimeField()
    title = StringField()
    image = StringField()
    description = StringField()
    shipping = StringField()
    available = StringField()
    price = StringField()
    rating = FloatField()
    reviews = IntField()
    sell_rank = IntField()
    updated = BooleanField()
    also_like = ListField()
    catstrs = ListField(StringField())
    model = ListField(StringField())
    comments = ListField()
    meta = {
        "indexes": ["updated"]
    }

    def url(self):
        return 'http://www.cabelas.com/product/{0}.uts'.format(self.itemID)
