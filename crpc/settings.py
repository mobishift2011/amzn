#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
from itertools import chain

envs = {
    'COMMON': {
        'CRPC_ROOT': os.path.abspath(os.path.dirname(__file__)),
        'ENV_NAME': "crpc", 
    },
    'DEV': {
        'PEERS': ['root@127.0.0.1'],
        'USE_INDEX': ' --index-url http://e.pypi.python.org/simple/',
    },
    'TEST': {
        'PEERS': [
            'root@ec2-54-245-25-85.us-west-2.compute.amazonaws.com',
            'root@ec2-54-245-31-157.us-west-2.compute.amazonaws.com',
            'root@ec2-50-112-195-236.us-west-2.compute.amazonaws.com',
            'root@ec2-54-245-15-250.us-west-2.compute.amazonaws.com',
        ],
        'USE_INDEX': ' --index-url http://b.pypi.python.org/simple/',
    },
}

env = os.environ.get("ENV")
if not env:
    env = "DEV"

for key, value in chain(envs['COMMON'].iteritems(), envs[env].iteritems()):
    globals()[key] = value
