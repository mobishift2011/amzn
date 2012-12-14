'''
crawlers.venteprivee.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for hautelook

Created on 2012-11-16

@author: ethan
'''

from crawlers.common.models import BaseEvent, LuxuryProduct

import requests

from mongoengine import *
from settings import MONGODB_HOST, CRAWLER_PORT
DB = 'venteprivee'
connect(db=DB, alias=DB, host=MONGODB_HOST)


class Event(BaseEvent):
    type = StringField()
    
    meta = {
        'db_name': DB,
        'db_alias': DB,
    }
    
    def url(self):
        return 'http://us.venteprivee.com/v1/api/catalog/content/%s' % self.event_id

class Product(LuxuryProduct):
    meta = {
        # 'db_name': DB,
        'db_alias': DB,
    }
    
    def url(self):
        return "http://us.venteprivee.com/v1/api/productdetail/content/%s" % self.key


class VClient(object):
    __base_call_url = 'http://us.venteprivee.com/v1/api'
    
    def __init__(self):
        self.__is_auth = False
    
    def request(self, url):
        r = requests.get(url)
        r.raise_for_status()
        return r.json
    
    def sales(self):
        url = "%s/shop/default" % self.__base_call_url
        return self.request(url).get('sales')
    
    def catalog(self, event_id):
        url = "%s/catalog/content/%s" % (self.__base_call_url, event_id)
        return self.request(url) 
    
    def product_detail(self, pfid):
        url = "%s/productdetail/content/%s" % (self.__base_call_url, pfid)
        return self.request(url)

vclient = VClient()
