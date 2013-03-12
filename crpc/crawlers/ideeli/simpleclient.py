#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import re
import json
import lxml.html

from server import ideeliLogin, req
from models import Product

class CheckServer(object):
    def __init__(self):
        self.size_scarcity = re.compile("SkuBasedRemainingItems\({\s*url: function\(\) { return '(.+)' },")
        self.getids = re.compile('http://www.ideeli.com/events/(\d+)/offers/(\d+)/latest_view/')
        self.net = ideeliLogin()
        self.net.check_signin()


    def check_onsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nideeli {0}, {1}\n\n'.format(id, url)
            return

        cont = self.net.fetch_product_page(url)
        if isinstance(cont, int):
            cont = self.net.fetch_product_page(url)
            if isinstance(cont, int):
                print '\n\nideeli product[{0}] download error.\n\n'.format(url)
                return

        returl, cont = cont
        tree = lxml.html.fromstring(cont)
        try:
            title = tree.cssselect('div#offer_price div.info div.name_container div.name span.product_name')[0].text_content().encode('utf-8')
        except:
            self.net.login_account()
            cont = self.net.fetch_product_page(url)
            tree = lxml.html.fromstring(cont[1])
            try:
                title = tree.cssselect('div#offer_price div.info div.name_container div.name span.product_strapline')[0].text_content().encode('utf-8')
            except:
                print '\n\n%s, %s \n\n' % (cont[0], url)
                open('a.html', 'w').write(ret.content)
        price = tree.cssselect('div#offer_price div.info div.name_container div.price_container span.price')[0].text_content().replace('$', '').replace(',', '').strip()
        if not price:
            node = tree.cssselect('div#sizes_container_{0} div.sizes div.size_container'.format(id))[0]
            price = node.get('data-type-price').replace('$', '').replace(',', '').strip()
            listprice = node.get('data-type-msrp').replace('$', '').replace(',', '').strip()
        else:
            listprice = tree.cssselect('div#offer_price div.info div.name_container div.price_container span.msrp_price')[0].text_content().replace('$', '').replace(',', '').strip()

        sizes = []
        for ss in tree.cssselect('div#sizes_container_{0} div.sizes div.size_container'.format(id)):
            sizes.append( ss.get('data-type-skuid') )
        id1, id2 = self.getids.match(returl).groups()
        link = 'http://www.ideeli.com/events/{0}/offers/{1}/refresh_sale?force_cache_write=1'.format(id1, id2)
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
        if prd.listprice.replace('$', '').replace(',', '').strip() != listprice:
            print 'ideeli product[{0}] listprice error: {1}, {2}'.format(prd.combine_url, prd.listprice.replace('$', '').replace(',', '').strip(), listprice)
        if prd.title.encode('utf-8').lower() != title.lower():
            print 'ideeli product[{0}] title error: {1}, {2}'.format(prd.combine_url, prd.title.encode('utf-8'), title)
        if prd.soldout != soldout:
            print 'ideeli product[{0}] soldout error: {1}, {2}'.format(prd.combine_url, prd.soldout, soldout)


    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

if __name__ == '__main__':
    CheckServer().check_onsale_product('2968718', 'http://www.ideeli.com/events/110518/offers/5862198/latest_view/2968718')
