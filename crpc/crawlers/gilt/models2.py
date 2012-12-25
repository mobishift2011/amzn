#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from mongoengine import *
from settings import MONGODB_HOST
DB = 'gilt'
connect(db=DB, alias=DB, host=MONGODB_HOST)

from crawlers.common.models import BaseEvent, LuxuryProduct

class Event(BaseEvent):
    parent_id   = StringField()
    group_title = StringField()

    meta = { 'db_alias': DB, }
    def url(self):
        return

class Product(LuxuryProduct):
    meta = { 'db_alias': DB, }
    def url(self):
        return

