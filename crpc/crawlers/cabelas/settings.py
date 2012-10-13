#!/usr/bin/env python
# -*- coding: utf-8 -*-

RPC_PORT = 1239

DB_HOST = 'mongodb.favbuy.org'
DB = 'cabelas'

TIMEOUT = 60
ITEM_PER_PAGE = 48

from mongoengine import *
connect(db=DB, host=DB_HOST)

