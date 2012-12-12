#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()

from collections import defaultdict

from bottle import route, post, request, run, template, static_file, redirect, debug
from os.path import join, dirname

from backends.matching.models import Department, RawDocument
from backends.matching.classifier import SklearnClassifier

import random
import json

clf = SklearnClassifier('svm')
clf.load_from_database()
sites = ['myhabit', 'gilt', 'ruelala', 'hautelook', 'nomorerack', 'onekingslane', 'zulily']
def get_site_module(site):
    return __import__('crawlers.'+site+'.models', fromlist=['Category', 'Event', 'Product'])

def get_site_key():
    site = random.choice(sites)
    m = get_site_module(site)

    count = m.Product.objects().count()
    if count == 0:
        #sites.remove(site)
        return get_site_key()


    index = random.randint(1, count-1)
    p = m.Product.objects().skip(index).first()

    if (not p.list_info) or (not p.title):
        return get_site_key()

    return site+'_'+p.key

def get_text(site_key):
    site, key = site_key.split('_', 1)
    m = get_site_module(site)
    p = m.Product.objects.get(key=key)

    content = p.title + u'\n' + u'\n'.join(p.list_info)

    for fieldname in ['short_desc', 'summary', 'detail']:
        if getattr(p, fieldname):
            content += u'\n' + getattr(p, fieldname)

    return p.combine_url, content.replace('\n','<br />')

@route('/assets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=join(dirname(__file__), 'assets'))

@route('/')
def login():
   return template('index')

@route('/department/')
def department():
    departments = defaultdict(list)
    for d in Department.objects().order_by('main'):
        departments[d.main].append(d.sub)
    return template('department', departments=departments)

@route('/training-set/')
def trainingset():
    departments = defaultdict(list)
    ts = []
    for d in Department.objects().order_by('main'):
        departments[d.main].append(d.sub)
    for main, sublist in departments.items():
        for sub in sublist:
            d = Department.objects(main=main,sub=sub).first()
            ts.append([ main, sub, RawDocument.objects(department=d).count() ])
    return template('trainingset', ts=ts)

@route('/training-set/load-detail/')
def trainingset_loaddetail():
    main = request.query['main']
    sub = request.query['sub']
    d = Department.objects(main=main,sub=sub).first()
    j = []
    for rd in RawDocument.objects(department=d):
        try:
            site, key = rd.site_key.split('_', 1)
            m = get_site_module(site)
            p = m.Product.objects.get(key=key)
            url = p.combine_url
        except Exception, e:
            url = ''
        j.append({'content':rd.content,'site_key':rd.site_key,'url':url})
    return {'status':'ok','data':j}

@route('/teach/')
def teach():
    site_key = request.query.get('site_key')
    if not site_key:
        site_key = get_site_key()
        redirect('/teach/?site_key='+site_key)
    departments = defaultdict(list)
    for d in Department.objects().order_by('main'):
        departments[d.main].append(d.sub)
    departments_object = json.dumps(departments)
    try:
        url, content = get_text(site_key)
    except:
        redirect('/')
    return template('teach', **locals())
    #site_key=site_key, url=url, departments=departments, departments_object=departments_object, content=content)

@post('/teach/train/')
def teach_train():
    main = request.params['main']
    sub = request.params['sub']
    content = request.params['content']
    site_key = request.params['site_key']
    d = Department.objects(main=main,sub=sub).first()
    if d:
        clf.train(content, (main, sub))
        RawDocument.objects(site_key=site_key).update(set__department=d, set__content=content, upsert=True)
    else:
        print 'OOOOOPS', main, sub, 'doesnot seems like a department'
    return {'status':'ok'}

@route('/validate/')
def validate():
    site_key = get_site_key()
    url, content = get_text(site_key)
    result = clf.classify(content)
    return template('validate', **locals())

@route('/cross-validation/')
def crossvalidation():
    return template('crossvalidation')

debug(True)

run(server='gevent', host='0.0.0.0', port=1321, debug=True)
