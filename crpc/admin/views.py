# -*- coding: utf-8 -*-
from models import Brand

def get_all_brands():
	brands = [brand.to_json() for brand in Brand.objects()[0:101]]
	return brands

def get_brand(title):
	brand = Brand.objects.get(title=title)
	return brand.to_json()

def delete_brand(title):
	brand = Brand.objects(title=title)
	if brand:
		brand.delete()
	else:
		return False

	return True