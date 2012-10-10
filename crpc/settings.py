#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys

CRPC_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, CRPC_ROOT)

ENV_NAME = "crpc"

FETCHING_PEERS = [
    'root@ec2-54-245-25-85.us-west-2.compute.amazonaws.com',
    'root@ec2-54-245-31-157.us-west-2.compute.amazonaws.com',
]

PARSING_PEERS = [
    'root@ec2-50-112-195-236.us-west-2.compute.amazonaws.com',
    'root@ec2-54-245-15-250.us-west-2.compute.amazonaws.com',
]

PEERS = []
PEERS.extend(FETCHING_PEERS)
PEERS.extend(PARSING_PEERS)

#PEERS = ['root@127.0.0.1']
USE_INDEX = ' --index-url http://b.pypi.python.org/simple/'
