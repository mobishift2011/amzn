# -*- coding: utf-8 -*-
"""
crawlers.ruelala.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for ruelala
"""

DB = 'ruelala_test1'
TIMEOUT = 60
from mongoengine import *
from mongoengine import connect
from settings import MONGODB_HOST
connect(db=DB, alias=DB, host=MONGODB_HOST)

from crawlers.common.models import BaseEvent, BaseProduct

class Category(BaseEvent):
    sale_id = StringField(unique=True)
    category_name = StringField()
    img_url  = StringField()
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
    url = StringField()
    limit= StringField()

    meta = {
        "indexes": ["updated"],
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.ruelala.com/event/product/%s/%s/1/DEFAULT' %(self.sale_id,self.key)
