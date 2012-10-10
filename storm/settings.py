#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
ENV_NAME = "pystormenv"
PEERS = [
            'root@ec2-54-245-25-85.us-west-2.compute.amazonaws.com',
            'root@ec2-54-245-31-157.us-west-2.compute.amazonaws.com',
            'root@ec2-50-112-195-236.us-west-2.compute.amazonaws.com',
            'root@ec2-54-245-15-250.us-west-2.compute.amazonaws.com',
        ]

#PEERS = ['root@127.0.0.1']#['root@192.168.56.102', 'root@192.168.56.103']

USE_INDEX = ' --index-url http://e.pypi.python.org/simple/'
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
