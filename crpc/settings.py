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
        'MASTIFF_HOST': "http://intergrate.favbuy.org:8001/api/v1"
    },
    'DEV': {
        'CRAWLER_PEERS': [
            {'host_string':'root@127.0.0.1', 'port':1234},
        ],
        'POWER_PEERS': [
            {'host_string':'root@127.0.0.1', 'port':1235},
        ],
        'USE_INDEX': '',
        'MONGODB_HOST': '127.0.0.1',
        'REDIS_HOST': '127.0.0.1',
        'MASTIFF_HOST': "http://localhost:8001/api/v1"
    },
    'OFFICE': {
        'CRAWLER_PEERS': [
            {'host_string':'root@127.0.0.1', 'port':1234},
        ],
        'POWER_PEERS':[
            {'host_string':'root@192.168.2.111', 'port':1235},
        ],
        'USE_INDEX': '', 
        'MONGODB_HOST': '127.0.0.1',
        'REDIS_HOST': '127.0.0.1',
    },
    'HJC': {
        'CRAWLER_PEERS': [
            {'host_string':'root@192.168.56.102', 'port':1234},
            {'host_string':'root@192.168.56.103', 'port':1234},
        ],
        'POWER_PEERS':[
            {'host_string':'root@192.168.56.101', 'port':1235},
        ],
        'USE_INDEX': '',
        'MONGODB_HOST': '192.168.56.101',
        'REDIS_HOST': '192.168.56.101',
    },
    'TEST': {
        'CRAWLER_PEERS': [
            {'host_string':'root@ec2-54-245-60-173.us-west-2.compute.amazonaws.com', 'port':1234},
            {'host_string':'root@ec2-54-245-67-22.us-west-2.compute.amazonaws.com', 'port':1234},
            {'host_string':'root@ec2-54-245-49-77.us-west-2.compute.amazonaws.com', 'port':1234},
            {'host_string':'root@ec2-54-245-70-134.us-west-2.compute.amazonaws.com', 'port':1234},
        ],
        'POWER_PEERS': [
            {'host_string':'root@ec2-54-245-35-92.us-west-2.compute.amazonaws.com', 'port':1235},
        ],
        'USE_INDEX': '',
        'MONGODB_HOST': 'mongodb.favbuy.org',
        'REDIS_HOST': 'mongodb.favbuy.org',
    },
    'HM': {
        'CRAWLER_PEERS': [
            {'host_string':'root@ec2-50-112-220-196.us-west-2.compute.amazonaws.com', 'port':1023},
            {'host_string':'root@ec2-50-112-220-196.us-west-2.compute.amazonaws.com', 'port':1024},
            {'host_string':'root@ec2-50-112-220-196.us-west-2.compute.amazonaws.com', 'port':1025},
            {'host_string':'root@ec2-50-112-220-196.us-west-2.compute.amazonaws.com', 'port':1027},
        ],
        'POWER_PEERS':[
            {'host_string':'root@ec2-50-112-220-196.us-west-2.compute.amazonaws.com', 'port':1028},
        ],
        'PUBLISH_PEERS': [
            'root@mongodb.favbuy.org',
        ],
        'USE_INDEX': '',
        'MONGODB_HOST': 'ec2-50-112-220-196.us-west-2.compute.amazonaws.com',
        'REDIS_HOST': 'ec2-50-112-220-196.us-west-2.compute.amazonaws.com',
    },
    'INTEG': {
        'CRAWLER_PEERS': ['root@127.0.0.1'],
        'POWER_PEERS': ['root@127.0.0.1'],
        'PUBLISH_PEERS': ['root@127.0.0.1'],
        'USE_INDEX': '',
        'MONGODB_HOST': '127.0.0.1',
        'REDIS_HOST': '127.0.0.1',
        'MASTIFF_HOST': "http://localhost:8001/api/v1"
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
