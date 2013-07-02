#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import re
import slumber
import lxml.html
from datetime import datetime, timedelta

from models import Product
from server import fetch_product
from settings import MASTIFF_HOST

api = slumber.API(MASTIFF_HOST)

class CheckServer(object):
    def __init__(self):
        self.size = re.compile("var products_tmp = {([^}]*)};", re.M)

    def offsale_update(self, muri):
        _id = muri.rsplit('/', 2)[-2]
        utcnow = datetime.utcnow()
        var = api.product(_id).get()
        if 'ends_at' in var and var['ends_at'] > utcnow.isoformat():
            api.product(_id).patch({ 'ends_at': utcnow.isoformat() })
        if 'ends_at' not in var:
            api.product(_id).patch({ 'ends_at': utcnow.isoformat() })

    def check_onsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nmodnique {0}, {1}\n\n'.format(id, url)
            return

        ret = fetch_product(url)
        if ret[0] == -302:
            if prd.muri:
                self.offsale_update(prd.muri)
            if not prd.products_end or prd.products_end > datetime.utcnow():
                prd.products_end = datetime.utcnow()
                prd.update_history.update({ 'products_end': datetime.utcnow() })
                prd.save()
                print '\n\nmodnique product[{0}] redirect, sale end\n\n'.format(url)
            return
        elif isinstance(ret[0], int):
            print '\n\nmodnique download error: {0} , {1}\n\n'.format(ret[0], ret[1])
            return

        tree = lxml.html.fromstring(ret[0])
        pprice = tree.cssselect('div.lastUnit > div.line form > div.mod > div.hd > div.media > div.bd')
        if pprice:
            price = pprice[0].cssselect('span.price')[0].text_content().replace('$', '').replace(',', '').strip()
            listprice = pprice[0].cssselect('span.bare')
            listprice = listprice[0].text_content().replace('retail', '').replace('$', '').replace(',', '').strip() if listprice else ''
        else:
            price = listprice = ''
        title = tree.cssselect('div.lastUnit > div.line > .pbs')[0].text_content().strip().encode('utf-8')
        text = self.size.search(ret[0]).group(1)
        soldout = False if "Available" in text or "Last 1 Left" in text or "In Member's Bag" in text else True

        if price and prd.price.replace('$', '').replace(',', '').strip() != price:
            print 'modnique product[{0}] price error: {1}, {2}'.format(prd.combine_url, prd.price.replace('$', '').replace(',', '').strip(), price)
            prd.price = price
            prd.update_history.update({ 'price': datetime.utcnow() })
            prd.save()

        if listprice and prd.listprice.replace('$', '').replace(',', '').strip() != listprice:
            print 'modnique product[{0}] listprice error: {1}, {2}'.format(prd.combine_url, prd.listprice.replace('$', '').replace(',', ''), listprice)
            prd.listprice = listprice
            prd.update_history.update({ 'listprice': datetime.utcnow() })
            prd.save()

        if not prd.title:
            prd.title = title
            prd.save()
        elif prd.title.encode('utf-8').lower() != title.lower():
            print 'modnique product[{0}] title error: {1}, {2}'.format(prd.combine_url, prd.title.encode('utf-8'), title)
        if prd.soldout != soldout:
            print 'modnique product[{0}] soldout error: {1}, {2}'.format(prd.combine_url, prd.soldout, soldout)
            prd.soldout = soldout
            prd.update_history.update({ 'soldout': datetime.utcnow() })
            prd.save()



    def check_offsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nmodnique {0}, {1}\n\n'.format(id, url)
            return

        ret = fetch_product(url)
        if ret[0] == -302:
            return
        elif isinstance(ret[0], int):
            print '\n\nmodnique download error: {0} , {1}\n\n'.format(ret[0], ret[1])
            return

        soldout = None
        tree = lxml.html.fromstring(ret[0])
        text = tree.cssselect('#soldout a span')[0].text_content().strip()
        if 'Add To Waitlist' in text:
            soldout = True
        elif 'sold out' in text:
            soldout = True
        elif 'size sold' in text:
            soldout = False
        if soldout is False:
            print '\n\nmodnique product[{0}] on sale again.'.format(url)
            # no specific time, so add 3 days, If it off sale, can be fond by offsale function
            products_end = datetime.utcnow() + timedelat(days=3)
            prd.products_end = products_end
            prd.update_history.update({ 'products_end': datetime.utcnow() })
            prd.on_again = True
            prd.save()

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

if __name__ == '__main__':
    CheckServer().check_offsale_product('01492742', 'http://www.modnique.com/product/Top-Trends-Shop/8545/Color-Me-Red-Wrap-V-Neck-Dress/01492742/color/PURPLE/size/seeac/gseeac')
