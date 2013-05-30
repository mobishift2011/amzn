#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import requests
import slumber
import lxml.html
from datetime import datetime

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

        soldout = True if tree.cssselect('div.product-info div.product-prices div.soldout-label') else False
        if soldout != prd.soldout:
            print 'bluefly product[{0}] soldout error: {1} vs {2}'.format(url, prd.soldout, soldout)
            prd.soldout = soldout
            prd.update_history.update({ 'soldout': datetime.utcnow() })
            prd.save()

        try:
            listprice = tree.cssselect('div.product-info div.product-prices span.retail-price')[0].text_content().replace('retail :', '').replace('$', '').replace(',', '').strip()
            if float(listprice) != float(prd.listprice.replace('$', '').replace(',', '').strip()):
                print 'bluefly product[{0}] listprice error: {1} vs {2}'.format(url, prd.listprice.replace('$', '').replace(',', '').strip(), listprice)
                prd.listprice = listprice
                prd.update_history.update({ 'listprice': datetime.utcnow() })
                prd.save()
        except IndexError:
            print 'bluefly product[{0}] listprice not get.'.format(url)

        price = tree.cssselect('div.product-info div.product-prices span[itemprop=price]')[0].text_content().replace('(FINAL SALE)', '').replace('$', '').replace(',', '').strip()
        if float(price) != float(prd.price.replace('$', '').replace(',', '').strip()):
            print 'bluefly product[{0}] price error: {1} vs {2}'.format(url, prd.price.replace('$', '').replace(',', '').strip(), price)
            prd.price = price
            prd.update_history.update({ 'price': datetime.utcnow() })
            prd.save()
        if title.lower() != prd.title.lower():
            print 'bluefly product[{0}] title error: {1} vs {2}'.format(url, prd.title.encode('utf-8'), title.encode('utf-8'))

        list_info = []
        for li in tree.cssselect('section#main-product-detail div.product-info div.product-info-tabs div.product-detail-list ul.property-list li'):
            list_info.append(li.text_content().strip().replace('\n', ''))
        if list_info:
            prd.list_info = list_info
            prd.update_history.update({ 'list_info': datetime.utcnow() })
            prd.save()

    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass


if __name__ == '__main__':
    pass
