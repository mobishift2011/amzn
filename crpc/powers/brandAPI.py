# -*- coding: utf-8 -*-
from configs import SITES, DEBUG, CATALOG_BASE_URL

from gevent import monkey; monkey.patch_all()
import gevent

from slumber import API, Resource
import requests
import json
import re
import os
import esm

APIClient = API(CATALOG_BASE_URL)

def all(self):
	r = requests.get('http://localhost:1319/api/brand/').json
	return r.get('response', [])

def create(self):
	return self.post()	# TODO

def fail(*args, **kwargs):
	"""
	* params:
    ** title
    ** model: Brand, Dept, Tag
    ** content: The content of failure such as the brand name that can'be extacted.
    ** site: required
    ** doctype: Event or Product, required
    ** key = required
    ** url
	"""
	r = requests.post('http://localhost:1319/api/brand/fail/', data=kwargs)
	return r.status_code == 200


def match(self, **kwargs):
	site = kwargs.get('site', '')
	doctype = kwargs.get('doctype', '').capitalize()
	key = kwargs.get('key', '')
	brand = kwargs.get('brand') or ''
	title = kwargs.get('title') or ''
	combine_url = kwargs.get('combine_url') or ''

	# TO REMOVE
	import time
	print site,' ' + doctype + ' ',  key + ' ', 'brand-<'+brand+'>  ',  'title-<'+ title +'>'+ ':'

	indicator = 'brand'
	match = index.query(brand)
	if not match:
		indicator = 'title'
		match = index.query(title)
	if match:
		print '%s match:' % indicator
		print '%s%s%s%s%s%s' % (brand, '\n', title, '\n', match, '\n\n'),
		return match[-1][1]

	if not match:
		fail(title=title, model='Brand', content=brand, site=site, doctype=doctype, key=key, url=combine_url)
		# temp_output(brand, title, url)
		return None

# def temp_output(brand, title, url):
#     with open(os.path.dirname(__file__)+'/tempoutput', 'ar') as f:
#         f.write("%s\n%s\n%s\n\n" % ('prod brand: '+ brand,'title: ' + title, 'url: '+url))

setattr(Resource, 'all', all)
setattr(Resource, 'create', create)
setattr(Resource, 'match', match)

print 'brand index init'
index = esm.Index()
brands = APIClient.brand.all()
print 'brands total count:%s' % len(brands)
for brand in brands:
	index.enter(brand.encode('utf-8'))
index.fix()

if __name__ == '__main__':
	# APIClient.brand.fail(site='aaa', doctype='event', key='babala')
	# APIClient.brand.all()
	pass