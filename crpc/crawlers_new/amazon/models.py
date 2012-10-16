#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from mongoengine import *
from redisco import models
from urllib import quote, unquote
from datetime import datetime, timedelta

def catn2url(catn): 
    return 'http://www.amazon.com/s?ie=UTF8&rh=' + quote(catn.encode("utf-8"))

def url2catn(url): 
    m = re.compile(r'(n%3A.*?)&').search(url)
    if not m:
        m = re.compile(r'(n%3A.*)').search(url)
        if not m:
            return ''
    catn = unquote(m.group(1)).decode('utf-8')
    catn = [x for x in catn.split(',') if x.startswith('n:')][-1]
    return catn

class Category(Document):
    cats        =   ListField(StringField()) 
    is_leaf     =   BooleanField(default=False)
    update_time =   DateTimeField(default=datetime.utcnow)
    spout_time  =   DateTimeField()
    catn        =   StringField(unique=True)
    num         =   IntField() 
    pagesize    =   IntField()
    meta        =   {
        "indexes":  ["cats", ("is_leaf", "update_time"), "num", ],
    }
    def url(self):
        return catn2url(self.catn)
    def catstr(self):
        return " > ".join(self.cats)

class Product(Document):
    asin                =   StringField(primary_key=True)
    updated             =   BooleanField()
    cover_image_url     =   StringField()
    list_update_time    =   DateTimeField(default=datetime.utcnow)
    full_update_time    =   DateTimeField(default=datetime.utcnow)
    cats                =   ListField(StringField()) 
    catns               =   ListField(StringField())
    like                =   IntField()
    manufactory         =   StringField()
    brand               =   StringField()
    model               =   StringField()
    price               =   FloatField()
    pricestr            =   StringField()
    salesrank           =   StringField()
    stars               =   FloatField()
    reviews_count       =   IntField()
    title               =   StringField()
    slug                =   StringField()
    summary             =   StringField() 
    vartitle            =   StringField()
    meta                =   {
        "indexes":  ["asin", "cats", "list_update_time", "full_update_time", "model", "brand", "updated"],
    }
    def url(self):
        return "http://www.amazon.com/{slug}/dp/{asin}/".format(slug=self.slug, asin=self.asin)
    def catstr(self):
        return " > ".join(self.cats)

