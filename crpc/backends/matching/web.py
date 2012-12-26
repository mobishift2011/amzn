#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()

from collections import defaultdict

from bottle import route, post, request, run, template, static_file, redirect, debug
from os.path import join, dirname

from backends.matching.models import RawDocument, D0, D1, D2DICT
from backends.matching.classifier import FavbuyClassifier

from datetime import datetime
from collections import Counter

import random
import json

clf = FavbuyClassifier()
clf.load_from_database()

from feature import *

@route('/assets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=join(dirname(__file__), 'assets'))

@route('/')
def login():
   return template('index')

@route('/department/')
def department():
    d0, d1, d2dict = D0, D1, D2DICT
    return template('department', **locals())

@route('/training-set/')
def trainingset():
    d0, d1, d2dict = D0, D1, D2DICT
    dc = Counter()
    for doc in RawDocument.objects():
        dc[(doc.d0, doc.d1, doc.d2)] += 1
    return template('trainingset', **locals())

@route('/training-set/load-detail/')
def trainingset_loaddetail():
    d0 = request.query['d0']
    d1 = request.query['d1']
    d2 = request.query['d2']
    j = []
    for rd in RawDocument.objects(d0=d0,d1=d1,d2=d2):
        site, key = rd.site_key.split('_', 1)
        m = get_site_module(site)
        p = m.Product.objects.get(key=key)
        url = p.combine_url
        j.append({'content':rd.content,'site_key':rd.site_key,'url':url})
    return {'status':'ok','data':j}

@route('/teach/')
def teach():
    d0, d1, d2dict = D0, D1, D2DICT
    d2dict_json = json.dumps(d2dict)
    site_key = request.query.get('site_key')
    if not site_key:
        site_key = get_site_key()
        redirect('/teach/?site_key='+site_key)
    url, image_urls, content = get_text(site_key)
    return template('teach', **locals())

@route('/event/list/')
def event_list():
    now = datetime.utcnow()
    sk = {}
    for site in sites:
        m = get_site_module(site)
        if hasattr(m, 'Event'):
            results = []
            for e in m.Event.objects().only('event_id','image_urls'):
                results.append((e.event_id, e.image_urls[0] if e.image_urls else u''))
            sk[site] = results
    return template('event_list', **locals())

@route('/event/:site_key/')
def event_detail(site_key):
    d0, d1, d2dict = D0, D1, D2DICT
    site, key = site_key.split('_', 1)
    m = get_site_module(site)  
    products = m.Product.objects(event_id=key)
    results = []
    for p in products:
        __, ___, content = get_text(site+'_'+p.key)
        results.append( clf.classify(content) )
    return template('event_detail', **locals())

@post('/event/train/')
def event_train():
    site = request.params['site']
    key = request.params['key']
    d0 = request.params['d0']
    d1 = request.params['d1']
    d2 = request.params['d2']
    m = get_site_module(site)  
        
    for p in m.Product.objects(event_id=key):
        __, ___, content = get_text(site+'_'+p.key)
        clf.train(content, (d0, d1, d2))
        RawDocument.objects(site_key=site+'_'+p.key).update(set__d0=d0, set__d1=d1, set__d2=d2, set__content=content, upsert=True)
    return {'status':'ok'}
        

@post('/teach/train/')
def teach_train():
    d0 = request.params['d0']
    d1 = request.params['d1']
    d2 = request.params['d2']
    content = request.params['content']
    site_key = request.params['site_key']
    clf.train(content, (d0, d1, d2))
    RawDocument.objects(site_key=site_key).update(set__d0=d0, set__d1=d1, set__d2=d2, set__content=content, upsert=True)
    return {'status':'ok'}

@route('/validate/')
def validate():
    site_key = get_site_key()
    url, image_urls, content = get_text(site_key)
    result = clf.classify(content)
    return template('validate', **locals())

@route('/cross-validation/')
def crossvalidation():
    return template('crossvalidation')

debug(True)

if __name__ == '__main__':
    run(server='gevent', host='0.0.0.0', port=1321, debug=True)
