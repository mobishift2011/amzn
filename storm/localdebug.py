#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fabric.api import local

local("rm /opt/pystorm/rpcserver/common/*")
local("rm /opt/pystorm/rpcserver/workers/*")


with cd("/opt/pystorm/rpcserver"):
    with prefix("source /usr/local/bin/virtualenvwrapper.sh")
        with prefix("workon pystormenv")
            local("python rpc.py")
