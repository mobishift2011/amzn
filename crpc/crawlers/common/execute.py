#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from rpcserver import RPCServer
from routine import *
import crawllog

if __name__ == '__main__':
    rpc = RPCServer()
    update_category('myhabit', rpc)
