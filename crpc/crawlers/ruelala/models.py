# -*- coding: utf-8 -*-
"""
crawlers.ruelala.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for ruelala
"""

DB = 'ruelala'
TIMEOUT = 60
from mongoengine import *
from mongoengine import connect
from settings import MONGODB_HOST
connect(db=DB, alias=DB, host=MONGODB_HOST)

from crawlers.common.models import BaseEvent, BaseProduct

class Event(BaseEvent):
    sale_id = StringField(unique=True)
    category_name = StringField()
    meta = {
        "indexes": ["soldout"],
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.ruelala.com/event/%s' %self.sale_id

    def img_url(self):
        return 'http://www.ruelala.com/images/content/events/%s_doormini.jpg' %self.sale_id

class Product(BaseProduct):
    sale_id = StringField()
    fall_name = StringField()
    url = StringField()
    scarcity = StringField()
    listprice = StringField()
    list_info = ListField(StringField())
    sizes = ListField(StringField())
    soldout_sizes = ListField(StringField())
    end_time = DateTimeField()
    sold_out = BooleanField()

    meta = {
        "indexes": ["updated"],
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.ruelala.com/event/%s/product/%s/1/DEFAULT' %(self.sale_id,self.key)
