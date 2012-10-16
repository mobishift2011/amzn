#!/usr/bin/env python
# -*- coding: utf-8 -*-

RPC_PORT = 1238

DB_HOST = 'mongodb.favbuy.org'
DB = 'ecost'

TIMEOUT = 60
#import redisco
#redisco.connection_setup(host=DB_HOST)

ITEM_PER_PAGE = 25

from mongoengine import *
connect(db=DB, host=DB_HOST)

