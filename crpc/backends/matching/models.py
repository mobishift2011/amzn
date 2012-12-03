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
    text        =   StringField()
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

for k, vlist in CATS.iteritems():
    for v in vlist:
        print k, v
        Department.objects(main=k,sub=v).update(set__main=k, set__sub=v, upsert=True)
