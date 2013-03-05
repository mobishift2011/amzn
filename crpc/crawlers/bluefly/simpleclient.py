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

        listprice = tree.cssselect('div.product-info div.product-prices span.retail-price')[0].text_content().replace('retail :', '').replace('$', '').replace(',', '').strip()
        price = tree.cssselect('div.product-info div.product-prices span[itemprop=price]')[0].text_content().replace('(FINAL SALE)', '').replace('$', '').replace(',', '').strip()

        soldout = True if tree.cssselect('div.product-info div.product-prices div.soldout-label') else False
        if soldout != prd.soldout:
            prd.soldout = soldout
            prd.update_history.update({ 'soldout': datetime.utcnow() })
            prd.save()
            print 'bluefly product[{0}] soldout error: {1} vs {2}'.format(url, prd.soldout, soldout)
        if listprice != prd.listprice.replace('$', '').replace(',', '').strip():
            prd.listprice = listprice
            prd.update_history.update({ 'listprice': datetime.utcnow() })
            print 'bluefly product[{0}] listprice error: {1} vs {2}'.format(url, prd.listprice.replace('$', '').replace(',', '').strip(), listprice)
        if price != prd.price.replace('$', '').replace(',', '').strip():
            prd.price = price
            prd.update_history.update({ 'price': datetime.utcnow() })
            print 'bluefly product[{0}] price error: {1} vs {2}'.format(url, prd.price.replace('$', '').replace(',', '').strip(), price)
        if title.lower() != prd.title.lower():
            print 'bluefly product[{0}] title error: {1} vs {2}'.format(url, prd.title.encode('utf-8'), title.encode('utf-8'))

    def check_offsale_product(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

if __name__ == '__main__':
    pass
