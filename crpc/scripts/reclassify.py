#!/usr/bin/env python
from backends.matching.feature import sites
from backends.matching.mechanic_classifier import classify_product_department, classify_event_department
from settings import MASTIFF_HOST
from datetime import datetime
from slumber import API
from collections import Counter
import requests
import threading
import json
api = API(MASTIFF_HOST)

def get_site_module(site):
    return __import__('crawlers.'+site+'.models', fromlist=['Category', 'Event', 'Product'])

def reclassify(site='beyondtherack'):
    utcnow = datetime.utcnow()
    m = get_site_module(site)
    for p in m.Product.objects(updated=True):
        dept = classify_product_department(site, p)
        if p.favbuy_dept != dept:
            p.favbuy_dept = dept
            p.save()
            print 'RECLASSIFY PRODUCT', site, p.key, p.favbuy_dept
    if hasattr(m, 'Event'):
        for e in m.Event.objects():
            print 'RECLASSIFY EVENT', site, e.event_id, 
            dept = []
            counter = Counter()
            total = 0
            for p in m.Product.objects(event_id=e.event_id, updated=True):
                counter[tuple(p.favbuy_dept)] += 1
                total += 1
            threshold = int(total*0.1)
            for thedept, count in counter.items():
                if count > threshold:
                    dept.extend(list(thedept))
            dept = list(set(dept))
            print dept
            if e.favbuy_dept != dept:
                e.favbuy_dept = dept
                e.save()

def reclassify_mastiff():
    # EVENTS
    PAGESIZE = 20
    offset = 0
    total = 2**32
    while offset < total:
        data = api.event.get(offset=offset, limit=PAGESIZE)
        for e in data['objects']:
            site_key = e['site_key']
            site, key = site_key.split('_',1)
            m = get_site_module(site)
            try:
                e2 = m.Event.objects.get(event_id=key)
            except:
                print 'EVENT', site, key, 'NOT FOUND' 
            else:
                if e2.favbuy_dept != e['departments']:
                    print 'PATCH EVENT', site, key, e['title'], e2.favbuy_dept
                    api.event(e['id']).patch({'departments':e2.favbuy_dept})
        total = data['meta']['total_count']
        offset += PAGESIZE

    # PRODUCTS
    PAGESIZE = 20
    offset = 0
    total = 2**32
    while offset < total: 
        data = api.product.get(offset=offset, limit=PAGESIZE, order_by='updated_at')
        for p in data['objects']:
            site_key = p['site_key']
            site, key = site_key.split('_',1)
            m = get_site_module(site)
            try:
                p2 = m.Product.objects.get(pk=key)
            except:
                print 'PRODUCT', site, key, 'NOT FOUND'
            else: 
                dept = classify_product_department(site, p2)
                if p['department_path'] != dept:
                    print 'PATCH PRODUCT', site, key, p['title'], dept
                    api.product(p['id']).patch({'department_path':dept})
        total = data['meta']['total_count']
        offset += PAGESIZE
    
jobs = []
for site in sites:
    job = threading.Thread(target=reclassify, args=(site,))
    job.start()
    jobs.append(job)

for j in jobs:
    j.join()

reclassify_mastiff()
