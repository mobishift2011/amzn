#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import pymongo
from datetime import datetime
from settings import MONGODB_HOST

client = pymongo.MongoClient()
DB = ['gilt', 'ruelala', 'modnique', 'beyondtherack']

for site in DB:
    client[site].event.update({'create_time': {'$lt': datetime(2013,4,1)}, 'update_history.events_end': {'$exists': False}}, {'$set': {'update_history.events_end': datetime(2013,5,1)}}, multi=True)
