#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import MONGODB_HOST

from mongoengine import *
from datetime import datetime, timedelta

connect(db="monitor", host=MONGODB_HOST)

class Fail(Document):
    """ stores failures """
    time            =   DateTimeField(default=datetime.utcnow)
    site            =   StringField()
    method          =   StringField()
    key             =   StringField()
    message         =   StringField()

    def __str__(self):
        return self.to_json()

    def to_json(self):
        return {
            'name':     self.site+'.'+str(self.method)+'.'+str(self.key),
            'time':     self.time.isoformat(),
            'message':  self.message,
        }

class Task(Document):
    """.. :py:class: backends.controller.Task
    
        task orientied controlling model

    """
    READY, RUNNING, PAUSED, FAILED, FINISHED = 101, 102, 103, 104, 105

    # timing
    started_at      =   DateTimeField()
    ended_at        =   DateTimeField()
    status          =   IntField() # READY, RUNNING, PAUSED, FAILED, FINISHED

    # meta
    site            =   StringField()
    method          =   StringField() 
    fails           =   ListField(ReferenceField(Fail), default=[])

    # remote hosts
    peers           =   ListField(StringField(), default=[]) 

    # statistics
    num_finish      =   IntField(default=0)
    num_update      =   IntField(default=0)
    num_new         =   IntField(default=0)

    # meta
    meta        =   {
        "indexes":  [("status", "site", "method"), "started_at"],
    }

    def __str__(self):
        return self.to_json()

    def to_json(self):
        return {
            'name':         self.site+'.'+self.method,
            'status':       self.status,
            'started_at':   self.started_at.isoformat(),
            'fails':        len(self.fails),
            'dones':        self.num_finish,
            'updates':      self.num_update,
            'news':         self.num_new,
            'fail_details': [f.to_json() for f in self.fails],
        }
