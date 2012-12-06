#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.common.models
~~~~~~~~~~~~~~~~~~~~~~

"""
from mongoengine import *
from datetime import datetime, timedelta

class BaseDocumentSkeleton(object):
    """ :py:class:crawlers.common.models.BaseDocumentSkeleton

        common base class, we can not override meta information in subclass
    """
    spout_time          =   DateTimeField() # time when we issue a new category fetch operation
    create_time         =   DateTimeField(default=datetime.utcnow)
    update_time         =   DateTimeField(default=datetime.utcnow)
    is_leaf             =   BooleanField() # whether this Event/Category is leaf, need to be spouted

    # url this collections' object have
    combine_url         =   StringField()
    num                 =   IntField()
    image_urls          =   ListField(StringField(), default=list)
    image_path          =   ListField(StringField(), default=list)
    
    # text info
    slug                =   StringField()
    sale_title          =   StringField()
    sale_description    =   StringField()


class BaseCategory(Document, BaseDocumentSkeleton):
    """ :py:class:crawlers.common.models.BaseCategory
    
    common category info
    crawlers should inherit from this base class
    
    >>> from crawlers.common.models import BaseCategory
    >>> class Category(BaseCategory):
    ...     pass

    """
    cats        =   ListField(StringField()) # ['home', 'Textiles']
    pagesize    =   IntField()

    meta        =   {
        "allow_inheritance": True,
        "collection": "category",
        "indexes":  ["is_leaf"],
    }

    def catstr(self):
        return " > ".join(self.cats)
    
    def url(self):
        raise NotImplementedError("should implemented in sub classes!")

class BaseEvent(Document, BaseDocumentSkeleton):
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
    soldout             = BooleanField(default=False)
    dept                = ListField(StringField())

    # after setting urgent to False, you can't set it back
    # after event complete by crawler, urgent is False
    urgent              = BooleanField(default=True)
    

    image_complete      =   BooleanField(default=False)
    brand_complete      =   BooleanField(default=False)
    propagation_complete=   BooleanField(default=False)
    publish_time        =   DateTimeField()

    favbuy_brand        =   ListField(StringField(), default=list)
    favbuy_tag          =   ListField(StringField(), default=list)
    favbuy_dept         =   ListField(StringField(), default=list)
    lowest_price        =   StringField()
    highest_price       =   StringField()
    lowest_discount     =   StringField()
    highest_discount    =   StringField()

    muri                =   StringField()   # resource URL in mastiff
    
    meta = {
        "allow_inheritance": True,
        "collection": "event",
        "indexes": ["urgent", "events_begin", "events_end", "soldout", "event_id", "is_leaf"],
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
    updated             =   BooleanField(default=False) # after product is fully crawled, updated is True
    list_update_time    =   DateTimeField(default=datetime.utcnow)
    full_update_time    =   DateTimeField()

    # dimension info
    category_key        =   ListField(StringField()) # like event_id, but in category
    cats                =   ListField(StringField()) # ['home > Textiles', 'home > lighting']
    like                =   StringField()  # how many likes
    rating              =   StringField()  # how it is rated, if any
    brand               =   StringField()
    model               =   StringField()
    models              =   ListField() # maybe several models in one product
    price               =   StringField()
    sell_rank           =   IntField()
    combine_url         =   StringField()
    dept                =   ListField(StringField())
    tagline             =   ListField(StringField(), default=list)

    # text info
    title               =   StringField()
    slug                =   StringField()
    summary             =   StringField() 
    detail              =   StringField()
    shipping            =   StringField()
    available           =   StringField()
    short_desc          =   StringField()

    # reviews
    num_reviews         =   StringField()
    reviews             =   ListField(ReferenceField(BaseReview))

    # product images
    image_urls          =   ListField(StringField(), default=list)
    image_path          =   ListField(StringField(), default=list)

    image_complete      =   BooleanField(default=False)
    brand_complete      =   BooleanField(default=False)
    tag_complete        =   BooleanField(default=False)
    dept_complete       =   BooleanField(default=False)
    publish_time        =   DateTimeField()

    favbuy_brand        =   StringField(default='')
    favbuy_tag          =   ListField(StringField(), default=list)
    favbuy_dept         =   ListField(StringField(), default=list)
    favbuy_price        =   StringField()

    muri                =   StringField()   # resource URL in mastiff
    
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
    event_type          =   BooleanField(default=True) # whether this product spout by Event
    create_time         =   DateTimeField(default=datetime.utcnow)
    products_begin      =   DateTimeField()
    products_end        =   DateTimeField()

    soldout             =   BooleanField(default=False)

    listprice           =   StringField()
    color               =   StringField()
    returned            =   StringField()
    sizes_scarcity      =   ListField()
    sizes               =   ListField(StringField())
    scarcity            =   StringField()
    list_info           =   ListField(StringField())
    
    favbuy_listprice    =   StringField()
    
    meta                = {
        "indexes": ["soldout"],
    }
