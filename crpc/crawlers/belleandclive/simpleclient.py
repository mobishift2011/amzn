#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import requests
import lxml.html

from server import belleandcliveLogin
from models import Product, Event

class CheckServer(object):
    def __init__(self):
        self.net = belleandcliveLogin()
        self.net.check_signin()

    def check_onsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nbelleandclive {0}, {1}\n\n'.format(id, url)
            return

        cont = self.net.fetch_page(url)
        if cont is None or isinstance(cont, int):
            return
        tree = lxml.html.fromstring(cont)
        node = tree.cssselect('div#product-detail-wrapper div#product-details')[0]
        title = node.cssselect('div.left h1')[0].text_content().encode('utf-8')
        price = node.cssselect('div.left h3')[0].text_content().replace('$', '').replace(',', '').strip()
        listprice = node.cssselect('div.left p span')
        listprice = listprice[0].text_content().replace('$', '').replace(',', '').strip() if listprice else ''
        soldout = node.cssselect('div#product-detail-wrapper div#product-images div#img-div div.soldout-wrapper')
        soldout = True if soldout else False

        if prd.title.lower() != title.lower():
            print 'belleandclive product[{0}] title error: [{1} vs {2}]'.format(url, prd.title.encode('utf-8'), title.encode('utf-8'))
        if prd.listprice != listprice:
            print 'belleandclive product[{0}] listprice error: [{1} vs {2}]'.format(url, prd.listprice, listprice)
        if prd.price != price:
            print 'belleandclive product[{0}] price error: [{1} vs {2}]'.format(url, prd.price, price)
        if prd.soldout != soldout:
            print 'belleandclive product[{0}] soldout error: [{1} vs {2}]'.format(url, prd.soldout, soldout)


    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

if __name__ == '__main__':
    pass
