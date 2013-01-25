#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import collections
import subprocess
import pymongo
from datetime import datetime, timedelta
from settings import MONGODB_HOST
from backends.monitor.upcoming_ending_events_count import upcoming_events
from crawlers.common.stash import picked_crawlers

ganglia_host = ('mongodb.favbuy.org',
                'integrate.favbuy.org',
                'ec2-54-245-154-123.us-west-2.compute.amazonaws.com',
                'ec2-50-112-65-243.us-west-2.compute.amazonaws.com',
                'ec2-54-245-150-181.us-west-2.compute.amazonaws.com',
                'ec2-54-245-22-46.us-west-2.compute.amazonaws.com', )

# These crawlers don't have upcoming events now
except_crawler = ('bluefly',
                  'belleandclive',
                  'ideeli',
                  'nomorerack',
                  'lot18',
                  'zulily', )

def ganglia_alarm():
    """..:py:method::
    """
    for host in ganglia_host:
        ret = subprocess.Popen('telnet {0} 8649'.format(host), shell=True, stdout=subprocess.PIPE).communicate()[0]
        if len(ret) < 1000:
            alarm("Host[{0}] don't have ganglia data.".format(host))

def crawler_upcoming_alarm():
    """..:py:method::
    """
    data = collections.defaultdict(dict)
    upcoming_events(data)
    for crawler in picked_crawlers:
        if crawler not in except_crawler and crawler not in data['upcoming']:
            alarm("crawler[{0}] don't have upcoming events now.".format(crawler))

def crawl_error_alarm():
    """..:py:method::
    """
    _utcnow = datetime.utcnow()
    fail_col = pymongo.Connection(MONGODB_HOST)['monitor']['fail']
    for info in fail_col.find({'time': {'$gte': _utcnow - timedelta(seconds=3600)}}, fields=['site', 'method', 'time', 'message']):
        if '404' not in info['message'] and '-302' not in info['message'] and 'redirect to home' not in info['message']:
            alarm("{0}.{1}.[{2}]: {3}".format(info['site'], info['method'], info['time'], info['message']))

def alarm(message):
    print message

if __name__ == '__main__':
    import time
    while True:
        ganglia_alarm()
        crawler_upcoming_alarm()
        crawl_error_alarm()
        time.sleep(60*15)
