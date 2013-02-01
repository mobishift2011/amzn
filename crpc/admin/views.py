# -*- coding: utf-8 -*-
from models import Brand

def get_all_brands():
	brands = [brand.to_json() for brand in Brand.objects()[0:101]]
	return brands

def get_brand(title):
	brand = Brand.objects.get(title=title)
	return brand.to_json()

def update_brand(title, arguments):
	print '~~~~~~~~~~~~', title
	brand = Brand.objects.get(title=title)

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