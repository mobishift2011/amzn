#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawlers.onekingslane.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for onekingslane 
"""

from datetime import datetime, timedelta
from crawlers.common.models import BaseCategory, BaseEvent, LuxuryProduct

from mongoengine import *
from settings import MONGODB_HOST
DB = 'onekingslane'
connect(db=DB, alias=DB, host=MONGODB_HOST)

class Category(BaseCategory):
    key = StringField(unique=True)

    meta = {
        "db_alias": DB,
    }

    def url(self):
        """ vintage-market-finds/category_name """
        return 'https://www.onekingslane.com/vintage-market-finds/{0}'.format(self.key)

class Event(BaseEvent):
    """
        difference: event_id is in the url, replaced the space with '+', and dept is in the text_content
    """
    short_desc = StringField()

    meta = {
        "db_alias": DB,
    }

    def url(self):
        """ sales/event_id
            self.event_id.isdigit()
        """
        return 'https://www.onekingslane.com/sales/{0}'.format(self.event_id)


class Product(LuxuryProduct):
    short_desc = StringField()
    condition = StringField()
    era = StringField()
    seller = StringField()

    meta = {
        "db_alias": DB,
    }

    def url(self):
        """
            product/event_id/product_id
            vintage-market-finds/product/770075
        """
        return self.combine_url
