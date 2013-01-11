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
        print '{0}.{1} | {2} | {3} | {4} |\t {5} | {6} | {7} | {8} |'.format(
                site, obj['method'], obj['status'], obj['started_at'].isoformat()[:-7],
                obj['ended_at'].isoformat()[:-7], obj['num_finish'], obj['num_update'],
                obj['num_new'], obj['num_fails'])

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for site in sys.argv[1:]:
            get_all_task(site)
    else:
        for site in picked_crawlers:
            get_all_task(site)
            print('\n\n')
