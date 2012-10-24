#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from rpcserver import RPCServer
from routine import *
import crawllog
import sys

if __name__ == '__main__':
    rpc = RPCServer()
    if sys.argv[1] == 'myhabit':
        update_category('myhabit', rpc)
        update_product('myhabit', rpc)
    else:
        update_category('ruelala', rpc)
