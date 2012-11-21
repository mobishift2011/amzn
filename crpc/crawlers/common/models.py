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
    is_leaf     =   BooleanField()
    update_time =   DateTimeField(default=datetime.utcnow)
    spout_time  =   DateTimeField() # time when we issue a new category fetch operation
    num         =   IntField()
    pagesize    =   IntField()
    combine_url =   StringField()

    meta        =   {
        "allow_inheritance": True,
        "collection": "category",
        "indexes":  ["is_leaf"],
    }

    def catstr(self):
        return " > ".join(self.cats)
    
    def url(self):
        raise NotImplementedError("should implemented in sub classes!")

class BaseEvent(BaseCategory):
    """ :py:class:crawlers.common.models.BaseBrand
    
    common brand info
    luxury crawlers should inherit from this this basic class
    
    >>> from crawlers.common.models import BaseBrand
    >>> class Event(BaseEvent):
    ...     pass

    """
    event_id            = StringField(unique=True)
    events_begin        = DateTimeField()
    events_end          = DateTimeField()
    create_time         = DateTimeField(default=datetime.utcnow)
    soldout             = BooleanField(default=False)
    sale_title          = StringField()
    image_urls          = ListField(StringField())
    image_path          = ListField(StringField())
    sale_description    = StringField()
    dept                = ListField(StringField())

    # after setting urgent to False, you can't set it back
    urgent              = BooleanField(default=True)

    meta = {
        "indexes": ["urgent", "events_begin", "events_end", "soldout", "event_id"],
    }

class BaseReview(Document):
    """ :py:class:crawlers.common.models.BaseReview

    common review info
        
    """
    post_time       =   DateTimeField() # when the review is made
    username        =   StringField()
    title           =   StringField()
    content         =   StringField()
    rating          =   StringField()

    meta            =   {
        "allow_inheritance": True,
        "collection": "review",
        "indexes": ['post_time'],
    }

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
    products_end        =   DateTimeField()

    # dimension info
    cats                =   ListField(StringField()) 
    like                =   StringField()  # how many likes
    rating              =   StringField()  # how it is rated, if any
    brand               =   StringField()
    model               =   StringField()
    models              =   ListField()
    price               =   StringField()
    sell_rank           =   IntField()
    combine_url         =   StringField()

    # text info
    title               =   StringField()
    slug                =   StringField()
    summary             =   StringField() 
    detail              =   StringField()
    shipping            =   StringField()
    available           =   StringField()

    # reviews
    num_reviews         =   StringField()
    reviews             =   ListField(ReferenceField(BaseReview))

    # product images
    image_urls          =   ListField(StringField())
    image_path          =   ListField(StringField())

    meta                =   {
        "allow_inheritance": True,
        "collection": "product",
        "indexes":  ["key", "list_update_time", "full_update_time", "model", "brand", "updated"],
    }

    def url(self):
        raise NotImplementedError("should implemented in sub classes!")

class LuxuryProduct(BaseProduct):
    """ :py:class:crawlers.common.models.LuxuryProduct

    luxury product info
    crawlers should inherit from this base class

    >>> from crawlers.common.models import LuxuryProduct
    >>> class Product(LuxuryProduct):
    ...     pass

    """
    # associate to Event's unique key
    event_id            =   ListField(StringField())
    create_time         =   DateTimeField(default=datetime.utcnow)
    products_end        =   DateTimeField()

    soldout             =   BooleanField(default=False)

    listprice           =   StringField()
    color               =   StringField()
    returned            =   StringField()
    sizes_scarcity      =   ListField()
    sizes               =   ListField(StringField())
    scarcity            =   StringField()
    list_info           =   ListField(StringField())


    meta                = {
        "indexes": ["soldout"],
    }
