#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html

class Server(object):
    def __init__(self):
        pass

    def crawl_category(self, ctx=''):
        pass

    def crawl_listing(self, url, ctx=''):
        tree = lxml.html.fromstring(content)
        nodes = tree.cssselect('div#page > div.container-content > div.product-wrapper div.product')

    def crawl_product(self, url, ctx=''):
        pass
