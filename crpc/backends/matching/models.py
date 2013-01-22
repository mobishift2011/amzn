#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import MONGODB_HOST
from mongoengine import *
connect(db='training', alias='training', host=MONGODB_HOST)

from datetime import datetime

D0 = ["Men","Women","Adult","Home","Boys","Girls","Kids","Baby","Human"]
D1 = ["Books","Electronics","Computers","Home","Garden & Tools","Wine","Beauty","Toys & Games","Clothing","Shoes","Handbags","Accessories","Luggage","Jewelry","Watches"]
D2DICT = {
    "Home":[
        "Kitchen & Dinning",
        "Furniture & Lighting",
        "Rugs & Textiles",
        "Bedding & Bath",
        "Appliances",
        "Arts, Crafts & Sewing",
        "Tools, Home Improvement",
        "Home Accesories",
    ],
    "Wine":[
        "Red Wine",
        "White Wine",
        "Sparkling",
        "Others",
    ],
    "Beauty":[
        "Makeup",
        "Skin Care",
        "Hair Care",
        "Fragrance",
        "Tools & Accessories",
    ],
    "Clothing":[
        "Tops & Tees",
        "Sweaters",
        "Hoodies & Sweatshirts",
        "Active",
        "Dresses",
        "Jumpsuits & Rompers",
        "Jeans",
        "Pants",
        "Leggings",
        "Shorts",
        "Skirts",
        "Blazers & Jackets",
        "Suits",
        "Outerwear & Coats",
        "Socks & Hosiery",
        "Sleep & Lounge",
        "Intimates & Underwear",
        "Swim",
        "Accessories",
        "Maternity",
    ],
    "Accessories":[
        "Belts",
        "Ties",
        "Scarves",
        "Cufflinks"
        "Hats & Caps",
        "Wallets",
        "Card Cases",
        "Sunglasses",
        "Others",
    ],
    "Shoes": [
        "Athletic & Outdoor",
        "Boots",
        "Sneakers",
        "Flats",
        "Mules & Clogs",
        "Loafers & Slip-Ons",
        "Oxfords",
        "Pumps",
        "Sandals",
        "Slippers",
        "Work & Safety",
        "Others",
    ],
    "Handbags":[
        "Cluthes",
        "Crossbody Bags",
        "Evening Bags",
        "Hobo Bags",
        "Satchels",
        "Shoulder Bags",
        "Tote Bags",
        "Others",
    ],
    "Luggage":[
        "Backpacks",
        "Briefcases",
        "Laptop Bags",
        "Messenger Bags",
        "Others",
    ],
    "Jewelry":[
        "Rings",
        "Necklaces",
        "Earrings",
        "Bracelets",
        "Charms",
        "Anklets",
        "Others",
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
	    'Pants & Shorts',
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
        'Maternity',
        'Baby',
        'Accessories',
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
    'Bags': [
	    'Shoulder Bags',
	    'Crossbody Bags',
	    'Handbags',
	    'Backpacks & Laptop Bags',
        'Wallets',
        'Luggage Bags',
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
	    'Body Care & Hair',
    ],
    'Wine': [
	    'Red Wine',
	    'White Wine',
	    'Champagne',
    ],
}

class RawDocument(Document):
    site_key    =   StringField()   
    content     =   StringField()
    main        =   StringField()
    sub         =   StringField()
    d0          =   StringField(default="")
    d1          =   StringField(default="")
    d2          =   StringField(default="")
    updated_at  =   DateTimeField(default=datetime.utcnow)
    
    meta = {
        'indexes': [
            {'fields':['site_key'], 'unique':True, 'sparse':True}, 
        ],
        'db_alias': 'training',
    }

def convert(d0, d1, d2):
    """ convert d0,d1,d2 to a CAT(S) """
    results = []
    if d0 == "Baby":
        results.append(("Kids & Baby", "Baby"))
    if d1 in ("Electronics", "Computers"):
        results.append(("Home", "Electronics"))
    elif d1 == "Garden & Tools":
        results.append(("Home", "Tools"))
    elif (d1 == "Books" and d0 in ["Kids","Girls","Boys"]) \
        or (d1 == "Toys & Games"):
        results.append(("Kids & Baby", "Toys, Games & Books"))
    elif d1 == "Shoes":
        if d0 in ["Men","Adult","Human"]:
            results.append(("Men", "Shoes"))
        elif d0 in ["Women","Adult","Human"]:
            results.append(("Women", "Shoes"))
        elif d0 in ["Kids","Girls","Boys","Baby","Human"]:
            results.append(("Kids & Baby", "Shoes"))
    elif d1 == "Watches":
        if d0 in ["Men", "Adult", "Boys", "Kids", "Baby", "Human"]:
            results.append(("Jewelry & Watches", "Men's Watches"))
        elif d0 in ["Women", "Adult", "Girls", "Kids", "Baby", "Human"]:
            results.append(("Jewelry & Watches", "Women's Watches"))
    elif d1 == "Accessories":
        if d0 in ["Men", "Adult", "Boys", "Kids", "Baby", "Human"]:
            results.append(("Men", "Accessories"))
        elif d0 in ["Women", "Adult", "Girls", "Kids", "Baby", "Human"]:
            results.append(("Women", "Accessories"))
        else:
            results.append(("Home", "Home Accessories"))
    elif d1 in ["Luggage", "Handbags"]:
        results.append(("Handbags", d2))
    elif d1 == "Jewelry":
        results.append(("Jewelry & Watches", d2))
    else:
        results.append((d0, d2))
    return results[0]

if __name__ == '__main__':
    print convert("Human", "Home", "Furniture & Lighting")
