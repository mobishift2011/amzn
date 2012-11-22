# -*- coding: utf-8 -*-
"""
crawlers.amazon.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for Gilt

Created on 2012-10-26

@author: ethan

"""

from crawlers.common.models import BaseEvent, LuxuryProduct
from settings import MONGODB_HOST
from mongoengine import *
import requests

DB = 'gilt'
connect(db=DB, alias=DB, host=MONGODB_HOST)

STORE = {
    'women': 'women',
    'men': 'men',
    'kids': 'children',
    'home': 'home'
}

class Event(BaseEvent):
    TYPE = (
        ('sale', 'sales'),
        ('category', 'category')
    )
      
    store = StringField()
    type = StringField(choices=TYPE)    # sale, category
    dept = ListField(StringField())
    
    meta = {
        'db_name': DB,
        'db_alias': DB,
    }
    
    def link(self):
        return "http://www.gilt.com/{0}/{1}/{2}".format(self.type, STORE[self.store], self.event_id)
    
    def url(self):
        return "https://api.gilt.com/v1/sales/{0}/{1}/detail.json".format(self.store, self.event_id)

class Product(LuxuryProduct):
    store = StringField()
    product_key = StringField()  # unique key for get-a-product page, not product id, product id is field 'key' in the base class
    dept = ListField(StringField())
    skus = ListField()
    
    meta = {
        'db_name': DB,
        'db_alias': DB,
    }
    
    def link(self):
        if self.key == self.product_key:
            return None
        url = "http://www.gilt.com/sale/{0}/{1}/product/{2}".format(STORE[self.store], self.event_id[-1], self.product_key)
        return url
    
    def url(self):
        return "https://api.gilt.com/v1/products/{0}/detail.json".format(self.key)


class Gilt():
    __base_call_url = 'https://api.gilt.com/v1'
    __stores = ['women', 'men', 'kids', 'home']
    
    def stores(self):
        return self.__stores
    
    def __init__(self, apikey=None):
        self.__apikey = apikey
    
    def request(self, url):
        params = {'apikey': self.__apikey}
        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.json
    
    def sales_active(self, store=None):
        url = '%s/sales/%s/active.json' % (self.__base_call_url, store or '')
        return self.request(url)
    
    def sales_upcoming(self, store=None):
        url = '%s/sales/%s/upcoming.json' % (self.__base_call_url, store or '')
        return self.request(url)
    
    def product_detail(self, pid):
        url = '%s/products/%s/detail.json' % (self.__base_call_url, pid)
        return self.request(url)
    
    def products_categories(self):
        url = '%s/products/categories.json' % self.__base_call_url
        return self.request(url)

giltClient = Gilt(apikey='927a58fd5ced700ee4d1126879fa9ab0')
