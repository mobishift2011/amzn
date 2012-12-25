#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()

from collections import defaultdict

from bottle import route, post, request, run, template, static_file, redirect, debug
from os.path import join, dirname

from backends.matching.models import Department, RawDocument
from backends.matching.classifier import SklearnClassifier

from datetime import datetime

import random
import json

clf = SklearnClassifier('svm')
clf.load_from_database()
sites = ['beyondtherack', 'bluefly', 'gilt', 'hautelook', 'ideeli', 'lot18', 'modnique', 'myhabit', 'nomorerack', 'onekingslane', 'ruelala', 'venteprivee', 'zulily']
#sites = ['venteprivee']

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

    if (not p.title) or (not p.list_info):
        print p.title
        return get_site_key()

    return site+'_'+p.key

def get_text(site_key):
    site, key = site_key.split('_', 1)
    m = get_site_module(site)
    p = m.Product.objects.get(key=key)
    try:
        depts = []
        depts.extend(p.dept)
        for eid in p.event_id:
            e = m.Event.objects.get(event_id=eid)
            depts.extend( e.dept )
            if hasattr(e, 'short_desc'):
                depts.append( e.short_desc )

        content = u'=s=i=t=e=: ' + site + u'\n'
        if depts:
            content += u'=d=e=p=t=s=: ' + u'; '.join(depts) + u'\n'
        if p.cats:
            content += u'=c=a=t=s=: ' +  u'; '.join(p.cats) + u'\n'
        if p.brand:
            content += u'=b=r=a=n=d=: ' + p.brand + u'\n'
        if p.tagline:
            content += u'=t=a=g=l=i=n=e=: ' + u'; '.join(p.tagline) + u'\n'
        content += u'=t=i=t=l=e=: ' +  p.title + u'\n'
        content += u'=l=i=s=t=i=n=f=o=: ' + u'\n'.join(p.list_info)
    except:
        import traceback
        traceback.print_exc()

    return p.combine_url, p.image_urls, content.replace('\n','<br />')

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
        url, image_urls, content = get_text(site_key)
    except:
        redirect('/')
    return template('teach', **locals())
    #site_key=site_key, url=url, departments=departments, departments_object=departments_object, content=content)

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
    site, key = site_key.split('_', 1)
    m = get_site_module(site)  
    departments = defaultdict(list)
    for d in Department.objects().order_by('main'):
        departments[d.main].append(d.sub)
    departments_object = json.dumps(departments)
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
    main = request.params['main']
    sub = request.params['sub']
    d = Department.objects(main=main,sub=sub).first()
    m = get_site_module(site)  
    if d:
        # here we use a tempory classifier to filter duplicates
        # some basic text was trained to be able to use "strict" option
        clftemp = SklearnClassifier('svm')
        clftemp.train('Some text', ('never_mind','c1'))
        clftemp.train('Some more text', ('never_mind','c2'))
        for p in m.Product.objects(event_id=key):
            __, ___, content = get_text(site+'_'+p.key)
            if clftemp.train(content, (main, sub), strict=True):
                clf.train(content, (main, sub))
                RawDocument.objects(site_key=site+'_'+p.key).update(set__department=d, set__content=content, upsert=True)
    else:
        print 'OOOOOPS', main, sub, 'doesnot seems like a department'
    return {'status':'ok'}
        

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
    url, image_urls, content = get_text(site_key)
    result = clf.classify(content)
    return template('validate', **locals())

@route('/cross-validation/')
def crossvalidation():
    return template('crossvalidation')

debug(True)

if __name__ == '__main__':
    run(server='gevent', host='0.0.0.0', port=1321, debug=True)
