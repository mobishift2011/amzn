#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mongoengine import *
connect('training')

class Department(Document):
    main    =   StringField()
    sub     =   StringField()
    parent  =   ReferenceField('Department')

    meta    = {
        'indexes': [
            {'fields':['main','sub'], 'unique':True},
        ],
    }
    
class RawDocument(Document):
    site_key    =   StringField()   
    content     =   StringField()
    department  =   ReferenceField(Department)
    
    meta = {
        'indexes': [
            {'fields':['site_key'], 'unique':True, 'sparse':True}, 
        ],
    }


CATS = {
    'Women': [
	    'Shoes',
	    'Accessories',
	    'Dresses & Skirts',
	    'Pants & Shorts',
	    'Shirts & Sweaters',
	    'Outerwear',
	    'Intimates & Loungewear',
    ],
    'Men': [
	    'Shoes',
	    'Accessories',
	    'Suits & Coats',
	    'Shirts & Sweaters',
	    'Polos & Tees',
	    'Pants',
	    'Outerwear',
	    'Socks, Underwear & Sleepwear',
    ],
    'Kids & Baby': [
	    'Girls\' Shoes',
	    'Girls\' Clothing',
	    'Boys\' Shoes',
	    'Boys\' Clothing',
	    'Toys, Games & Books',
	    'Gear & Equipment',
	    'Bed, Bath & Furniture',
    ],
    'Home': [
	    'Furniture & Lighting',
	    'Bed & Bath',
	    'Rugs & Textiles',
	    'Home Accessories',
	    'Electronics',
	    'Tools',
	    'Kitchen & Dining',
    ],
    'Handbags': [
	    'Shoulder Bags',
	    'Tote Bags',
	    'Satchels',
	    'Clutches',
	    'Hobo Bags',
	    'Crossbody Bags',
	    'Evening Bags',
	    'Backpacks & Laptop Bags',
    ],
    'Jewelry & Watches': [
	    'Women\'s Watches',
	    'Men\'s Watches',
	    'Bracelets',
	    'Earrings',
	    'Necklaces',
	    'Rings',
	    'Pendants',
    ],
    'Beauty & Health': [
	    'Skin Care',
	    'Makeup',
	    'Fragrance',
	    'Body Care',
    ],
    'Wine': [
	    'Red Wine',
	    'White Wine',
	    'Champagne',
	    'Wine Accessories',
    ],
}

def bootstrap():
    print 'reconstructing categories'
    for k, vlist in CATS.iteritems():
        for v in vlist:
            print k, v
            Department.objects(main=k,sub=v).update(set__main=k, set__sub=v, upsert=True)
    # Department.objects(main='Beauty & Health').update(set__parent='Women')
    # Department.objects(main='Jewelry & Watches').update(set__parent='Women')
    # Department.objects(main='Handbags').update(set__parent='Women')

    print
    print 'constructing rawdocs'
    import os
    from os.path import join
    from classifier import SklearnClassifier
    clf = SklearnClassifier('svm')
    for dept_subdept in os.listdir('dataset'):
        dept, subdept = dept_subdept.split('|')
        print dept, subdept
        d = Department.objects.get(main=dept, sub=subdept)
        for site_key in os.listdir(join('dataset',dept_subdept)):
            content = open(join('dataset', dept_subdept, site_key)).read()
            if clf.train(content, dept_subdept):
                RawDocument.objects(site_key=site_key).update(set__content=content, set__department=d, upsert=True)
            else:
                print 'duplicate document', site_key

if __name__ == '__main__':
    bootstrap()
