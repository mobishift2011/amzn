#!/usr/bin/env python
# -*- coding: utf-8

CREDENTIALS = [
    ('kwtools3457@gmail.com','1qaz2wsx!@'),
    ('kwtools3458@gmail.com','1qaz2wsx!@'),
    ('kwtools3459@gmail.com','1qaz2wsx!@'),
    ('kwtools3460@gmail.com','1qaz2wsx!@'),
    ('kwtools3461@gmail.com','1qaz2wsx!@'),
    ('kwtools3462@gmail.com','1qaz2wsx!@'),
    ('kwtools3463@gmail.com','1qaz2wsx!@'),
    ('kwtools3464@gmail.com','1qaz2wsx!@'),
]

import os, sys
PATH = os.path.dirname(os.path.abspath(__file__))

from sh import casperjs

casperjs_with_proxy = casperjs.bake(proxy='199.19.110.124:1238')

import simplejson as json
import random
    
from models import Model, Session
from datetime import datetime, timedelta

from kwt import KeywordSearch
import threading

def getvolume(keywords, email=None, passwd=None):
    """ get keyword volume info
    
    :param keywords: a list of keywords
    :rtype: a dictionary like this: {'kw1':[120,10], 'kw2':[200,30]}
            the value tuple represents global volume and local volume
    
    Usage:

    >>> print getvolume(["hp", "samsung", "apple"])
    {'hp': ['101,000,000', '16,600,000'], 'apple': ['83,100,000', '30,400,000'], 'samsung': ['185,000,000', '16,600,000']} 

    """
    if not email:
        email, passwd = random.choice(CREDENTIALS)

    print email
    kw = ','.join(keywords)
    data = casperjs(os.path.join(PATH,'kwt.js'), email = email, passwd = passwd, keywords = kw)
    print data.ran
    return json.loads(data.stdout)

def volume2int(volume):
    if volume.startswith('<'):
        volume = volume[2:]
    volume = volume.replace(',', '')
    try:
        return int(volume)
    except:
        return 0

def normalizemodel(model):
    if model.startswith('-'):
        return model[1:]
    else:
        return model

def update_volume():
    blocksize = 50
    concurrency = 1 #len(CREDENTIALS)
    
    count = 0
    while True:
        count += 1
        print 'looping...', count
        session = Session()
        OFFSET = random.randint(100, 10000)
        models = (m.model.lower() for m in session.query(Model).filter(Model.global_volume == None).offset(OFFSET).limit(blocksize*concurrency))
        if not models:
            break

        models = [ normalizemodel(m) for m in models ]

        update_volume_with_email_passwd(models)

        session.close()

def update_volume_with_email_passwd(models, email=None, passwd=None):
    session = Session()
    #kwdict = getvolume(models, email, passwd)
    if not hasattr(update_volume_with_email_passwd, 'ks'):
        setattr(update_volume_with_email_passwd, 'ks', KeywordSearch())
    ks = update_volume_with_email_passwd.ks
    kwdict = ks.search(models)

    for k, v in kwdict.items():
        print k, v
        m = session.query(Model).filter_by(model=k).first()
        if m:
            m.global_volume = volume2int(v[0])
            m.local_volume = volume2int(v[1])
            m.updated_at = datetime.utcnow()
            session.add(m)

    session.commit()
    session.close()
    sleep = 3
    while sleep>0:
        import time
        print 'sleeping', sleep
        time.sleep(1)
        sleep -= 1

if __name__ == "__main__":
    update_volume()
    #for email, passwd in CREDENTIALS:
    #    print getvolume(["t1", "t2", "t3"], email, passwd)
