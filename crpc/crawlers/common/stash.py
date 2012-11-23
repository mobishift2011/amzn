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
import pytz
from datetime import datetime
from gevent.coros import Semaphore

__lock = Semaphore()

login_email = 'huanzhu@favbuy.com'
login_passwd = '4110050209'

headers = { 
    'User-Agent': 'Mozilla 5.0/Firefox 16.0.1',
}
config = { 
    'max_retries': 5,
    'pool_connections': 10, 
    'pool_maxsize': 10, 
}
request = requests.Session(prefetch=True, timeout=30, config=config, headers=headers)


def progress(msg='.'):
    import sys 
    sys.stdout.write('.')
    sys.stdout.flush()


def singleton(cls):
    """.. :py:method::
        decorator for a singleton class
        add a lock the keep the singleton is co-routine safe
    """
    instances = {}
    def get_instance(*args, **kwargs):
        with __lock:
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


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


locked = {}
def exclusive_lock(name):
    """.. :py:method::
    A common lock for selenium or other crawlers when crawling category.
    
    @exclusive_lock(self.__class__.__name__)
    def crawl_category(self):
        pass

    @exclusive_lock('myhabit')
    def crawl_product(self):
        pass

    """
    if name not in locked:
        locked[name] = Semaphore()

    def safe_lock(func, *args, **kwargs):
        def wrapper(*args, **kwargs):
            with locked[name]:
                return func(*args, **kwargs)
        return wrapper
    return safe_lock


def time_convert(time_str, time_format, timezone='PT'):
    """.. :py:method::

    :param time_str: u'SAT OCT 20 9 AM '
    :param time_format: '%a %b %d %I %p %Y'
    :rtype: datetime type utc time
    """
    if timezone == 'PT' or timezone == 'PST' or timezone == 'PDT':
        pt = pytz.timezone('US/Pacific')
    elif timezone == 'ET' or timezone == 'EST' or timezone == 'EDT':
        pt = pytz.timezone('US/Eastern')

    tinfo = time_str + str(pt.normalize(datetime.now(tz=pt)).year)
    endtime = pt.localize(datetime.strptime(tinfo, time_format))
    return endtime.astimezone(pytz.utc)

