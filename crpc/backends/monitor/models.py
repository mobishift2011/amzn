#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import MONGODB_HOST

from mongoengine import *
from mongoengine import signals
from datetime import datetime, timedelta

DB = "monitor"
connect(db=DB, alias=DB, host=MONGODB_HOST, max_pool_size=50)

def fail(site, method, key='', url='', message="undefined", time=datetime.utcnow()):
    f = Fail(site=site, method=method, key=key, url=url, message=message, time=time)
    f.save()
    return f

class Schedule(Document):
    """ schedules info """
    site            =   StringField()
    method          =   StringField()
    description     =   StringField()
    minute          =   StringField()
    hour            =   StringField()
    dayofmonth      =   StringField()
    month           =   StringField()
    dayofweek       =   StringField()
    enabled         =   BooleanField(default=False)

    meta        =   {
         "db_alias": DB,
    }

    def get_crontab_arguments(self):
        return "{0} {1} {2} {3} {4}".format(self.minute, self.hour, self.dayofmonth, self.month, self.dayofweek)

    def timematch(self):
        t = datetime.utcnow()
        tsets = self._time_sets()
        return  t.minute in tsets['minute'] and \
                t.hour in tsets['hour'] and \
                t.day in tsets['dayofmonth'] and \
                t.month in tsets['month'] and \
                t.weekday() in tsets['dayofweek']

    def _time_sets(self):
        wholes = {'minute':60, 'hour':24, 'dayofmonth':31, 'month':12, 'dayofweek':7}
        names = ['minute', 'hour', 'dayofmonth', 'month', 'dayofweek']
        for name in names:
            if not getattr(self, name):
                setattr(self, name, "*")
        
        tsets = {} 
        for name in names:
            nsets = set()
            for e in getattr(self, name).split(','):
                if '/' in e:
                    # */3
                    star, div = e.rsplit('/',1)
                    if star != '*':
                        raise ValueError('valid syntax: */n')
                    nsets.update(filter(lambda x:x%int(div)==0, range(0,wholes[name])))
                elif '-' in e:
                    # 1-5
                    f, t = e.split('-')
                    nsets.update(range(int(f),int(t)+1))
                elif e == '*':
                    nsets.update(range(0, wholes[name]+1))
                else:
                    # 7
                    nsets.add(int(e))

            tsets[ name ] = nsets
    
        return tsets

class Fail(Document):
    """ stores failures """
    time            =   DateTimeField(default=datetime.utcnow)
    site            =   StringField()
    method          =   StringField()
    key             =   StringField()
    url             =   StringField()
    message         =   StringField()

    meta        =   {
         "db_alias": DB,
    }

    def __str__(self):
        return str(self.to_json())

    def to_json(self):
        return {
            'name':     self.site+'.'+str(self.method)+'.'+str(self.key)+'.'+str(self.url),
            'time':     self.time.isoformat(),
            'message':  self.message,
        }

class Task(Document):
    """.. :py:class: backends.controller.Task
    
        task orientied controlling model

    """
    READY, RUNNING, PAUSED, FAILED, FINISHED = 101, 102, 103, 104, 105
    @staticmethod
    def inverse_status(st):
        return {101:'READY',102:'RUNNING',103:'PAUSED',104:'FAILED',105:'FINISHED'}.get(st,'UNDEFINED')

    # timing
    started_at      =   DateTimeField(default=datetime.utcnow())
    updated_at      =   DateTimeField(default=datetime.utcnow())
    ended_at        =   DateTimeField()
    status          =   IntField() # READY, RUNNING, PAUSED, FAILED, FINISHED

    # meta
    ctx             =   StringField(unique=True)
    site            =   StringField()
    method          =   StringField() 
    fails           =   ListField(ReferenceField(Fail), default=[])

    # remote hosts
    peers           =   ListField(StringField(), default=[]) 

    # statistics
    num_finish      =   IntField(default=0)
    num_update      =   IntField(default=0)
    num_new         =   IntField(default=0)
    num_fails       =   IntField(default=0)

    # meta
    meta        =   {
        "indexes":  ["status", "site", "method", "started_at", "updated_at", "ended_at"],
        "db_alias": DB,
    }

    def __str__(self):
        return str(self.to_json())

    def to_json(self):
        return {
            'name':         self.site+'.'+self.method,
            'status':       Task.inverse_status(self.status),
            'started_at':   self.started_at.isoformat() if self.started_at else 'undefined',
            'updated_at':   self.updated_at.isoformat() if self.updated_at else 'undefined',
            'ended_at':     self.ended_at.isoformat() if self.ended_at else 'undefined',
            'fails':        self.num_fails,
            'dones':        self.num_finish,
            'updates':      self.num_update,
            'news':         self.num_new,
            'ctx':          self.ctx,
            #'fail_details': [f.to_json() for f in self.fails][-10:],
        }

#    @classmethod
#    def pre_save(cls, sender, document, **kwargs):
#         document.updated_at = datetime.utcnow()
#
#signals.pre_save.connect(Task.pre_save, sender=Task)

class Stat(Document):
    site        =   StringField(required = True)
    doctype     =   StringField(required = True)
    crawl_num   =   IntField(default = 0)
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
            'crawl_num': self.crawl_num,
            'image_num': self.image_num,
            'prop_num': self.prop_num,
            'publish_num': self.publish_num,
            'interval': self.interval,
            'created_at': str(self.created_at),
        }

#     @classmethod
#     def pre_save(cls, sender, document, **kwargs):
#         document.updated_at = datetime.utcnow()

# signals.pre_save.connect(Stat.pre_save, sender=Stat)



class ProductReport(Document):
    today_date          = DateTimeField()
    site                = StringField()

    product_num         = IntField(default=0)
    published_num       = IntField(default=0)

    # unpublished field
    no_image_url_num    = IntField(default=0)
    no_image_path_num   = IntField(default=0)
    no_dept_num         = IntField(default=0)
    event_not_ready     = IntField(default=0)
    unknown             = IntField(default=0)
    meta = {
        'db_alias': DB,
        'indexes': [
            {'fields': ['today_date', 'site'], 'unique': True},
        ],
    }

    def to_json(self):
        return {
            'site': self.site,
            'product_num': self.product_num,
            'published_num': self.published_num,
            'no_image_url_num': self.no_image_url_num,
            'no_image_path_num': self.no_image_path_num,
            'no_dept_num': self.no_dept_num,
            'event_not_ready': self.event_not_ready,
            'unknown': self.unknown,
        }

class EventReport(Document):
    today_date                      = DateTimeField()
    site                            = StringField()

    event_num                       = IntField(default=0)
    published_num                   = IntField(default=0)

    # unpublished field
    not_leaf_num                    = IntField(default=0)
    upcoming_no_image_url_num       = IntField(default=0)
    upcoming_no_image_path_num      = IntField(default=0)
    onsale_no_product_num           = IntField(default=0)
    onsale_no_image_url_num         = IntField(default=0)
    onsale_no_image_path_num        = IntField(default=0)
    onsale_propagation_not_complete = IntField(default=0)
    unknown                         = IntField(default=0)
    meta = {
        'db_alias': DB,
        'indexes': [
            {'fields': ['today_date', 'site'], 'unique': True},
        ],
    }

    def to_json(self):
        return {
            'site': self.site,
            'event_num': self.event_num,
            'published_num': self.published_num,
            'not_leaf_num': self.not_leaf_num,
            'upcoming_no_image_url_num': self.upcoming_no_image_url_num,
            'upcoming_no_image_path_num': self.upcoming_no_image_path_num,
            'onsale_no_product_num': self.onsale_no_product_num,
            'onsale_no_image_url_num': self.onsale_no_image_url_num,
            'onsale_no_image_path_num': self.onsale_no_image_path_num,
            'onsale_propagation_not_complete': self.onsale_propagation_not_complete,
            'unknown': self.unknown,
        }


if __name__ == '__main__':
    Schedule().timematch()
