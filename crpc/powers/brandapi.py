# -*- coding: utf-8 -*-
import requests
import json
import re
import os
import esm

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djCatalog.djCatalog.settings")
from djCatalog.catalogs.models import Brand
from configs import SITES

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

class Extracter(object):
	def __init__(self):
		self.stopwords = ' \t\r\n,;.%0123456789\'"_-'
		print 'brand index init'
		self._rebuild_index()

	def _rebuild_index(self):
		brands = Brand.objects().values_list('title')
		print 'brands total count:%s' % len(brands)

		self.index = esm.Index()
		for brand in brands:
			self.index.enter(brand.lower().encode('utf-8'), brand)
		self.index.fix()

	def extract(self, brand):
		ret = ''
		brand = brand.lower()
		mathces = self.index.query(brand)

		for match in matches:
			startPos = match[0][0]
			endPos = match[0][1]
			pattern_brand = match[1]
			if (startPos== 0 or brand[startPos-1] in self.stopwords) and \
				(endPos == len(brand) or brand[endPos] in self.stopwords) \
					and len(pattern_brand) > ret :
						ret = pattern_brand
		return ret

	# def postFail(self, **kwargs)
	# 	site = kwargs.get('site', '')
	# 	doctype = kwargs.get('doctype', '').capitalize()
	# 	key = kwargs.get('key', '')
	# 	brand = kwargs.get('brand') or ''
	# 	title = kwargs.get('title') or ''
	# 	combine_url = kwargs.get('combine_url') or ''

	# 	#TO REMOVE
	# 	import time
	# 	print site,' ' + doctype + ' ',  key + ' ', 'brand-<'+brand+'>  ',  'title-<'+ title +'>'+ ':'

	# 	indicator = 'brand'
	# 	match = index.query(brand)
	# 	if not match:
	# 		indicator = 'title'
	# 		match = index.query(title)
	# 	if match:
	# 		print '%s match:' % indicator
	# 		print '%s%s%s%s%s%s' % (brand, '\n', title, '\n', match, '\n\n'),
	# 		return match[-1][1]

	# 	if not match:
	# 		fail(title=title, model='Brand', content=brand, site=site, doctype=doctype, key=key, url=combine_url)


if __name__ == '__main__':
	# APIClient.brand.fail(site='aaa', doctype='event', key='babala')
	# APIClient.brand.all()
	pass