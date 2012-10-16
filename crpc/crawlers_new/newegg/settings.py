#!/usr/bin/env python
# -*- coding: utf-8 -*-
RPC_PORT = 1235

DB_HOST = 'ec2-50-112-70-241.us-west-2.compute.amazonaws.com'
DB = 'newegg'

from mongoengine import *
connect(db=DB, host=DB_HOST)

