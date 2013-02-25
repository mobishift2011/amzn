#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import pymongo
from settings import MONGODB_HOST
from crawlers.common.stash import picked_crawlers

conn = pymongo.Connection(MONGODB_HOST)
for site in picked_crawlers:
    print 'site:\n'
    col = conn[site].collection_names()
    if 'event' in col:
        ev = conn[site].event.find({'product_ids': {'$exists': False}}, fields=['event_id', 'combine_url'])
        for e in ev:
            print e['event_id'], e['combine_url']

