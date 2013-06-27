#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
import slumber
from datetime import datetime

from server import beyondtherackLogin
from models import Product, Event

from settings import MASTIFF_HOST
api = slumber.API(MASTIFF_HOST)

class CheckServer(object):
    def __init__(self):
        self.net = beyondtherackLogin()
        self.net.check_signin()

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
            print '\n\nbeyondtherack {0}, {1}\n\n'.format(id, url)
            return

        cont = self.net.fetch_product_page(url)
        if cont == -302:
            if prd.muri:
                self.offsale_update(prd.muri)
            if not prd.products_end or prd.products_end > datetime.utcnow():
                prd.products_end = datetime.utcnow()
                prd.update_history.update({ 'products_end': datetime.utcnow() })
                prd.save()
                print '\n\nbeyondtherack product[{0}] redirect, sale end.'.format(url)
            return

        elif cont is None or isinstance(cont, int):
            cont = self.net.fetch_product_page(url)
            if cont is None or isinstance(cont, int):
                print '\n\nbeyondtherack product[{0}] download error.\n\n'.format(url)
                return

        tree = lxml.html.fromstring(cont)
        title = tree.cssselect('div.prodDetail div.clearfix div[style] div[style=font-size: 20px; font-weight: 900;]')[0].text_content()
        listprice = tree.cssselect('div.prodDetail div.clearfix div[style] div.clearfix div[style] span.product-price-prev')[0]
        price = tree.cssselect('div.prodDetail div.clearfix div[style] div.clearfix div[style] span.product-price')[0]

        soldout = tree.cssselect('div#product-detail-wrapper div#product-images div#img-div div.soldout-wrapper')
        soldout = True if soldout else False

        if prd.title.encode('utf-8').lower() != title.lower():
            print 'beyondtherack product[{0}] title error: [{1} vs {2}]'.format(url, prd.title.encode('utf-8'), title)
        if listprice and prd.listprice.replace('$', '').replace(',', '').strip() != listprice:
            print 'beyondtherack product[{0}] listprice error: [{1} vs {2}]'.format(url, prd.listprice.replace('$', '').replace(',', '').strip(), listprice)
            prd.listprice = listprice
            prd.update_history.update({ 'listprice': datetime.utcnow() })
            prd.save()

        if prd.price.replace('$', '').replace(',', '').strip() != price:
            print 'beyondtherack product[{0}] price error: [{1} vs {2}]'.format(url, prd.price.replace('$', '').replace(',', '').strip(), price)
            prd.price = price
            prd.update_history.update({ 'price': datetime.utcnow() })
            prd.save()

        if prd.soldout != soldout:
            print 'beyondtherack product[{0}] soldout error: [{1} vs {2}]'.format(url, prd.soldout, soldout)
            prd.soldout = soldout
            prd.update_history.update({ 'soldout': datetime.utcnow() })
            prd.save()


    def check_offsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nbeyondtherack {0}, {1}\n\n'.format(id, url)
            return

        cont = self.net.fetch_product_page(url)
        if cont == -302:
            return
        elif cont is None or isinstance(cont, int):
            cont = self.net.fetch_product_page(url)
            if cont is None or isinstance(cont, int):
                print '\n\nbeyondtherack product[{0}] download error.\n\n'.format(url)
                return
        else:
            tree = lxml.html.fromstring(cont)
            tt = tree.cssselect('#eventTTL')[0].get('eventttl')
            products_end = datetime.utcfromtimestamp(tt)
            if not prd.products_end or prd.products_end < products_end:
                print '\n\nbeyondtherack product[{0}] on sale again.'.format(url)
                prd.products_end = products_end
                prd.update_history.update({ 'products_end': datetime.utcnow() })
                prd.on_again = True
                prd.save()



    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

if __name__ == '__main__':
    CheckServer().check_onsale_product('','')
