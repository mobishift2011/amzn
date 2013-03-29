#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from server import req


class CheckServer(object):
    def __init__(self):
        pass

    def fetch_page(self, url):
        ret = req.get(url)
        if ret.url.startswith('http://www.ebags.com/error/unknown'):
            return -404
        if ret.ok: return ret.content
        else: return ret.status

    def check_onsale_product(self, id, url):
        return
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nebags {0}, {1}\n\n'.format(id, url)
            return

        ret = self.fetch_page(url)
        if isinstance(ret, int):
            print("\n\nebags download product page error: {0}".format(url))
            return



    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass


if __name__ == '__main__':
    pass

