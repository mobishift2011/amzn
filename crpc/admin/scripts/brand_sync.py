# -*- coding: utf-8 -*-
from settings import MONGODB_HOST
from settings import MASTIFF_HOST
from admin.models import Brand as EditBrand
from powers.models import Brand as PowerBrand
from helpers.log import getlogger
import slumber
import json
import requests
import sys
import traceback

logger = getlogger('brandsync', filename='/tmp/brandsync.log')

def sync2power(host="http://localhost:1317/brand/"):
	"""Brand of catalogIndex sync to the one of power"""
	brands = EditBrand.objects(is_delete=False)
	logger.debug('Total edit brands to sync {0}: {1}'.format(host, len(brands)))

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

	error_count = 0
	for brand in brands:
		try:
			name = brand.title_edit or brand.title
			safe_name = name.replace('/', '_')
			safe_name = safe_name.replace('?', '_')
			query = api.brand.get(name=name)
			params = {
				'name': name.encode('utf-8'),
				'safe_name': safe_name,
				'url': brand.url.encode('utf-8') if brand.url else '',
				'blurb': brand.blurb.encode('utf-8') if brand.blurb else '',
				'level': brand.level,
				# 'aliases': brand.alias,
				'global_searchs': brand.global_searchs,
				'logo_url': brand.images[0] if brand.images else '',
				'icon_url': brand.icon if brand.icon else '',
				'cn_name': brand.title_cn,
				'cn_blurb': brand.blurb_cn,
			}

			if query['objects']:
				brand_id = query['objects'][0]['id']
				api.brand(brand_id).patch(params)
			else:
				print 'post new brand', params.get('name')
				api.brand.post(params)

			print name, brand.title_cn

		except Exception, e:
			logger.error('Sync {0} to mastiff error: {1}'.format(name.encode('utf-8'), traceback.format_exc()))
			error_count += 1
	print error_count


if __name__ == '__main__':
	if sys.argv > 1:
		if sys.argv[1] == '-p':
			sync2power()
		elif sys.argv[1] == '-m':
			sync2mastiff()
	else:
		print 'Option -p or -m required.'