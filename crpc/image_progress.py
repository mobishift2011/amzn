#!/usr/bin/env python
# -*- coding : utf-8 -*-
sites = ['gilt','hautelook','myhabit','bluefly','ideeli', 'beyondtherack','onekingslane','zulily','venteprivee','nomorerack']

def get_site_module(site):
    return __import__('crawlers.'+site+'.models', fromlist=['Category', 'Event', 'Product'])


def get_counts():
    count = 0
    for site in sites:
        m = get_site_module(site)
        count += m.Product.objects(image_path__exists=True).count()
        if hasattr(m, 'Event'):
            count += m.Event.objects(image_path__exists=True).count()
    return count

import time

base = get_counts()
t1 = time.time()
while True:
    counts = get_counts()
    time.sleep(1)
    print counts, (counts-base)/(time.time()-t1)
