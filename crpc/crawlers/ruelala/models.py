# -*- coding: utf-8 -*-
"""
crawlers.ruelala.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for ruelala
"""

DB = 'ruelala'
from mongoengine import *
from settings import MONGODB_HOST
connect(db=DB, alias=DB, host=MONGODB_HOST)

from crawlers.common.models import BaseEvent, BaseProduct,LuxuryProduct

class Event(BaseEvent):
    event_id = StringField(unique=True)

    meta = {
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.ruelala.com/event/{0}'.format(self.event_id)

class Product(LuxuryProduct):
    limit     = StringField()
    ship_rule = StringField()

    meta = {
        "db_alias": DB,
    }

    def url(self):
        return 'http://www.ruelala.com/event/product/%s/%s/1/DEFAULT' %(self.event_id[0],self.key)
