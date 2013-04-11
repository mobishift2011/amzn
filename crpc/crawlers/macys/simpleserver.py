#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

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



    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass


if __name__ == '__main__':
    pass

