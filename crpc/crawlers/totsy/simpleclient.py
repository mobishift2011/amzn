#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import slumber
import lxml.html
from datetime import datetime

from server import totsyLogin
from models import Product
from settings import MASTIFF_HOST

api = slumber.API(MASTIFF_HOST)

class CheckServer(object):
    def __init__(self):
        self.net = totsyLogin()
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
            print '\n\ntotsy {0}, {1}\n\n'.format(id, url)
            return

        cont = self.net.fetch_page(url)
        if cont == 404:
            if prd.muri:
                self.offsale_update(prd.muri)
            if not prd.products_end or prd.products_end > datetime.utcnow():
                prd.products_end = datetime.utcnow()
                prd.update_history.update({ 'products_end': datetime.utcnow() })
                prd.save()
            print '\n\ntotsy product[{0}] redirect, sale end.\n\n'.format(url)
        elif isinstance(cont, int):
            print '\n\ntotsy product[{0}] download error: {1} \n\n'.format(url, cont)
            return

        tree = lxml.html.fromstring(cont)
        node = tree.cssselect('section#pageheader div.row div.product-main')[0]
        title = node.cssselect('div.page-header h3')[0].text_content().encode('utf-8')
        info = node.cssselect('div.product-addtocart form#product_addtocart_form div#product-main-info')[0]
        soldout = True if info.cssselect('div.availability') else False
        price = info.cssselect('div.product-prices div.product-prices-main div.price-box span.special-price')[0].text_content().replace('$', '').strip()
        listprice = info.cssselect('div.product-prices div.product-prices-main div.product-price-was')[0].text_content().replace('Was', '').replace('$', '').strip()

        if prd.title.encode('utf-8').lower() != title.lower():
            print 'totsy product[{0}] title error: {1} vs {2}'.format(url, prd.title.encode('utf-8'), title)
        if prd.soldout != soldout:
            print 'totsy product[{0}] soldout error: {1} vs {2}'.format(url, prd.soldout, soldout)
        if prd.price.replace('$', '').strip() != price:
            print 'totsy product[{0}] price error: {1} vs {2}'.format(url, prd.price.replace('$', '').strip(), price)
        if prd.listprice.replace('$', '').strip() != listprice:
            print 'totsy product[{0}] listprice error: {1} vs {2}'.format(url, prd.listprice.replace('$', '').strip(), listprice)



    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

if __name__ == '__main__':
    CheckServer().check_onsale_product('orthaheel-cecilia-952045', 'http://www.totsy.com/sales/orthaheel-dr-weil-by-orthaheel-8018/orthaheel-cecilia-952045.html')
    pass
