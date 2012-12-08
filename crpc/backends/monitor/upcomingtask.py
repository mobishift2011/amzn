#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import os
import pymongo
from datetime import datetime
import collections

from settings import MONGODB_HOST, CRPC_ROOT
from crawlers.common.stash import exclude_crawlers

cset = collections.defaultdict(set)
conn = pymongo.Connection(host=MONGODB_HOST)
dbs = conn.database_names()

for crawler_name in os.listdir( os.path.join(CRPC_ROOT, 'crawlers') ):
    path = os.path.join(CRPC_ROOT, 'crawlers', crawler_name)
    if crawler_name not in exclude_crawlers and crawler_name in dbs and os.path.isdir(path):
        collections = conn.crawler_name.collection_names()
        if 'event' in collections:
            upcoming_events = conn.crawler_name.event.find({'events_begin': {'$gte': datetime.utcnow()}}, fields=['events_begin'])
            events_begin = set( [e['events_begin'] for e in upcoming_events] )
            for begin in events_begin:
                cset[begin].add('{0}.new'.format(crawler_name))
