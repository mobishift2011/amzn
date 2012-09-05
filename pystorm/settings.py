#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
ENV_NAME = "pystormenv"
PEERS = [
            'root@ec2-50-112-8-128.us-west-2.compute.amazonaws.com',
            'root@ec2-50-112-11-0.us-west-2.compute.amazonaws.com',
            'root@ec2-50-112-60-174.us-west-2.compute.amazonaws.com',
            'root@ec2-50-112-85-43.us-west-2.compute.amazonaws.com',
        ]
PEERS = ['root@192.168.56.102', 'root@192.168.56.103']
USE_INDEX = ' --index-url http://e.pypi.python.org/simple/'
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
