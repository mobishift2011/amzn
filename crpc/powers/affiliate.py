# -*- coding: utf-8 -*-
from powers.models import Link
from datetime import datetime
import re
import requests
import urllib
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
	pattern = r'(https?://[^\?]*)\??(#.*)'
	match = re.search(pattern, combine_url)
	if match:
		url, params = match.groups()
		favbuy_url = "%s?tag=%s%s" % (url, AmznSID, params)
		return favbuy_url
	else:
		return


def cj(self, combine_url):
	favbuy_url = None
	link = Link.objects(site=self.site, affiliate='cj').first()

	if not link:
		return

	tracking_url = link.tracking_url
	if not tracking_url:
		return

	pattern = r'(https?://[^\?]*)\??(.*)'
	match = re.search(pattern, tracking_url)
	if not match:
		return

	url, params = match.groups()
	favbuy_url = '%s?url=%s&%s' % (url, urllib.quote_plus(combine_url), params) \
					if params else '%s?url=%s' % (url, urllib.quote_plus(combine_url))

	return favbuy_url


def linkshare(self, combine_url):
	"""
	Doc: http://cli.linksynergy.com/cli/publisher/links/webServices.php?serviceID=43
	"""
	TOKEN = 'dbc865547a1a0a42b1f0ddac8574a1f1d0262a9705b55636246b5d47ee13196e'
	MID = ''

	url = 'http://getdeeplink.linksynergy.com/createcustomlink.shtml?'
	url += 'token={0}&mid={1}&murl={2}'.format(TOKEN, MID, combine_url)

	print url

	link_generator = requests.get(url)
	print link_generator.content


def test(site=None):
	from crawlers.bluefly.models import *
	from mongoengine import Q

	products = Product.objects(Q(url_complete=None) | Q(url_complete=False))
	for product in products:
		if not product.combine_url \
			or product.url_complete:
				return

		affiliate = Affiliate('bluefly') # TO alternative the site
		product.favbuy_url = affiliate.get_link(product.combine_url)
		print product.combine_url
		print product.favbuy_url
		
		product.url_complete = bool(product.favbuy_url)

		print product.url_complete
		print

		if product.url_complete:
			product.update_history.update({'favbuy_url': datetime.utcnow()})

		# product.save()

	print len(products)


Strategy = {
	'myhabit': myhabit,
	# 'beyondtherack': linkshare,
	'bluefly': cj,
	'belleandclive': cj,
}

if __name__ == '__main__':
	test()
