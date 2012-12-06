#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import pymongo
import json
import cPickle

c = pymongo.Connection()
col = c['hautelook']['product']

def load_product():
    data = {}
    for i in col.find({}, fields=['scarcity'], timeout=False).sort("_id", pymongo.DESCENDING):
        data[i['_id']] = i['scarcity']
    return data

def dump():
    data = load_product()
    fd = open('scarcity_hautelook.15.40.txt', 'w')
    cPickle.dump(data, fd)

def load():
    fd = open('scarcity_hautelook.2012.12.6.15.35.txt', 'r')
    d = cPickle.load(fd)
    return d

if __name__ == '__main__':
    before_data = load()
    now_data = load_product()

    total = 0
    for _id, scarcity in now_data.iteritems():
        if _id in before_data:
            if scarcity != before_data[_id]:
                total += 1
    print total
