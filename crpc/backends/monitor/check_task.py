#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import sys
import pymongo
from settings import MONGODB_HOST
from crawlers.common.stash import picked_crawlers

conn = pymongo.Connection(MONGODB_HOST)
task = conn['monitor']['task']


def get_all_task(site):
    for obj in task.find({'site': site}, fields=['method', 'status', 'started_at', 'updated_at', 'ended_at', 'num_finish', 'num_update', 'num_new', 'num_fails']).sort('started_at', pymongo.DESCENDING):
        print site, obj['method'], obj['status']

if __name__ == '__main__':
    if sys.argv[1]:
        get_all_task(sys.argv[1])
    else:
        for site in picked_crawlers:
            get_all_task(site)
            print('\n\n')
