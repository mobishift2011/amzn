#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawlers.myhabit.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for myhabit 
"""

from crawlers.common.models import BaseEvent, LuxuryProduct

from mongoengine import *
from settings import MONGODB_HOST
DB = 'myhabit'
connect(db=DB, alias='myhabit', host=MONGODB_HOST)

class Event(BaseEvent):
    """ override them everytime
        save asin information of this asin's product detail page;
                { u'B009HNGTG0': {u'url': u'11ZzxfXapAL.js'}, u'B009HWDRZ2': {u'url': u'11mSwRff8OL.js'} }
        save casin information for listing page update soldout;
                { u'B009HNGTG0': {u'soldOut': 1,    u'soldOutAt': {u'offset': -480, u'time': 1354234710000}} }
    """
#    upcoming_title_img = ListField()
    brand_link = StringField()
    listing_url = StringField() # http://g-ecx.images-amazon.com/images/I/41iZSE3DlGL.js

    asin_detail_page = DictField()
    casin_soldout_info = DictField()

    meta = {
        "db_alias": DB,
    }

    def url(self):
        return self.listing_url
        # return 'http://www.myhabit.com/homepage#page=b&sale={0}'.format(self.event_id)


class Product(LuxuryProduct):
#    key = StringField(unique=True, spare=True)
    asin = StringField()
    jslink = StringField() # indicates the url where we can make an "API call" to

    video = StringField()
    international_shipping = StringField()

    meta = {
        "db_alias": DB,
    }

    def url(self):
        return self.jslink
        # return 'http://www.myhabit.com/homepage#page=d&sale={0}&asin={1}&cAsin={2}'.format(self.event_id[0], self.asin, self.key)
