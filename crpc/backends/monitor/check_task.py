#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import sys
import time
import pymongo
from settings import MONGODB_HOST
from crawlers.common.stash import picked_crawlers

conn = pymongo.Connection(MONGODB_HOST)
task = conn['monitor']['task']


def get_all_task(site):
    with open('{0}_{1}.html'.format(site, int(time.time())), 'w') as fd:
        fd.write('<html><body>\n<table border="1" bordercolor="#000000" cellspacing="0" style="border-collapse:collapse">\n')
        fd.write('<thead><tr>\n<th>Task</th>\n<th>Status</th>\n<th>Started At</th>\n<th>Ended At</th>\n<th>Dones</th>\n<th>Updates</th>\n<th>News</th>\n<th>Fails</th>\n</tr></thread>\n<tbody>')

        for obj in task.find({'site': site}, fields=['method', 'status', 'started_at', 'updated_at', 'ended_at', 'num_finish', 'num_update', 'num_new', 'num_fails']).sort('started_at', pymongo.DESCENDING):
            fd.write('<tr>\n<td>{0}.{1}</td>\n<td>{2}</td>\n<td>{3}</td>\n<td>{4}</td>\n<td align="right">{5}</td>\n<td align="right">{6}</td>\n<td align="right">{7}</td>\n<td align="right">{8}</td>\n</tr>'.format(
                    site, obj['method'], obj['status'], obj['started_at'].isoformat()[:-7],
                    obj['ended_at'].isoformat()[:-7], obj['num_finish'], obj['num_update'],
                    obj['num_new'], obj['num_fails']
                    ))

        fd.write('\n</tbody>\n</table>\n</body></html>')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for site in sys.argv[1:]:
            get_all_task(site)
    else:
        for site in picked_crawlers:
            get_all_task(site)
            print('\n\n')
