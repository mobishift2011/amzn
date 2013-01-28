# -*- coding: utf-8 -*-
from settings import CRPC_ROOT
from crawlers.common.stash import exclude_crawlers
from powers.models import Brand
from powers.routine import get_site_module
from mongoengine import Q
import os

"""
To count the brands which has been extracted by the products.
"""

def get_all_sites():
	names = set(os.listdir(os.path.join(CRPC_ROOT, 'crawlers'))) - \
				set(exclude_crawlers)
	return [name for name in names if os.path.isdir(os.path.join(CRPC_ROOT, 'crawlers', name))]

def stat():
	brand_set = set()
	sites = get_all_sites()
	for site in sites:
		print 'site -> {0}\n'.format(site)
		m = get_site_module(site)
		favbuy_brands = m.Product.objects(brand_complete=True).values_list('favbuy_brand')
		brand_set.update(set(favbuy_brands))

	brand_list = list(brand_set)
	brand_list.sort()
	return brand_list

def main():
	favbuy_brands = stat()
	total = len(favbuy_brands)
	file_path = CRPC_ROOT + '/powers/script/product_brands.txt'
	with open(file_path, 'w') as f:
		f.write('total: '+ str(total)+'\r\n\r\n\r\n')
		for favbuy_brand in favbuy_brands:
			brand = Brand.objects(Q(title_edit=favbuy_brand) | Q(title=favbuy_brand)).first()
			title = brand.title_edit if brand.title_edit else brand.title
			f.write('%s\r\n' % title.encode('utf-8'))
			for alias in brand.alias:
				if alias and alias != 'undefined':
					f.write(alias.encode('utf-8')+'\r\n')
		f.write('\r\n')

if __name__ == '__main__':
	main()