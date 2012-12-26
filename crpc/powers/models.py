# -*- coding: utf-8 -*-

from settings import MONGODB_HOST

from mongoengine import *
from mongoengine import signals
from datetime import datetime
DB = 'power'
connect(db=DB, alias=DB, host=MONGODB_HOST)

class Brand(Document):
    title           =   StringField(unique = True)
    title_edit      =   StringField(default = '')
    title_checked   =   BooleanField(default = False)
    keywords        =   StringField(default = '')
    url             =   StringField(default = '')
    url_checked     =   BooleanField(default = False)
    blurb           =   StringField(default = '')
    level           =   IntField(default = 0) # luxrious or not 
    dept            =   ListField(StringField(max_length = 30))
    is_delete       =   BooleanField(default = False)
    done            =   BooleanField(default = False)
 
    meta = {
        'db_name': DB,
        'db_alias': DB,
        'indexes': ['title', 'title_checked', 'is_delete', 'done'],
        'ordering': ['title']
    }
        
    def __unicode__(self):
        return self.title

class Stat(Document):
    site        =   StringField(required = True)
    doctype     =   StringField(required = True)
    image_num   =   IntField(default = 0)
    prop_num    =   IntField(default = 0)
    publish_num =   IntField(default = 0)
    interval    =   DateTimeField()
    created_at  =   DateTimeField(default = datetime.utcnow)

    meta = {
        'db_name': DB,
        'db_alias': DB,
        'indexes': ['site', 'doctype', 'interval', ('site', 'doctype', 'interval')],
        'ordering': ['-interval'],
    }

    def to_json(self):
        return {
            'site': self.site,
            'doctype': self.doctype,
            'image_num': self.image_num,
            'prop_num': self.prop_num,
            'publish_num': self.publish_num,
            'interval': self.interval,
            'created_at': str(self.created_at),
        }

#     @classmethod
#     def pre_save(cls, sender, document, **kwargs):
#         document.updated_at = datetime.utcnow()

# signals.pre_save.connect(Task.pre_save, sender=Task)
