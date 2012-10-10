#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import Stat
import zerorpc

def crawl(remote, caller, *args):
    s = Stat.get_or_create(caller)
    try:
        getattr(remote, caller)(*args)
    except zerorpc.RemoteError, e:
        import traceback
        s.error(traceback.format_exc())
    else:
        s.incr()

