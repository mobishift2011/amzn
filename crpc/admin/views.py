# -*- coding: utf-8 -*-
from settings import MASTIFF_HOST
from models import Brand
from powers.models import Brand as PowerBrand, Link
import slumber
from urllib import unquote

def get_all_brands(db='catalogIndex'):
	if db.lower() == "catalogindex":
		brands = [brand.to_json() for brand in Brand.objects()]
	elif db.lower() == "power":
		brands = [{
			'title': brand.title,
			'title_edit': brand.title_edit,
			'global_searchs': brand.global_searchs,
		} for brand in PowerBrand.objects()]
	return brands

def get_brand(title, db):
	if not db:
		db = 'e'
	if db == 'e':
		brand = Brand.objects.get(title=title)
	elif db == 'p':
		brand = PowerBrand.objects.get(title=title)
	return brand.to_json()

def update_brand(title, arguments):
	brand = Brand.objects.get(title=title) \
		if title else Brand()

	for k, v in arguments.iteritems():
		try:
			value = getattr(brand, k)
		except AttributeError:
			continue

		if hasattr(value, '__iter__'):
			setattr(brand, k, list(set(value) | set(v)))	
		else:
			value = v[0] if v else value
			if value == 'True':
				value = True
			elif value == 'False':
				value = False
			setattr(brand, k, value)

	brand.save()
	brand = Brand.objects.get(title=brand.title)
	return brand.to_json()


def delete_brand(title):
	brand = Brand.objects(title=title)
	if brand:
		brand.delete()
	else:
		return False

	return True


def update_brand_volumn(title, volumns):
	pb = PowerBrand.objects.get(title=title)
	pb.global_searchs = volumns
	pb.save()
	return pb.to_json()



link_api = slumber.API(MASTIFF_HOST)

def get_all_links():
	return [ link for link in link_api.affiliate.get().get('objects') ]


def post_link(patch=False, **kwargs):
	site = kwargs.get('site')
	affiliate = kwargs.get('affiliate')

	request = link_api.affiliate(kwargs.get('key')).patch(kwargs) \
		if patch else link_api.affiliate.post(kwargs)


def delete_link(key):
	links = Link.objects(key=key)
	links.delete()

