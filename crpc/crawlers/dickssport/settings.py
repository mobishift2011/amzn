#!/usr/bin/env python
# -*- coding: utf-8 -*-

RPC_PORT = 1240

DB_HOST = 'ec2-50-112-19-38.us-west-2.compute.amazonaws.com'
DB = 'dickssport'

TIMEOUT = 60
ITEM_PER_PAGE = 12

from mongoengine import *
connect(db=DB, host=DB_HOST)

import redis
redis_KEY = DB
redis_SERVER = redis.Redis(host=DB_HOST, port=6379)
