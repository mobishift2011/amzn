from settings import MONGODB_HOST

from mongoengine import *
from datetime import datetime

connect(db='deal', host=MONGODB_HOST)

class BrandMonitor(Document):
    brand            =   StringField(unique=True)
    reason          =   StringField()
    site               =   ListField(StringField())
    sample        =   StringField()
    done             =   BooleanField(default=False)
    updated_at    =   DateTimeField()
    created_at     =   DateTimeField(default=datetime.now())
    
    meta = {
        'indexes': ['title'],
        'ordering': ['title']
    }
        
    def __unicode__(self):
        return self.title

    def to_json(self):
        return {
            'title'                :   self.title,
            'reason'            :   self.reason,
            'site'                 :   self.site,
            'samples'          :   self.samples,
            'done'               :   self.done,
            'updated_at'     :   str(self.updated_at)
            'created_at'      :   str(self.created_at)
        }