#!/usr/bin/env python
# -*- coding:utf-8 -*-
#from gevent import monkey; monkey.patch_all()

import os
import sys
from itertools import chain

envs = {
    'COMMON': {
        'CRPC_ROOT': os.path.abspath(os.path.dirname(__file__)),
        'ENV_NAME': "crpc", 
        'CRAWLER_PORT': 1234,
        'POWER_PORT': 1235,
    },
    'DEV': {
        'CRAWLER_PEERS': ['root@127.0.0.1'],
        'POWER_PEERS':['root@127.0.0.1'],
        'USE_INDEX': '',
        'MONGODB_HOST': '127.0.0.1',
        'REDIS_HOST': '127.0.0.1',
    },
    'HJC': {
        'CRAWLER_PEERS': ['root@192.168.56.102','root@192.168.56.103'],
        'POWER_PEERS':['root@192.168.56.101'],
        'USE_INDEX': '',
        'MONGODB_HOST': '192.168.56.101',
        'REDIS_HOST': '192.168.56.101',
    },
    'TEST2': {
        'CRAWLER_PEERS': [
            'root@54.245.60.173',
            'root@54.245.67.22',
            'root@54.245.49.77',
            'root@54.245.70.134',
        ],
        'POWER_PEERS': ['root@mongodb.favbuy.org'],
        'USE_INDEX': '',
        'MONGODB_HOST': 'mongodb.favbuy.org',
        'REDIS_HOST': 'mongodb.favbuy.org',
    },
    'TEST': {
        'CRAWLER_PEERS': [
            'root@ec2-54-245-60-173.us-west-2.compute.amazonaws.com',
            'root@ec2-54-245-67-22.us-west-2.compute.amazonaws.com',
            'root@ec2-54-245-49-77.us-west-2.compute.amazonaws.com',
            'root@ec2-54-245-70-134.us-west-2.compute.amazonaws.com',
        ],
        'POWER_PEERS': ['root@mongodb.favbuy.org'],
        'USE_INDEX': '',
        'MONGODB_HOST': 'mongodb.favbuy.org',
        'REDIS_HOST': 'mongodb.favbuy.org',
    },
}

env = os.environ.get("ENV")
if not env:
    env = "DEV"


for key, value in chain(envs['COMMON'].iteritems(), envs[env].iteritems()):
    globals()[key] = value

PEERS = CRAWLER_PEERS + POWER_PEERS

import redisco
redisco.connection_setup(host=REDIS_HOST)
