#!/usr/bin/env python
# -*- coding: utf-8 -*-

RPC_PORT = 1237

DB_HOST = 'mogodb.favbuy.org'
DB = 'bhphotovideo'

TIMEOUT = 60
#import redisco
#redisco.connection_setup(host=DB_HOST)

ITEM_PER_PAGE = 25

from mongoengine import *
connect(db=DB, host=DB_HOST)
