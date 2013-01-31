# -*- coding: utf-8 -*-
from settings import MASTIFF_HOST
from admin.models import Brand
import slumber

def sync2extracter(brand):
	pass


def sync2mastiff(brand):
	if brand.is_delete:
		return

	name = brand.title_edit or brand.title
	api = slumber.API('http://192.168.2.108:8001/api/v1/')#(MASTIFF_HOST)
	query = api.brand.get(name=name)
	params = {
		'name': name.encode('utf-8'),
		'url': brand.url.encode('utf-8') if brand.url else '',
		'blurb': brand.blurb.encode('utf-8') if brand.blurb else '',
		'level': brand.level,
		# 'aliases': brand.alias,
	}

	if query['meta']['total_count']:
		brand_id = query['objects'][0]['id']
		api.brand(brand_id).patch(params)
	else:
		api.brand.post(params)


def sync():
	brands = Brand.objects()
	for brand in brands:
		sync2extracter(brand)
		sync2mastiff(brand)

if __name__ == '__main__':
	sync()