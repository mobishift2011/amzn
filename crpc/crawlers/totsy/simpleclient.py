#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
from datetime import datetime

from server import totsyLogin
from models import Product

class CheckServer(object):
    def __init__(self):
        self.net = totsyLogin()
        self.net.check_signin()

    def check_onsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\ntotsy {0}, {1}\n\n'.format(id, url)
            return

        cont = self.net.fetch_page(url)
        if isinstance(cont, int):
            print '\n\ntotsy product[{0}] download error: {1} \n\n'.format(url, cont)
            return


    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

if __name__ == '__main__':
    pass
