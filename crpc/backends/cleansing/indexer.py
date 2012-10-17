#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymongo
import MySQLdb
from binascii import crc32

def site2id(sitename):
    return crc32(sitename) & 0xffffffff

SITES = {
    'amazon': {'pk':'_id'},
    #'bestbuy': {'pk':'sku'},
    #'newegg': {'pk':'_id'},
    #'cabelas':{'pk':'itemID'},
    #'ecost':{'pk':'ecost'},
    #'bhphotovideo':{'pk':'bah'},
}

from models import Product, Session

session = Session()

for site, info in SITES.items():
    mdb = getattr(pymongo.Connection(), site)
    pkname = SITES[site]['pk']
    siteid = site2id(site)
    for d in mdb.product.find():
        model = d.get('model')
        title = d.get('title')
        key = d.get(pkname)

        if model and key:
            print site, model, key

            p = session.query(Product).filter_by(site=site, key=key).first()
            isnew = False
            if not p:
                isnew = True
                p = Product()

            p.model = model.encode('utf-8')
            if title:
                p.title = title.encode('utf-8')
            p.key = key.encode('utf-8')
            p.site = site

            if isnew:
                session.add(p)

            session.commit()
