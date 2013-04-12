#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
"""
crawler.common.stash
~~~~~~~~~~~~~~~~~~~

This module is a common function collections used by all the crawlers.

"""
import re
import os
import pytz
import requests
import ConfigParser
import random
from datetime import datetime
from gevent.coros import Semaphore
from settings import CRPC_ROOT

__lock = Semaphore(1)

exclude_crawlers = ['common', 'amazon', 'newegg', 'ecost', 'bhphotovideo', 'bestbuy', 'dickssport', 'overstock', 'cabelas']
# for auto-scheduler. bluefly, beyondtherack, nomorerack, zulily should better not be schedule together
luxury_crawlers = (
         'belleandclive',
         'ideeli',
         'bluefly',
         'ruelala',
         'gilt',
         'nomorerack',
         'venteprivee',
         'totsy',
         'beyondtherack',
         'lot18',
         'myhabit',
         'modnique',
#         'zulily',
         'onekingslane',
         'hautelook', )

deal_crawlers = (
    'nordstrom',
    '6pm',
    'ebags',
    'shopbop',
    'ashford',
    'macys',
    'bloomingdales',
    'saksfifthavenue',
)

picked_crawlers = tuple(set(luxury_crawlers) | set(deal_crawlers))

login_email = {'bluefly': '2012luxurygoods@gmail.com',
               'ideeli': '2012luxurygoods@gmail.com',
               'ruelala': '2012luxurygoods@gmail.com',
               'gilt': '2012luxurygoods@gmail.com',
               'nomorerack': '2012luxurygoods@gmail.com',
               'venteprivee': '2012luxurygoods@gmail.com',
               'totsy': '2012luxurygoods@gmail.com',
               'beyondtherack': '2012luxurygoods@gmail.com',
               'lot18': '2012luxurygoods@gmail.com',
               'myhabit': '2012luxurygoods@gmail.com',
               'belleandclive': '2012luxurygoods@gmail.com',
               'modnique': '2012luxurygoods@gmail.com',
#               'zulily': 'badbad@zulily.com',
               'onekingslane': '2012luxurygoods@gmail.com',
               'hautelook': '2012luxurygoods@gmail.com',
}

configFile = ConfigParser.ConfigParser()
def get_login_email(site):
    configFile.read( os.path.join(os.path.dirname(__file__), 'username.ini') )
    try:
        email = random.choice( [i.strip() for i in configFile.get('username', site).split(',')] )
    except ConfigParser.NoOptionError:
        return ''
    return email

login_passwd = 'abcd1234'

headers = { 
    'User-Agent': 'Mozilla 5.0/Firefox 16.0.1',
}
config = { 
    'max_retries': 5,
    'pool_connections': 10, 
    'pool_maxsize': 10, 
}

# this request_only should not be override or used in multiple crawler,
# because one crawler change its header or config, the other crawler will mess.
request_only = requests.Session(prefetch=True, timeout=30, config=config, headers=headers)


def get_ordinary_crawlers():
    """.. :py:method::
        get ordinary crawlers from directory of CRPC_ROOT/crawlers/
    """
    return [crawler for crawler in os.listdir( os.path.join(CRPC_ROOT, 'crawlers') ) \
        if crawler not in exclude_crawlers and os.path.isdir( os.path.join(CRPC_ROOT, 'crawlers', crawler) )]


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
        ret = request_only.get(url)
    except:
        # page not exist or timeout
        return

    if ret.ok: return ret.content
    else: return ret.status_code


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

def time_convert_std(time_str, time_format, timezone='PT'):
    """.. :py:method::

    :param time_str: u'2013 SAT OCT 20 9 AM'
    :param time_format: '%Y %a %b %d %I %p'
    :rtype: datetime type utc time
    """
    if timezone == 'PT' or timezone == 'PST' or timezone == 'PDT':
        pt = pytz.timezone('US/Pacific')
    elif timezone == 'ET' or timezone == 'EST' or timezone == 'EDT':
        pt = pytz.timezone('US/Eastern')

    endtime = pt.localize(datetime.strptime(time_str, time_format))
    return endtime.astimezone(pytz.utc)

