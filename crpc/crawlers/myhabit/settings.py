#!/usr/bin/env python
# -*- coding: utf-8 -*-

RPC_PORT = 1242

DB_HOST = 'mongodb.favbuy.org'
DB = 'myhabit'

TIMEOUT = 60
ITEM_PER_PAGE = 12

from mongoengine import *
connect(db=DB, host=DB_HOST)

import redis
redis_KEY = DB
redis_SERVER = redis.Redis(host=DB_HOST, port=6379)
