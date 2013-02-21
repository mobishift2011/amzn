#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import json
import requests
import pymongo
import collections
from datetime import datetime
from settings import MONGODB_HOST, MASTIFF_HOST
from crawlers.common.stash import picked_crawlers

conn = pymongo.Connection(MONGODB_HOST)
conn_m = pymongo.Connection(MASTIFF_HOST.split(':')[1].replace('//', ''))

def obsolete():
    event_url = 'http://www.favbuy.com/api/v1/event/?title__iexact='
    product_url = 'http://www.favbuy.com/api/v1/product/?title__iexact='

    js = json.loads( requests.get(event_url) )
    for ev in js['objects']:
        site, event_id = ev['site_key'].split('_')
        env = conn[site]['event'].find_one({'event_id': event_id})
        env.update_history.update({ 'sale_title': datetime.utcnow() })
        env.save()

def repair_event_sale_title():
    ev = conn_m.mastiff.event.find({'title': ''}, fields=['site_key'])
    for e in ev:
        site, key = e['site_key'].split('_')
        conn[site].event.update({'event_id': key}, {'$set': {'update_history.sale_title': datetime.utcnow()} })

if __name__ == '__main__':
    repair_event_sale_title()
