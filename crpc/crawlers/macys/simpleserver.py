#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
from datetime import datetime
from server import fetch_macys_page


class CheckServer(object):
    def __init__(self):
        pass


    def check_onsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nebags {0}, {1}\n\n'.format(id, url)
            return

        ret = fetch_macys_page(url)
        if isinstance(ret, int):
            print("\n\nmacys download product page error: {0}".format(url))
            return

        tree = lxml.html.fromstring(ret)
        price = None; listprice = None
        for price_node in tree.cssselect('div#priceInfo span'):
            if  price_node.get('class') and 'priceSale' in price_node.get('class'):
                price = price_node.xpath('text()')[-1].strip()
            else:
                if listprice is None:
                    listprice = price_node.text.strip() if price_node.text else listprice
        if price is None or listprice is None:
            return
        price = re.compile('[^\d]*(\d+\.?\d*)').match(price).group(1)
        price = price.replace('Sale', '').replace('Your Choice', '').replace('Now', '').replace('$', '').replace(',', '').strip()
        listprice = re.compile('[^\d]*(\d+\.?\d*)').match(listprice).group(1)
        listprice = listprice.replace('Reg.', '').replace('Orig.', '').replace('$', '').replace(',', '').strip()
        if price != prd.price:
            prd.price = price
            prd.update_history.update({ 'price': datetime.utcnow() })
        if listprice != prd.listprice:
            prd.listprice = listprice
            prd.update_history.update({ 'listprice': datetime.utcnow() })

        prd.save()




    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass


if __name__ == '__main__':
    pass

