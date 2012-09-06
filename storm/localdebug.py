#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from fabric.api import local, settings, cd, prefix


with settings(warn_only=True):
    local("rm -r /opt/pystorm/rpcserver/common/*")
    local("rm -r /opt/pystorm/rpcserver/workers/*")

os.system("bash -c 'cd /opt/pystorm/rpcserver && source /usr/local/bin/virtualenvwrapper.sh && workon pystormenv && python rpc.py'")
