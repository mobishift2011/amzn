#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from mongoengine import *
from settings import MONGODB_HOST
DB = "techbargains"
connect(db=DB, alias=DB, host=MONGODB_HOST)

class Deal(Document):
    key = StringField(unique=True)

    title = StringField()
    description = StringField()
    price = StringField()
    listprice = StringField()
    image_url = StringField()
    original_url = StringField()
    shipping = StringField()

    meta = {
        'db_alias': DB,
    }
