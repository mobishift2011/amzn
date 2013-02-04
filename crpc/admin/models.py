from settings import MONGODB_HOST
from mongoengine import *
from datetime import datetime

connect(db='catalogIndex', host=MONGODB_HOST)

class Brand(Document):
    title           =   StringField(unique=True)
    title_edit      =   StringField()
    title_checked   =   BooleanField(default=False)
    alias           =   ListField(StringField(), default=list())
    keywords        =   StringField(default='')
    url             =   StringField(default='')
    url_checked     =   BooleanField(default=False)
    blurb           =   StringField(default='')
    images          =   ListField(StringField())   
    level           =   IntField(default=0) # luxrious or not 
    dept            =   ListField(StringField(max_length=30))
    is_delete       =   BooleanField(default=False)
    done            =   BooleanField(default=False)
    created_at      =   DateTimeField(default=datetime.now())
 
    meta = {
        'ordering': ['title']
    }
        
    def __unicode__(self):
        return self.title

    def to_json(self):
        return {
            'title'           :   self.title,
            'title_edit'      :   self.title_edit,
            'title_checked'   :   self.title_checked,
            'alias'           :   self.alias,
            'keywords'        :   self.keywords,
            'url'             :   self.url,
            'url_checked'     :   self.url_checked,
            'blurb'           :   self.blurb,
            'images'          :   self.images,
            'level'           :   self.level,
            'dept'            :   self.dept,
            'is_delete'       :   self.is_delete,
            'done'            :   self.done,
            'created_at'      :   str(self.created_at)
        }