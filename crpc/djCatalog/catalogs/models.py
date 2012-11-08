from django.db import models
from mongoengine import *

class Brand(Document):
    title = StringField(unique=True)
    url = URLField()
    blurb = StringField()
    level = IntField(default=1) # luxrious or not 
    dept = ListField(StringField(max_length=30))
 
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