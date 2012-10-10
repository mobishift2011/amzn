#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crawlers.newegg.models import Product as NeweggProduct

from models import Product, Session
from mongoengine import *


def the_cleanse_amazon(p):
    if not hasattr(the_cleanse_amazon, 'session'):
        setattr(the_cleanse_amazon, 'session', Session())
    session = the_cleanse_amazon.session
    duplicate = False
    if not session.query(Product).filter_by(site="amazon", key=p.asin).first():
        for dp in session.query(Product).filter_by(model=p.model.encode('utf-8')):
            duplicate = True
            dp.duplicate = True
            session.add(dp)
        if not p.price:
            p.price = 0
        gp = Product(model=p.model.encode('utf-8'), title=p.title, site="amazon", key=p.asin, price=float(p.price), duplicate=duplicate)
        session.add(gp)
        session.commit()

def cleanse_amazon():
    from crawlers.amazon.models import Product as AmazonProduct
    connect(db='amazon')
    counter = 12210000
    for p in AmazonProduct.objects().order_by('full_update_time').skip(counter).timeout(False):
        counter += 1
        if counter % 1000 == 0:
            print counter
        if p.model:
            the_cleanse_amazon(p)
            #pool.apply_async(the_cleanse_amazon, args=(p,))

cleanse_amazon()
