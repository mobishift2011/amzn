#!/usr/bin/env python
from gevent import monkey; monkey.patch_all()
import gevent
import gevent.pool

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

def patch_mastiff_product(offset, pagesize):
    try:
        data = api.product.get(offset=offset, limit=pagesize)
    except:
        print 'OFFSET', offset
        raise
        
    total = data['meta']['total_count']
    offset += pagesize
       
    _patch_mastiff_product(data) 
    return offset, total

def _patch_mastiff_product(data):
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

def patch_mastiff_event(data):
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

def reclassify_mastiff():
    pool = gevent.pool.Pool(30)

    # EVENTS
    PAGESIZE = 20
    offset = 0
    total = 2**32
    while offset < total:
        print 'EVENT OFFSET', offset, 'OF', total
        data = api.event.get(offset=offset, limit=PAGESIZE)
        total = data['meta']['total_count']
        offset += PAGESIZE
        pool.spawn(patch_mastiff_event, data)

    # PRODUCTS
    PAGESIZE = 20
    offset = 0
    total = api.product.get(offset=offset, limit=1)['meta']['total_count']
    while offset < total: 
        print "PRODUCT OFFSET", offset, 'OF', total
        pool.spawn(patch_mastiff_product, offset, PAGESIZE) 
        offset += PAGESIZE

    pool.join()
    
def reclassify_mongodb():
    jobs = []
    for site in sites:
        job = threading.Thread(target=reclassify, args=(site,))
        job.start()
        jobs.append(job)

    for j in jobs:
        j.join()

reclassify_mongodb()
reclassify_mastiff()
