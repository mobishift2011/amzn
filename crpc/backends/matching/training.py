#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bottle

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
