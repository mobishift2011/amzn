from django.db import models
from mongoengine import *
from mongoengine import signals
from datetime import datetime

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

class Fail(Document):
    title = StringField()
    model = StringField()   # Brand, Dept, Tag
    content = StringField() # The content of failure such as the brand name that can'be extacted.
    site = StringField()
    doctype = StringField() # Event or Product
    key = StringField(unique_with=['site', 'doctype'])
    url = StringField(default='')
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())

    meta = {
        'ordering': ['-updated_at'],
        # 'indexes': [
        #     {'fields': [('site', 'doctype', 'key')], 'unique': True}
        # ]
    }

    def to_json(self):
        return {
            'title': self.title,
            'model': self.model,
            'content': self.content,
            'site': self.site,
            'doctype': self.doctype,
            'key': self.key,
            'url': self.url,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
         document.updated_at = datetime.utcnow()

signals.pre_save.connect(Fail.pre_save, sender=Fail)
