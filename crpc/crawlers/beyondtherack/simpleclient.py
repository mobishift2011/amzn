#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
import slumber
from datetime import datetime

from server import beyondtherackLogin
from models import Product, Event

from settings import MASTIFF_HOST
from mongoengine import *
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
            if not prd.muri: return
            _id = prd.muri.rsplit('/', 2)[-2]
            if not prd.products_end or 'products_end' not in prd.update_history:
                if prd.products_end:
                    prd.update_history.update({ 'products_end': prd.products_end })
                    api.product(_id).patch({ 'ends_at': prd.products_end.isoformat() })
                else:
                    _now = datetime.utcnow()
                    prd.products_end = _now
                    prd.update_history.update({ 'products_end': _now })
                    api.product(_id).patch({ 'ends_at': datetime.utcnow().isoformat() })
            elif prd.publish_time and prd.update_history['products_end'] > prd.publish_time:
                api.product(_id).patch({ 'ends_at': prd.products_end.isoformat() })
                prd.publish_time = prd.products_end
            prd.save()
            return
        elif cont is None or isinstance(cont, int):
            cont = self.net.fetch_product_page(url)
            if cont is None or isinstance(cont, int):
                print '\n\nbeyondtherack product[{0}] download error.\n\n'.format(url)
                return
        else:
            tree = lxml.html.fromstring(cont)
            try: # only have style. 'EVENT HAS ENDED'
                tt = tree.cssselect('#eventTTL')[0].get('eventttl')
            except IndexError:
                return

            products_end = datetime.utcfromtimestamp( float(tt) )
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
    check = CheckServer()

    a = Product.objects(products_end__lt=datetime(year=2013, month=3, day=1))
    b = Product.objects(Q(products_end__lt=datetime(year=2013, month=4, day=1)) & Q(products_end__gt=datetime(year=2013, month=3, day=1)))
    c = Product.objects(Q(products_end__lt=datetime(year=2013, month=5, day=1)) & Q(products_end__gt=datetime(year=2013, month=4, day=1)))
    d = Product.objects(Q(products_end__lt=datetime(year=2013, month=6, day=1)) & Q(products_end__gt=datetime(year=2013, month=5, day=1)))
    e = Product.objects(Q(products_end__lt=datetime(year=2013, month=7, day=1)) & Q(products_end__gt=datetime(year=2013, month=6, day=1))) 
    f = Product.objects(Q(products_end__lt=datetime(year=2013, month=8, day=1)) & Q(products_end__gt=datetime(year=2013, month=7, day=1)))
    g = Product.objects(Q(products_end__lt=datetime(year=2013, month=9, day=1)) & Q(products_end__gt=datetime(year=2013, month=8, day=1)))
    for o in a:
        check.check_offsale_product( o.key, o.url() )
    exit()

    obj = Product.objects.where("function(){ a=this.update_history; if(a){return a.products_end != undefined;}else{return false;}}").timeout(False)
    print 'have {0} off sale event products.'.format(obj.count())
    obj2 = Product.objects(products_end__exists=False).timeout(False)
    print 'have {0} off sale category products.'.format(obj2.count())

    for o in obj:
        check.check_offsale_product( o.key, o.url() )

    for o in obj2:
        check.check_offsale_product( o.key, o.url() )

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
