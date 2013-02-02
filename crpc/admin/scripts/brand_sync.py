# -*- coding: utf-8 -*-
from settings import MONGODB_HOST
from settings import MASTIFF_HOST
from admin.models import Brand as EditBrand
from powers.models import Brand as PowerBrand
from helpers.log import getlogger
import slumber
import json
import requests
import traceback

logger = getlogger('brandsync', filename='/tmp/brandsync.log')

def sync2power(host="http://mongodb.favbuy.org:1317/brand/"):
	"""Brand of catalogIndex sync to the one of power"""
	brands = EditBrand.objects(is_delete=False)
	logger.debug('Total edit brands to sync: {0}'.format(len(brands)))

	for brand in brands:
		try:
			r = requests.post(host, data={'brand': json.dumps(brand.to_json())})
			r.raise_for_status()
			logger.debug('Sync to power: {0} ---> {1}'.format(
				brand.title.encode('utf-8'), \
					brand.title_edit.encode('utf-8') if brand.title_edit else ''))
		except Exception, e:
			logger.error('Sync to power error: {0}'.format(traceback.format_exc()))


def sync2mastiff(host=MASTIFF_HOST):
	"""Brand of power sync to the one of mastiff"""
	api = slumber.API(host)
	brands = PowerBrand.objects(is_delete=False)
	logger.debug('Total power brands to sync: {0}'.format(len(brands)))

	for brand in brands:
		try:
			name = brand.title_edit or brand.title
			query = api.brand.get(name=name)
			params = {
				'name': name.encode('utf-8'),
				'url': brand.url.encode('utf-8') if brand.url else '',
				'blurb': brand.blurb.encode('utf-8') if brand.blurb else '',
				'level': brand.level,
				# 'aliases': brand.alias,
				'local_searchs': brand.local_searchs,
			}

			if query['meta']['total_count']:
				brand_id = query['objects'][0]['id']
				api.brand(brand_id).patch(params)
			else:
				api.brand.post(params)

		except Exception, e:
			logger.error('Sync to mastiff error: {0}'.format(traceback.format_exc()))


if __name__ == '__main__':
	sync2mastiff()