#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from mongoengine import *
from redisco import models
from urllib import quote, unquote
from datetime import datetime, timedelta

class Category(Document):
    update_time =   DateTimeField(default=datetime.utcnow)
    spout_time  =   DateTimeField()
    catid       =   IntField(unique=True)
    catname     =   StringField()
    num         =   IntField()
    meta        =   {
        "indexes":  ["update_time", "num", ],
    }
    def url(self, page=1):
        return 'http://www.newegg.com/Store/SubCategory.aspx?SubCategory={0}&name={1}&PageSize=100&Page={2}&Order=RATING'.format(self.catid, self.catname, page)
        
    def catstr(self):
        return " > ".join(self.cats)

class Product(Document):
    itemid              =   StringField(primary_key=True)
    catids              =   ListField(IntField())
    updated             =   BooleanField()
    cover_image_url     =   StringField()
    list_update_time    =   DateTimeField(default=datetime.utcnow)
    full_update_time    =   DateTimeField(default=datetime.utcnow)
    cats                =   ListField(StringField()) 
    comments            =   ListField(StringField())
    price               =   StringField()
    promote             =   StringField()
    suggests            =   ListField(StringField())
    title               =   StringField()
    description         =   StringField()
    model               =   StringField()
    brand               =   StringField()
    details             =   StringField()
    extrainfo           =   DictField()
    def url(self):
        return 'http://www.newegg.com/Product/Product.aspx?Item={0}&SortField=1'.format(self.itemid)
    def catstr(self):
        return " > ".join(self.cats)

