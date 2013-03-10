#!/usr/bin/env python
# -*- coding: utf-8

from pipelines import ProductPipeline


class Picker(object):
	def __init__(self, site=None):
		self.site = site

	def pick(self, product):
		pp = ProductPipeline(self.site, product)
		
		selected = True
		fns = Strategy.get(self.site, Strategy.get('default'))

		for fn in fns:
			if hasattr(fn, '__call__') and not fn(product):
				selected = False
		
		return selected


def price_pick(product):
	# print 'price pick'

	return True


def discount_pick(product):
	# print 'discount pick'

	# threshold = 0.5
	# discount = product.price / product.listprice

	# if discount < threshold:
	# 	return True
	
	return True


def dept_pick(product):
	# print 'dept pick'
	
	return True


Strategy = {
	'default': [price_pick, discount_pick, dept_pick],
}


if __name__ == '__main__':
	pass