# -*- coding: utf-8 -*-
"""
crawlers.ruelala.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for ruelala
"""

from crawlers.common.models import BaseEvent, LuxuryProduct

from mongoengine import *
from settings import MONGODB_HOST
DB = 'ruelala'
connect(db=DB, alias=DB, host=MONGODB_HOST, connecttimeoutms=1e10)


class Event(BaseEvent):

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
        return 'http://www.ruelala.com/event/product/{0}/{1}/1/DEFAULT'.format(self.event_id[0], self.key)
