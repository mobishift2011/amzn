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

class Event(BaseEvent):
    event_id = StringField(unique=True)
    img_url  = StringField()
    meta = {
        "indexes": ["soldout"],
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.ruelala.com/event/%s' %self.event_id

    def img_url(self):
        return 'http://www.ruelala.com/images/content/events/%s_doormini.jpg' %self.event_id

class Product(BaseProduct):
    url = StringField()
    limit= StringField()

    meta = {
        "indexes": ["updated"],
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.ruelala.com/event/product/%s/%s/1/DEFAULT' %(self.event_id,self.key)
