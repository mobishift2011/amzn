# -*- coding: utf-8 -*-
from settings import CRPC_ROOT
from crawlers.common.stash import exclude_crawlers
from powers.models import Brand
from powers.routine import get_site_module

from mongoengine import Q
from collections import Counter
from datetime import datetime
import os

__module = {} 

def get_all_sites():
	names = set(os.listdir(os.path.join(CRPC_ROOT, 'crawlers'))) - \
				set(exclude_crawlers)
	return [name for name in names if os.path.isdir(os.path.join(CRPC_ROOT, 'crawlers', name))]

def get_unextracted_brands(site):
	unknown_set = set()
	now = datetime.utcnow()
	# products = __module[site].Product.objects(Q(brand_complete=False) \
	# 			& (Q(products_begin__lte=now) | Q(products_begin__exists=False)) \
	# 				& (Q(products_end__gte=now) | Q(products_end__exists=False)) \
	# 					).values_list('brand', 'title', 'combine_url')
	products = __module[site].Product.objects(brand_complete=False).values_list('brand', 'title', 'combine_url')
	
	c = Counter()
	for brand, title, combine_url in products:
		if brand:
			c[brand] += 1
		else:
			unknown_set.add((title, combine_url))

	print site
	print 'unextracted products: ', products.count()
	print 'unextracted brands: ', len(c.keys())
	print 'no brand products: ', len(unknown_set)
	print c
	print
	
	return c, unknown_set

def feed(brands, unknowns):
	pass

def main():
	sites = get_all_sites()
	for site in sites:
		__module[site] = get_site_module(site)
		brands, unknowns = get_unextracted_brands(site)
		feed(brands, unknowns)

if __name__ == '__main__':
	main()