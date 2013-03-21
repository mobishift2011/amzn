#!/usr/bin/env python
# -*- coding: utf-8
from settings import MASTIFF_HOST
from events import change_for_dsfilter
from pipelines import ProductPipeline
import slumber

DSFILTER = slumber.API(MASTIFF_HOST).dsfilter.get()
SITEPREF = {}
siteprefs = slumber.API('http://mastiff.favbuy.org:8001/api/v1').sitepref.get().get('objects', [])
for sitepref in siteprefs:
    if sitepref.get('site'):
        SITEPREF.setdefault(sitepref.get('site'), sitepref.get('discount_threshold_adjustment'))


@change_for_dsfilter.bind
def refresh_dsfilter(sender, **kwargs):
    global DSFILTER
    global SITEPREF
    DSFILTER = slumber.API(MASTIFF_HOST).dsfilter.get()
    SITEPREF = {}
    siteprefs = slumber.API('http://mastiff.favbuy.org:8001/api/v1').sitepref.get().get('objects', [])
    for sitepref in siteprefs:
        if sitepref.get('site'):
            SITEPREF.setdefault(sitepref.get('site'), sitepref.get('discount_threshold_adjustment'))


class Picker(object):
    def __init__(self, site=None):
        self.site = site

    def pick(self, product):
        pp = ProductPipeline(self.site, product)
        pp.clean()
        return pick_by_disfilter(product, SITEPREF.get(self.site, SITEPREF.get('ALL')) or 1)


def pick_by_disfilter(product, threshold_adjustment=1):
    if not product.favbuy_price or not product.favbuy_listprice:
        return False

    if product.favbuy_brand:
        filter_key = '%s.^_^.%s' % (product.favbuy_brand, product.favbuy_dept) \
            if product.favbuy_dept else '%s.^_^.ALL' % product.favbuy_brand

        threhold = DSFILTER.get(filter_key, {}).get('medium', 0)
        discount = float(product.favbuy_price) / float(product.favbuy_listprice)

        print discount, ' compared to threshold: %s * %s = %s \n' % (threhold, threshold_adjustment, threhold * threshold_adjustment)
        return discount < threhold * threshold_adjustment

    return False


# Strategy = {
#   'default': [pick_by_disfilter],
# }


if __name__ == '__main__':
    import sys
    site = sys.argv[1]
    m = __import__('crawlers.%s.models' % site, fromlist=['Product']) 
    pick_list = []
    products = m.Product.objects(dept__exists=True)
    for product in products:
        p = Picker('nordstrom')
        if p.pick(product):
            pick_list.append(product)
            print

    # for product in pick_list:
    #     print product.key, product.title
    #     print product.brand, product.favbuy_brand
    #     print product.dept, product.favbuy_dept
    #     print float(product.favbuy_price) / float(product.favbuy_listprice)
    #     print product.combine_url, '\n'

    print products.count(), len(pick_list)