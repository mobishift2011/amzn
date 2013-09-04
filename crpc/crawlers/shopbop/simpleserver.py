#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
from datetime import datetime
from server import req
from models import Product


class CheckServer(object):
    def __init__(self):
        pass

    def fetch_page(self, url):
        ret = req.get(url)
        if ret.ok: return ret.content
        else: return ret.status

    def check_onsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nshopbop {0}, {1}\n\n'.format(id, url)
            return

        ret = self.fetch_page(url)
        if isinstance(ret, int):
            print("\n\nshopbop download product page error: {0}".format(url))
            return

        tree = lxml.html.fromstring(ret)

        listprice = price = None
        for price_node in tree.cssselect('div#productPrices div.priceBlock'):
            if price_node.cssselect('span.salePrice'):
                price = price_node.cssselect('span.salePrice')[0].text_content().replace(',', '').replace('$', '').strip()
            elif price_node.cssselect('span.originalRetailPrice'):
                listprice = price_node.cssselect('span.originalRetailPrice')[0].text_content().replace(',', '').replace('$', '').strip()

        soldout = True if tree.cssselect('img#soldOutImage') else False

        if listprice and prd.listprice != listprice:
            prd.listprice = listprice
            prd.update_history.update({ 'listprice': datetime.utcnow() })
        if prd.price != price:
            prd.price = price
            prd.update_history.update({ 'price': datetime.utcnow() })
        if prd.soldout != soldout:
            prd.soldout = soldout
            prd.update_history.update({ 'soldout': datetime.utcnow() })
        prd.save()


    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

import slumber
from settings import MASTIFF_HOST
class Publish(object):
    def __init__(self):
        self.api = slumber.API(MASTIFF_HOST)

    def publish_old_stuff(self):
        for prd in Product.objects():
            if prd.publish_time is None or 'soldout' not in prd.update_history or prd.publish_time < prd.update_history['soldout']:
                self.api.product(prd.id).patch({'sold_out': prd.soldout})
                prd.publish_time = datetime.utcnow()
                prd.save()


if __name__ == '__main__':
#    check_onsale_product('845524441951543', 'http://www.shopbop.com/maya-ballet-flat-rag-bone/vp/v=1/845524441951543.htm')

    import traceback
    from gevent.pool import Pool
    try:
        from crawlers.common.onoff_routine import spout_obj
        import os, sys

        method = sys.argv[1] if len(sys.argv) > 1 else 'check_onsale_product'
        pool = Pool(10)
        for product in spout_obj(os.path.split(os.path.abspath(__file__+'/../'))[-1], method):
            pool.spawn(getattr(CheckServer(), method), product.get('id'), product.get('url'))
            pool.join()
    except:
        print traceback.format_exc()
