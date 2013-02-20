#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import pymongo
import collections
from settings import MONGODB_HOST
from crawlers.common.stash import picked_crawlers

conn = pymongo.Connection(MONGODB_HOST)
conn_m = pymongo.Connection(MASTIFF_HOST.split(':')[1].replace('//'))


def check_events_begin_end(data=collections.defaultdict(dict)):
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
            print 'events_begin error: {0}, {1}'.format(site, key)
        if data[site][key][1] != e['ends_at']:
            print 'events_end error: {0}, {1}'.format(site, key)

def sync_time_mastiff_to_mongodb(data=collections.defaultdict(dict)):
    ev = conn_m.event.find({}, fields=['site_key', 'starts_at', 'ends_at'])
    for e in ev:
        site, key = e['site_key'].split('_')
        if site not in data: data[site] = {}
        data[site][key] = [e['starts_at'], e['ends_at']]

    for site in picked_crawlers:
        col = conn[site].collection_names()
        if 'event' in col:
            ev = conn[site].event.find({}, fields=['event_id', 'events_begin', 'events_end'])
            for e in ev:
                e['events_begin'] = data[site][e['event_id']][0]
                e['events_end'] = data[site][e['event_id']][1]
                conn[site].event.save(e)


if __name__ == '__main__':
    check_events_begin_end()
