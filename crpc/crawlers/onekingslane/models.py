#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawlers.onekingslane.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for onekingslane 
"""

from datetime import datetime, timedelta
from crawlers.common.models import BaseEvent, LuxuryProduct

from mongoengine import *
from settings import MONGODB_HOST
DB = 'onekingslane'
connect(db=DB, alias='onekingslane', host=MONGODB_HOST)

class Event(BaseEvent):
    """
        difference: event_id is in the url, replaced the space with '+', and dept is in the text_content
    """
    event_id = StringField(unique=True)
    short_desc = StringField()

    meta = {
        "db_alias": DB,
    }

    def url(self):
        """
            self.event_id:
                sales/event_id
                vintage-market-finds/category_name
        """
        if self.event_id.isdigit():
            return 'https://www.onekingslane.com/sales/{0}'.format(self.event_id)
        else:
            return 'https://www.onekingslane.com/vintage-market-finds/{0}'.format(self.event_id)


class Product(LuxuryProduct):
    short_desc = StringField()
    products_end = DateTimeField()
    condition = StringField()
    era = StringField()
    seller = StringField()

    meta = {
        "indexes": ["updated"],
        "db_alias": DB,
    }

    def url(self):
        """
            product/event_id/product_id
            vintage-market-finds/product/770075
        """
        if self.short_desc: # or we can use sell_rank to differentiate.
            return 'https://www.onekingslane.com/vintage-market-finds/product/{0}'.format(self.key)
        else:
            return 'https://www.onekingslane.com/product/{0}/{1}'.format(self.event_id[0], self.key)
