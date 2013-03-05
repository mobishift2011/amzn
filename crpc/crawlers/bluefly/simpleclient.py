#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import requests
import slumber
import lxml.html

from settings import MASTIFF_HOST
from models import Product

api = slumber.API(MASTIFF_HOST)

class CheckServer(object):
    def __init__(self):
        self.s = requests.Session()
        self.headers = {
        }

    def check_onsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nbluefly {0}, {1}\n\n'.format(id, url)
            return
        ret = self.s.get(url, headers=self.headers)
        if not ret.ok:
            ret = self.s.get(url, headers=self.headers)
            if not ret.ok:
                print '\n\nbluefly download product error: {0}\n\n'.format(url)
                return
        tree = lxml.html.fromstring(ret.content)
        # brand = tree.cssselect('section#main-product-detail > div.product-info > div.limitBrandName > h1.product-brand > a')[0].get('name')
        title = tree.cssselect('section#main-product-detail > div.product-info > h2.product-name')[0].text_content().strip()

        price = tree.cssselect('div.product-info div.product-prices span[itemprop=price]')[0].text_content().replace('retail', '').replace(':', '').replace('$', '').strip()

        soldout = True if tree.cssselect('div.product-info div.product-prices div.soldout-label') else False
        if soldout != prd.soldout:
            print 'bluefly product[{0}] soldout error: {1} vs {2}'.format(url, prd.soldout, soldout)
        if price != prd.price.replace('$', '').strip():
            print 'bluefly product[{0}] price error: {1} vs {2}'.format(url, prd.price, price)
        if title.lower() != prd.title.lower():
            print 'bluefly product[{0}] title error: {1} vs {2}'.format(url, prd.title, title)

if __name__ == '__main__':
    pass
