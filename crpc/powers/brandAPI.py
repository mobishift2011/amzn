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
	return json.loads(self.get()).get('response', [])

def create(self):
	return self.post()	# TODO

def match(self, brand='', title='', url=''):
	indicator = 'brand'
	match = index.query(brand)
	if not match:
		indicator = 'title'
		match = index.query(title)
	if match:
		print '%s match:' % indicator
		print '%s%s%s%s%s%s' % (brand, '\n', title, '\n', match, '\n\n'),
		return brand

	if not match:
		temp_output(brand, title, url)
		return None

def temp_output(brand, title, url):
    with open(os.path.dirname(__file__)+'/tempoutput', 'ar') as f:
        f.write("%s\n%s\n%s\n\n" % ('prod brand: '+ brand,'title: ' + title, 'url: '+url))

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
	match()