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

class BrandTask(Document):
    title = StringField()
    brand = StringField()
    favbuy_brand = StringField()
    site = StringField()
    doctype = StringField() # Event or Product
    key = StringField()
    url = StringField(default='')
    brand_complete = BooleanField(default=False)   # False
    is_checked = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())

    meta = {
        'ordering': ['-updated_at'],
        # 'indexes': [
        #     {'fields': [('site', 'doctype', 'key')], 'unique': True},
        # ]
    }

    def to_json(self):
        return {
            'pk': self.pk,
            'title': self.title,
            'brand': self.brand,
            'favbuy_brand': self.favbuy_brand,
            'site': self.site,
            'doctype': self.doctype,
            'key': self.key,
            'url': self.url,
            'brand_complete': self.brand_complete,
            'is_checked': self.is_checked,
            'created_at': str(self.created_at),
            'updated_at': str(self.updated_at)
        }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.updated_at = datetime.utcnow()

signals.pre_save.connect(BrandTask.pre_save, sender=BrandTask)
