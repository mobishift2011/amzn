#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import pymongo
import collections
from datetime import datetime
from settings import MONGODB_HOST
from crawlers.common.stash import picked_crawlers

connection = pymongo.Connection(MONGODB_HOST)

def upcoming_events(data=collections.defaultdict(dict)):
    if 'upcoming' not in data: data['upcoming'] = {}
    dbs = connection.database_names()
    for crawler in picked_crawlers:
        if crawler in dbs:
            col = connection[crawler].collection_names()
            if 'event' in col:
                if crawler not in data['upcoming']: data['upcoming'][crawler] = {}
                upcoming = connection[crawler].event.find({'events_begin': {'$gte': datetime.utcnow()}}, fields=['events_begin'])
                for e in upcoming:
                    if e['events_begin'] not in data['upcoming'][crawler]:
                        data['upcoming'][crawler][e['events_begin']] = 1
                    else:
                        data['upcoming'][crawler][e['events_begin']] += 1
    return data['upcoming']

def ending_events(data=collections.defaultdict(dict)):
    if 'ending' not in data: data['ending'] = {}
    dbs = connection.database_names()
    for crawler in picked_crawlers:
        if crawler in dbs:
            col = connection[crawler].collection_names()
            if 'event' in col:
                if crawler not in data['ending']: data['ending'][crawler] = {}
                ending = connection[crawler].event.find({'events_end': {'$gte': datetime.utcnow()}}, fields=['events_end'])
                for e in ending:
                    if e['events_end'] not in data['ending'][crawler]:
                        data['ending'][crawler][e['events_end']] = 1
                    else:
                        data['ending'][crawler][e['events_end']] += 1
    return data['ending']

if __name__ == '__main__':
    data = collections.defaultdict(dict)
    up = upcoming_events(data)
    ed = ending_events(data)
    import pprint
    print '\nUpcoming:'
    pprint.pprint( data['upcoming'] )
    print '\nEnding soon:'
    pprint.pprint( data['ending'] )
