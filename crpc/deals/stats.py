#!/usr/bin/env python
# -*- coding: utf-8
from settings import MASTIFF_HOST
import slumber

from helpers.log import getlogger
logger = getlogger('picks', filename='/tmp/deals.log')

DSFILTER = slumber.API(MASTIFF_HOST).dsfilter.get()
SITEPREF = {}
siteprefs = slumber.API('http://mastiff.favbuy.org:8001/api/v1').sitepref.get().get('objects', [])
for sitepref in siteprefs:
    if sitepref.get('site'):
        SITEPREF.setdefault(sitepref.get('site'), sitepref.get('discount_threshold_adjustment'))


def main(site):
    m = __import__('crawlers.%s.models' % site, fromlist=['Product'] )
    products = m.Product.objects()

    with open('status.txt', 'w') as f: 
        f.write('url;price;listprice;disount;filter_key;medium;adjustrate;adjustment')
        for product in products:
            title = product.title.encode('utf-8')
            combine_url = product.combine_url
            price = product.favbuy_price
            listprice = product.favbuy_listprice
            disount = float(product.favbuy_price) / float(product.favbuy_listprice)
            filter_key = '%s.^_^.%s' % (product.favbuy_brand, '-'.join(product.favbuy_dept))
            medium = DSFILTER[filter_key]['medium']
            adjustrate = SITEPREF.get(site, SITEPREF.get('ALL')) or 1
            adjustment = float(medium) * float(adjustrate)
            f.write('%s;%s;%s;%s;%s;%s;%s;%s\n' % (combine_url, price, listprice, disount, filter_key, medium, adjustrate, adjustment))



if __name__ == '__main__':
    import sys
    site = sys.argv[1]
    main(site)