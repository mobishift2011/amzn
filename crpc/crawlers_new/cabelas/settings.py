#!/usr/bin/env python
# -*- coding: utf-8 -*-

RPC_PORT = 1239

#DB_HOST = 'ec2-54-245-3-3.us-west-2.compute.amazonaws.com'
DB_HOST = 'ec2-54-245-40-206.us-west-2.compute.amazonaws.com'
DB = 'cabelas'

TIMEOUT = 60
ITEM_PER_PAGE = 48

from mongoengine import *
connect(db=DB, host=DB_HOST)

