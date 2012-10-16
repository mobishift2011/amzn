#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


RPC_PORT = 1234

DB_HOST = 'ec2-50-112-70-241.us-west-2.compute.amazonaws.com'
DB = 'amazon'

import redisco
redisco.connection_setup(host=DB_HOST)

from mongoengine import *
connect(db=DB, host=DB_HOST)

