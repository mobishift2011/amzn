#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from server import ventepriveeLogin
from models import Product

class CheckServer(object):
    def __init__(self):
        self.net = ventepriveeLogin()

    def check_onsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nventepricee {0}, {1}\n\n'.format(id, url)
            return

        cont = self.net.fetch_page(url)
        if isinstance(cont, int):
            cont = self.net.fetch_page(url)
            if isinstance(cont, int):
                print '\n\nventeprivee product[{0}] download error.\n\n'.format(url)
                return
        js = cont.json


    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

