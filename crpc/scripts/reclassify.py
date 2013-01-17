#!/usr/bin/env python
from backends.matching.feature import sites
from backends.matching.mechanic_classifier import classify_product_department, classify_event_department
from settings import MASTIFF_HOST
from datetime import datetime
from slumber import API
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
            print 'RECLASSIFY EVENT', site, e.event_id
            dept = []
            for p in m.Product.objects(event_id=e.event_id, updated=True):
                dept.extend(p.favbuy_dept)
            dept = list(set(dept))
            if e.favbuy_dept != dept:
                e.favbuy_dept = dept
                e.save()

def reclassify_mastiff():
    PAGESIZE = 100
    offset = 0
    total = 2**32
    while offset < total: 
        data = api.product.get(offset=offset, limit=PAGESIZE, order_by='updated_at')
        total = data['meta']['total_count']
        for p in data['objects']:
            print p
            break
        offset += PAGESIZE

reclassify_mastiff()
exit(1)

jobs = []
for site in sites:
    job = threading.Thread(target=outdate, args=(site,))
    job.start()
    jobs.append(job)

for j in jobs:
    j.join()

