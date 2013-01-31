# -*- coding: utf-8 -*-
from datetime import datetime
import re
import types

AmznSID = 'favbuy-20'

class Affiliate(object):
	def __init__(self, site=None):
		self.combine_url = ''
		self.site = site
		if site:
			fn = Strategy.get(site)
			if fn and hasattr(fn, '__call__'):
				self.get_link = types.MethodType(fn, self)

	def get_link(self, product):
		"""
		Convert the product combine_url to Affiliate url.
		"""
		print 'default get_link -> {0}'.format(self.site)
		return ''


def myhabit(self, combine_url):
	"""
	Doc: http://www.myhabit.com/help/200690180
	Insert tag=<INSERT_STORE_ID> to the url, eg.
	http://www.myhabit.com/?tag=<INSERT_STORE_ID>
	#page=d&dept=women&sale=A1OVF043559BDP&asin=B006L4PRN4&cAsin=B006L
	"""
	pattern = r'(https?://.*?)\??(#.*)'
	match = re.search(pattern, combine_url)
	if match:
		url, params = match.groups()
		favbuy_url = "%s?tag=%s%s" % (url, AmznSID, params)
		return favbuy_url
	else:
		return


def cj(self, combine_url):
	pass


def linkshare():
	"""
	Doc: http://cli.linksynergy.com/cli/publisher/links/webServices.php?serviceID=43
	"""
	pass

def test(site=None):
	from crawlers.venteprivee.models import *
	from mongoengine import Q

	products = Product.objects(Q(url_complete=None) | Q(url_complete=False))
	print len(products)
	for product in products:
		if not product.combine_url \
			or product.url_complete:
				return

		affiliate = Affiliate('venteprivee') # TO alternative the site
		product.favbuy_url = affiliate.get_link(product.combine_url)
		print product.combine_url
		print product.favbuy_url
		print
		product.url_complete = bool(product.favbuy_url)

		if product.url_complete:
			product.update_history.update({'favbuy_url': datetime.utcnow()})

		product.save()

Strategy = {
	'myhabit': myhabit,
	'beyondtherack': linkshare,
	'venteprivee': myhabit,
}

if __name__ == '__main__':
	test()
