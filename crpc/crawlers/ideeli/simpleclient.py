#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import re
import json
import lxml.html

from server import ideeliLogin
from models import Product

class CheckServer(object):
    def __init__(self):
        self.size_scarcity = re.compile("SkuBasedRemainingItems\({\s*url: function\(\) { return '(.+)' },")
        self.net = ideeliLogin()
        self.net.check_signin()


    def check_onsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nideeli {0}, {1}\n\n'.format(id, url)
            return

        cont = self.net.fetch_page(url)
        if isinstance(cont, int):
            ret = self.net.fetch_page(url)
            if isinstance(cont, int):
                print '\n\nideeli product[{0}] download error.\n\n'.format(url)
                return

        tree = lxml.html.fromstring(cont)
        price = tree.cssselect('div#offer_price div.info div.name_container div.price_container span.price')[0].text_content()
        listprice = tree.cssselect('div#offer_price div.info div.name_container div.price_container span.msrp_price')[0].text_content()
        title = tree.cssselect('div#offer_price div.info div.name_container div.name span.product_name')[0].text_content()

        sizes = []
        for ss in tree.cssselect('div#sizes_container_{0} div.sizes div.size_container'.format(id)):
            sizes.append( ss.get('data-type-skuid') )
        link = self.size_scarcity.search(cont).group(1)
        link = link if link.startswith('http') else 'http://www.ideeli.com' + link
        ret = self.net.fetch_page(link)
        js = json.loads(ret)
        soldout = True
        for sku in sizes:
            if js['skus'][sku] != u'0':
                soldout = False
                break

        if prd.price != price:
            print 'ideeli product[{0}] price error: {1}, {2}'.format(prd.combine_url, prd.price, price)
        if prd.listprice != listprice:
            print 'ideeli product[{0}] listprice error: {1}, {2}'.format(prd.combine_url, prd.listprice, listprice)
        if prd.title.lower() != title.lower():
            print 'ideeli product[{0}] title error: {1}, {2}'.format(prd.combine_url, prd.title, title)
        if prd.soldout != soldout:
            print 'ideeli product[{0}] soldout error: {1}, {2}'.format(prd.combine_url, prd.soldout, soldout)


    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

if __name__ == '__main__':
    CheckServer().check_onsale_product('3011542', 'http://www.ideeli.com/events/128378/offers/7091342/latest_view/3011542')
#CheckServer().check_onsale_product('3050034', 'http://www.ideeli.com/events/128378/offers/7081882/latest_view/3050034')
