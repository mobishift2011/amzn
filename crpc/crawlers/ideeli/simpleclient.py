#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import re
import json
import slumber
import lxml.html
from datetime import datetime

from server import ideeliLogin
from models import Product
from settings import MASTIFF_HOST

api = slumber.API(MASTIFF_HOST)

class CheckServer(object):
    def __init__(self):
        self.size_scarcity = re.compile("SkuBasedRemainingItems\({\s*url: function\(\) { return '(.+)' },")
        self.getids = re.compile('http://www.ideeli.com/events/(\d+)/offers/(\d+)/latest_view/')
        self.net = ideeliLogin()
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
            print '\n\nideeli {0}, {1}\n\n'.format(id, url)
            return

        cont = self.net.fetch_product_page(url)
        if cont == -302:
            if prd.muri:
                self.offsale_update(prd.muri)
            print '\n\nideeli product[{0}] redirect to homepage.\n\n'.format(url)
            return
        if isinstance(cont, int):
            cont = self.net.fetch_product_page(url)
            if isinstance(cont, int):
                print '\n\nideeli product[{0}] download error.\n\n'.format(url)
                return

        returl, cont = cont
        tree = lxml.html.fromstring(cont)
        try:
            title = tree.cssselect('div#offer_price div.info div.name_container div.name span.product_strapline')[0].text_content().encode('utf-8')
        except:
            self.net.login_account()
            cont = self.net.fetch_product_page(url)
            if cont[0] == 'https://www.ideeli.com/login':
                print '\n\n%s, %s \n\n' % (cont[0], url)
                return
            tree = lxml.html.fromstring(cont[1])
            title = tree.cssselect('div#offer_price div.info div.name_container div.name span.product_strapline')[0].text_content().encode('utf-8')

        price = tree.cssselect('div#offer_price div.info div.name_container div.price_container span.price')[0].text_content().replace('$', '').replace(',', '').strip()
        if not price:
            try:
                node = tree.cssselect('div#sizes_container_{0} div.sizes div.size_container'.format(id))[0]
            except IndexError:
                node = tree.cssselect("div[id^='sizes_container_'] div.sizes div.size_container")[0]
            price = node.get('data-type-price').replace('$', '').replace(',', '').strip()
            listprice = node.get('data-type-msrp').replace('$', '').replace(',', '').strip()
        else:
            listprice = tree.cssselect('div#offer_price div.info div.name_container div.price_container span.msrp_price')[0].text_content().replace('$', '').replace(',', '').strip()

        sizes = []
        size = tree.cssselect('div#sizes_container_{0} div.sizes div.size_container'.format(id))
        if not size:
            size = tree.cssselect('div[id^="sizes_container_"] div.sizes div.size_container')
        for ss in size:
            sizes.append( ss.get('data-type-skuid') )
        try:
            id1, id2 = self.getids.match(returl).groups()
            link = 'http://www.ideeli.com/events/{0}/offers/{1}/refresh_sale?force_cache_write=1'.format(id1, id2)
        except AttributeError:
            link = tree.cssselect('#refresh_event_path')[0].get('value')
            link = link if link.startswith('http') else 'http://www.ideeli.com' + link
        ret = self.net.fetch_page(link)
        soldout = True
        for sku in sizes:
            avl = re.compile("ideeli.size_selectors.sizes\['size_container_{0}'\].markAs(.+)\(\);".format(sku)).search(ret).group(1)
            if avl == 'Available':
                soldout = False

#        link = self.size_scarcity.search(cont).group(1)
#        link = link if link.startswith('http') else 'http://www.ideeli.com' + link
#        ret = self.net.fetch_page(link)
#        js = json.loads(ret)
#        soldout = True
#        for sku in sizes:
#        sku not in js['skus']
#            if js['skus'][sku] != u'0':
#                soldout = False
#                break

        if prd.price.replace('$', '').replace(',', '').strip() != price:
            print 'ideeli product[{0}] price error: {1}, {2}'.format(prd.combine_url, prd.price.replace('$', '').replace(',', '').strip(), price)
            prd.price = price
            prd.update_history.update({ 'price': datetime.utcnow() })
            prd.save()
        if prd.listprice.replace('$', '').replace(',', '').strip() != listprice:
            print 'ideeli product[{0}] listprice error: {1}, {2}'.format(prd.combine_url, prd.listprice.replace('$', '').replace(',', '').strip(), listprice)
            prd.listprice = listprice
            prd.update_history.update({ 'listprice': datetime.utcnow() })
            prd.save()
        if prd.title.encode('utf-8').lower() != title.lower():
            print 'ideeli product[{0}] title error: {1}, {2}'.format(prd.combine_url, prd.title.encode('utf-8'), title)
        if prd.soldout != soldout:
            print 'ideeli product[{0}] soldout error: {1}, {2}'.format(prd.combine_url, prd.soldout, soldout)
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
    CheckServer().check_onsale_product('3080850', 'http://www.ideeli.com/events/127202/offers/7009630/latest_view/3080850')
