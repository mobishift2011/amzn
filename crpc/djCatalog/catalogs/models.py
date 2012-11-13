from django.db import models
from mongoengine import *

class Brand(Document):
    title = StringField(unique=True)
    title_edit = StringField(default='')
    title_checked = BooleanField(default=False)
    keywords = StringField(default='')
    url = StringField(default='')
    url_checked = BooleanField(default=False)
    blurb = StringField(default='')
    level = IntField(default=0) # luxrious or not 
    dept = ListField(StringField(max_length=30))
    is_delete = BooleanField(default=False)
    done = BooleanField(default=False)
 
    meta = {
        'ordering': ['title']
    }
        
    def __unicode__(self):
        return self.title


class Dept(Document):
    title = StringField(unique=True)
    
    meta = {
        'ordering': ['title']
    }
    
    def __unicode__(self):
        return self.title


class Tag(Document):
    title = StringField(unique_with=('dept'))
    dept = ReferenceField(Dept)
    
    meta = {
        'ordering': ['dept', 'title']
    }
    
    def __unicode__(self):
        return self.title
