#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import pymongo
import collections
from datetime import datetime
from settings import MONGODB_HOST
from crawlers.common.stash import picked_crawlers

connection = pymongo.Connection(MONGODB_HOST)

def upcoming_events(data=collections.defautldict(dict)):
    if 'upcoming' not in data: data['upcoming']
    dbs = connection.database_names()
    for crawler in picked_crawlers:
        if crawler in dbs:
            col = connection[crawler].collection_names()
            if 'event' in col:
                if crawler not in data['upcoming']: data['upcoming'][crawler] = {}
                upcoming = connections[crawler].event.find({'events_begin': {'$gte': datetime.utcnow()}}, fields=['events_begin'])
                for e in upcoming:
                    if e['events_begin'] not in data['upcoming'][crawler]:
                        data['upcoming'][crawler][e['events_begin']] = 0
                    else:
                        data['upcoming'][crawler][e['events_begin']] += 1

def ending_events(data=collections.defautldict(dict)):
    if 'ending' not in data: data['ending']
    dbs = connection.database_names()
    for crawler in picked_crawlers:
        if crawler in dbs:
            col = connection[crawler].collection_names()
            if 'event' in col:
                if crawler not in data['ending']: data['ending'][crawler] = {}
                ending = connections[crawler].event.find({'events_end': {'$gte': datetime.utcnow()}}, fields=['events_end'])
                for e in ending:
                    if e['events_end'] not in data['ending'][crawler]:
                        data['ending'][crawler][e['events_end']] = 0
                    else:
                        data['ending'][crawler][e['events_end']] += 1

if __name__ == '__main__':
    data = collections.defautldict(dict)
    upcoming_events(data)
    ending_events(data)
    print data
