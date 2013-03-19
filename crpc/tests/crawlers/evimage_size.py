#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import requests
import pymongo
import itertools
from datetime import datetime
from PIL import Image
from cStringIO import StringIO
from collections import Counter

from settings import MONGODB_HOST
from crawlers.common.stash import picked_crawlers

conn = pymongo.Connection(MONGODB_HOST)

def statistics_image_size():
    for site in picked_crawlers:
        print 'site: {0}\n'.format(site)
        utcnow = datetime.utcnow()
        cnt = Counter()
        col = conn[site].collection_names()
        if 'event' in col:
            ev = conn[site].event.find({'events_begin': {'$gt': utcnow}, 'image_urls': {'$exists': True}}, fields=['image_urls'])
            ev2 = conn[site].event.find({'events_begin': {'$lt': utcnow}, 'events_end': {'$gt': utcnow}, 'image_urls': {'$exists': True}}, fields=['image_urls'])
            for e in itertools.chain(ev, ev2):
                for img in e['image_urls']:
                    size = download_img(img)
                    if size:
                        cnt[size] += 1
            print cnt


def download_img(img_url):
    r = requests.get(img_url)
    # the site response a 200 html page to indicate the error.
    if 'text/html' in r.headers.get('Content-Type', ''):
        return
    cs = StringIO(r.content)
    img = Image.open(cs)

    return img.size

def get_proportion(tupsize):
    proportion = tupsize[0]*1.0 / tupsize[1]
    return proportion


if __name__ == "__main__":
    statistics_image_size()
