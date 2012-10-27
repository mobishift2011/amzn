#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawler.common.stash
~~~~~~~~~~~~~~~~~~~

This module is a common function collections used by all the crawlers.

"""
import requests
import re


headers = { 
    'User-Agent': 'Mozilla 5.0/Firefox 16.0.1',
}
config = { 
    'max_retries': 3,
    'pool_connections': 10, 
    'pool_maxsize': 10, 
}
request = requests.Session(prefetch=True, timeout=17, config=config, headers=headers)


def progress(msg='.'):
    import sys 
    sys.stdout.write('.')
    sys.stdout.flush()

def fetch_page(url):
    try:
        ret = request.get(url)
    except:
        # page not exist or timeout
        return

    if ret.ok: return ret.content

def login_page(url, data):
    """
        data = {key1: value1, key2: value2}
    """
    request.post(url, data=data)

