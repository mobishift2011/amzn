#!/usr/bin/env python
# -*- coding: utf-8

CREDENTIALS = [
    ('kwtools3456@gmail.com','1qaz2wsx!@'),
    ('kwtools3457@gmail.com','1qaz2wsx!@'),
    ('kwtools3458@gmail.com','1qaz2wsx!@'),
]

import os, sys
PATH = os.path.dirname(os.path.abspath(__file__))

from sh import casperjs
import simplejson as json
import random
    
from models import Model, Session
from datetime import datetime, timedelta

def getvolume(keywords):
    """ get keyword volume info
    
    :param keywords: a list of keywords
    :rtype: a dictionary like this: {'kw1':[120,10], 'kw2':[200,30]}
            the value tuple represents global volume and local volume
    
    Usage:

    >>> print getvolume(["hp", "samsung", "apple"])
    {'hp': ['101,000,000', '16,600,000'], 'apple': ['83,100,000', '30,400,000'], 'samsung': ['185,000,000', '16,600,000']} 

    """
    email, passwd = random.choice(CREDENTIALS)
    kw = ','.join(keywords)
    data = casperjs(os.path.join(PATH,'kwt.js'), email = email, passwd = passwd, keywords = kw)
    return json.loads(data.stdout)


def update_volume():
    session = Session()
    models = (m.model for m in session.query(Model).filter(Model.global_volume == None).limit(499))

    models = list(models)
    print models

    for k, v in getvolume(models):
        print k, v
        m = session.query(Model).filter_by(model=k).first()
        m.global_volume, m.local_volume = v
        session.add(m)

    session.commit()
    

if __name__ == "__main__":
    update_volume()
