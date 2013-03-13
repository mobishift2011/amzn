#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import re
import lxml.html
from datetime import datetime

from models import Product
from server import fetch_product

class CheckServer(object):
    def __init__(self):
        self.size = re.compile("var products_tmp = {([^}]*)};", re.M)

    def check_onsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nmodnique {0}, {1}\n\n'.format(id, url)
            return

        ret = fetch_product(url)
        if isinstance(ret[0], int):
            print '\n\nmodnique download error: {0} , {1}\n\n'.format(ret[0], ret[1])
            return

        tree = lxml.html.fromstring(ret[0])
        pprice = tree.cssselect('div.lastUnit > div.line form > div.mod > div.hd > div.media > div.bd')[0]
        price = pprice.cssselect('span.price')[0].text_content().replace('$', '')
        listprice = pprice.cssselect('span.bare')
        listprice = listprice[0].text_content().replace('retail', '').replace('$', '').strip() if listprice else ''
        title = tree.cssselect('div.lastUnit > div.line > h4.pbs')[0].text_content().strip().encode('utf-8')
        text = self.size.search(ret[0]).group(1)
        soldout = False if "Available" in text or "Last 1 Left" in text or "In Member's Bag" in text else True

        if prd.price.replace('$', '').strip() != price:
            print 'modnique product[{0}] price error: {1}, {2}'.format(prd.combine_url, prd.price.replace('$', ''), price)
        if listprice and prd.listprice.replace('$', '').strip() != listprice:
            print 'modnique product[{0}] listprice error: {1}, {2}'.format(prd.combine_url, prd.listprice.replace('$', ''), listprice)
        if prd.title.encode('utf-8').lower() != title.lower():
            print 'modnique product[{0}] title error: {1}, {2}'.format(prd.combine_url, prd.title.encode('utf-8'), title)
        if prd.soldout != soldout:
            print 'modnique product[{0}] soldout error: {1}, {2}'.format(prd.combine_url, prd.soldout, soldout)



    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

if __name__ == '__main__':
    CheckServer().check_onsale_product('01513534', 'http://www.modnique.com/product/Our-Favorite-Silver-Jewelry-Styles/10399/Ladies-Necklace-Designed-In-925-Sterling-Silver/01513534/color/Silver/size/seeac/gseeac')
