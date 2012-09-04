#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
import settings

worker_type = settings.TYPE_MINT
num_workers = 1

configs = {
    'num_coroutines' : 1,   # num of concurrently running greenlets
    'qps_limit'      : 0,   # 0 -> not limiting, not implemented yet
}

def execute(self, **kwargs):
    logging.debug("sleep 10 sec")
    time.sleep(10)

def setup(self):
    pass
