'''
crawlers.venteprivee.models
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category Model for hautelook

Created on 2012-11-16

@author: ethan
'''

from crawlers.common.models import BaseEvent, LuxuryProduct

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
        'db_alias': DB,
    }
    
    def url(self):
        return "http://us.venteprivee.com/v1/api/productdetail/content/%s" % self.key

