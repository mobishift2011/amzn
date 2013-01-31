# -*- coding: utf-8 -*-
from settings import MASTIFF_HOST
from admin.models import Brand
from helpers.log import getlogger
import slumber

logger = getlogger('brandsync', filename='/tmp/brandsync.log')

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
	brands = Brand.objects(is_delete=False)
	logger.debug('Total brands to sync: {0}'.format(len(brands)))
	for brand in brands:
		try:
			sync2extracter(brand)
		except Exception, e:
			logger.error('Sync for extracter error: {0}'.format(traceback.format_exc()))
		try:
			sync2mastiff(brand)
		except Exception, e:
			logger.error('Sync for mastiff error: {0}'.format(traceback.format_exc()))


if __name__ == '__main__':
	sync()