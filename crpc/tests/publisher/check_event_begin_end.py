#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import pymongo
import collections
from settings import MONGODB_HOST
from crawlers.common.stash import picked_crawlers

conn = pymongo.Connection(MONGODB_HOST)
conn_m = pymongo.Connection(MASTIFF_HOST.split(':')[1].replace('//'))

data=collections.defaultdict(dict)

for site in picked_crawlers:
    col = conn[site].collection_names()
    if 'event' in col:
        if site not in data: data[site] = {}
        ev = conn[site].event.find({}, fields=['event_id', 'events_begin', 'events_end'])
        for e in ev:
            data[site][e['event_id']] = [e['events_begin'], e['events_end']]

ev = conn_m.event.find({}, fields=['site_key', 'starts_at', 'ends_at'])
for e in ev:
    site, key = e['site_key'].split('_')
    if data[site][key][0] != e['starts_at']:
        print site, key
    if data[site][key][1] != e['ends_at']:
        print site, key
