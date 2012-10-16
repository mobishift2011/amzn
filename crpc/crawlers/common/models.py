#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.common.models
~~~~~~~~~~~~~~~~~~~~~~

"""
from mongoengine import *
from datetime import datetime, timedelta

class BaseCategory(Document):
    """ :py:class:crawlers.common.models.BaseCategory
    
    common category info
    crawlers should inherit from this base class
    
    >>> from crawlers.common.models import BaseCategory
    >>> class Category(BaseCategory):
    ...     pass

    """
    cats        =   ListField(StringField()) 
    is_leaf     =   BooleanField(default=False) # should set values to false manually
    update_time =   DateTimeField(default=datetime.utcnow)
    spout_time  =   DateTimeField() # time when we issue a new category fetch operation
    num         =   IntField()
    pagesize    =   IntField()
    meta        =   {
        "allow_inheritance": True,
        "collection": "caetgory",
        "indexes":  ["cats", ("is_leaf", "update_time"), "num", ],
    }

    def catstr(self):
        return " > ".join(self.cats)
    
    def url(self):
        raise NotImplementedError("should implemented in sub classes!")

class BaseProduct(Document):
    """ :py:class:crawlers.common.models.BaseProduct

    common product info
    crawlers should inherit from this base class

    >>> from crawlers.common.models import BaseProduct
    >>> class Product(BaseProduct):
    ...     pass

    """
    key                 =   StringField(primary_key=True)

    # meta infomation for record keeping
    updated             =   BooleanField(default=False)
    list_update_time    =   DateTimeField(default=datetime.utcnow)
    full_update_time    =   DateTimeField()

    # dimension info
    cats                =   ListField(StringField()) 
    like                =   StringField()  # how many likes
    rating              =   StringField()  # how it is rated, if any
    brand               =   StringField()
    model               =   StringField()
    models              =   ListField()
    price               =   StringField()

    # text info
    title               =   StringField()
    slug                =   StringField()
    summary             =   StringField() 

    # reviews
    num_reviews         =   StringField()
    reviews             =   ListField(StringField())

    # product images
    image_urls          =   ListField(StringField())

    meta                =   {
        "allow_inheritance": True,
        "collection": "product",
        "indexes":  ["key", "cats", "list_update_time", "full_update_time", "model", "brand", "updated"],
    }

    def catstr(self):
        return " > ".join(self.cats)

    def url(self):
        raise NotImplementedError("should implemented in sub classes!")

