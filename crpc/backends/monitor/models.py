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
    fails           =   ListField(ReferenceField(Fail))

    # remote hosts
    peers           =   ListField(StringField()) 

    # statistics
    num_finish      =   IntField()
    num_update      =   IntField()
    num_new         =   IntField()

    # meta
    meta        =   {
        "indexes":  [("status", "site", "method"), "started_at"],
    }
