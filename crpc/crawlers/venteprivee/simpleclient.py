#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from datetime import datetime

from server import ventepriveeLogin
from models import Product

class CheckServer(object):
    def __init__(self):
        self.net = ventepriveeLogin()
        self.net.check_signin()

    def check_onsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nventepricee {0}, {1}\n\n'.format(id, url)
            return

        ret = self.net.fetch_page(url)
        if isinstance(ret, int):
            ret = self.net.fetch_page(url)
            if isinstance(ret, int):
                print '\n\nventeprivee product[{0}] download error.\n\n'.format(url)
                return
        js = ret.json
        brand = js['operationName']
        title = js['name']
        if prd.title.lower() != title.lower():
            print 'venteprivee product[{0}] title error: {1}, {2}'.format(prd.combine_url, prd.title, title)
        price = js['formattedPrice']
        if prd.price != price:
            print 'venteprivee product[{0}] price error: {1}, {2}'.format(prd.combine_url, prd.price, price)
        listprice = js['formattedMsrp']
        if prd.listprice != listprice:
            print 'venteprivee product[{0}] listprice error: {1}, {2}'.format(prd.combine_url, prd.listprice, listprice)
        soldout = js['isSoldOut']
        if prd.soldout != soldout:
            print 'venteprivee product[{0}] soldout error: {1}, {2}'.format(prd.combine_url, prd.soldout, soldout)
            prd.soldout = soldout
            prd.update_history.update({ 'soldout': datetime.utcnow() })
            prd.save()


    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

if __name__ == '__main__':
    CheckServer().check_onsale_product('1056013', 'http://us.venteprivee.com/v1/api/productdetail/content/1056013')
