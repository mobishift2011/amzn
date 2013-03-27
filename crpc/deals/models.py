from settings import MONGODB_HOST

from mongoengine import *
from datetime import datetime

connect(db='deal', host=MONGODB_HOST)

class BrandMonitor(Document):
    brand            =   StringField(unique=True)
    reason          =   StringField()
    site               =   ListField(StringField())
    sample          =   StringField()
    done             =   BooleanField(default=False)
    updated_at    =   DateTimeField()
    created_at     =   DateTimeField(default=datetime.now())
    
    meta = {
        'indexes': ['brand'],
        'ordering': ['brand']
    }
        
    def __unicode__(self):
        return self.title

    def to_json(self):
        return {
            'brand'              :   self.brand,
            'reason'            :   self.reason,
            'site'                 :   self.site,
            'sample'          :     self.sample,
            'done'               :   self.done,
            'updated_at'      :   str(self.updated_at),
            'created_at'       :   str(self.created_at)
        }