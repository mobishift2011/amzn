'''
Created on 2012-11-19

@author: ethan
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import MONGODB_HOST

from mongoengine import *
from mongoengine import signals
from datetime import datetime, timedelta
DB = 'power'
connect(db=DB, alias=DB, host=MONGODB_HOST, , connecttimeoutms=1e10)

class EventProgress(Document):
    site = StringField(required=True)
    key = StringField(required=True, unique_with='site')
    
    image_complete = BooleanField(default=False)
    branch_complete = BooleanField(default=False)
    transfered = BooleanField(default=False)
    soldout = BooleanField(default=False)

    # statistics
    num_image      =   IntField(default=0)
    num_fails       =   IntField(default=0)
    
    started_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())
    
    # save which task trigger the progress, mostly applied for monitor.
    task_title = StringField()
    task_key = StringField()
    task_start = DateTimeField()
    
    meta = {
        'db_name': DB,
        'db_alias': DB,
        'indexes':  [('site', 'key'), 'site', 'updated_at'],
    }
    
    def __unicode__(self):
        return '%s_%s' % (self.site, self.key)
    
    def to_json(self):
        return {
            'site': self.site,
            'key': self.key,
            'image_complete': self.image_complete,
            'num_image': self.num_image,
            'branch_complete': self.branch_complete,
            'transfered': self.transfered,
            'soldout': self.soldout,
            'started_at': self.started_at.isoformat() if self.started_at else 'undefined',
            'updated_at': self.updated_at.isoformat() if self.updated_at else 'undefined',
            'task_title': self.task_title,
            'task_key': self.task_key,
            'task_start': self.task_start,
        }
    
    @staticmethod
    def inverse_status(st):
        return {0:'NOTHING',1:'IMAGE CRAWLING',2:'BRAND EXTRACT',3:'I&B',4:'PUSH',5:'I&P',6:'B&P',7:'I&B&P'}.get(st,'UNDEFINED')
    
    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.updated_at = datetime.utcnow()


class ProductProgress(Document):
    site = StringField(required=True)
    key = StringField(required=True, unique_with='site')
    
    image_complete = BooleanField(default=False)
    branch_complete = BooleanField(default=False)
    transfered = BooleanField(default=False)
    soldout = BooleanField(default=False)
    
    # statistics
    num_image      =   IntField(default=0)
    num_fails       =   IntField(default=0)
    
    started_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField(default=datetime.utcnow())
    
    # save which task trigger the progress, mostly applied for monitor.
    task_title = StringField()
    task_key = StringField()
    task_start = DateTimeField()
    
    meta = {
        'db_name': DB,
        'db_alias': DB,
        'indexes':  [('site', 'key'), 'site', 'updated_at'],
    }
    
    def __unicode__(self):
        return '%s_%s' % (self.site, self.key)
    
    def to_json(self):
        return {
            'site': self.site,
            'key': self.key,
            'image_complete': self.image_complete,
            'num_image': self.num_image,
            'branch_complete': self.branch_complete,
            'transfered': self.transfered,
            'soldout': self.soldout,
            'started_at': self.started_at.isoformat() if self.started_at else 'undefined',
            'updated_at': self.updated_at.isoformat() if self.updated_at else 'undefined',
            'task_title': self.task_title,
            'task_key': self.task_key,
            'task_start': self.task_start,
        }
    
    @staticmethod
    def inverse_status(st):
        return {0:'NOTHING',1:'IMAGE CRAWLING',2:'BRAND EXTRACT',3:'I&B',4:'PUSH',5:'I&P',6:'B&P',7:'I&B&P'}.get(st,'UNDEFINED')
    
    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.updated_at = datetime.utcnow()


def fail(site, method, key='', url='', message="undefined"):
    f = Fail(site=site, method=method, key=key, url=url, message=message)
    f.save()
    return f

class Fail(Document):
    """ stores failures """
    time            =   DateTimeField(default=datetime.utcnow)
    site            =   StringField()
    method          =   StringField()
    key             =   StringField()
    url             =   StringField()
    message         =   StringField()

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
    started_at      =   DateTimeField()
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
        "indexes":  [("status", "site", "method"), "started_at", "updated_at"],
    }

    def __str__(self):
        return str(self.to_json())

    def to_json(self):
        return {
            'name':         self.site+'.'+self.method,
            'status':       Task.inverse_status(self.status),
            'started_at':   self.started_at.isoformat() if self.started_at else 'undefined',
            'updated_at':   self.updated_at.isoformat() if self.updated_at else 'undefined',
            'fails':        self.num_fails,
            'dones':        self.num_finish,
            'updates':      self.num_update,
            'news':         self.num_new,
            'ctx':          self.ctx,
            #'fail_details': [f.to_json() for f in self.fails][-10:],
        }

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.updated_at = datetime.utcnow()

signals.pre_save.connect(Task.pre_save, sender=Task)
