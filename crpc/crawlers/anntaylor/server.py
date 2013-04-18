#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import requests
import lxml.html
from datetime import datetime

from models import *

class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.anntaylor.com'

    def crawl_category(self, ctx='', **kwargs):
        ret = requests.get(self.siteurl)
        tree = lxml.html.fromstring(ret.content)
        for node in tree.cssselect('div#main-hd div#nav-site ul.list-l1 li'):
            dept_name = node.cssselect('div.changeCategorys')[0].text_content().replace('AT', '').strip()
            for node_l2 in node.cssselect('div.wrapper-l2 ul.list-l2 li'):
                link = node_l2.cssselect('a')[0].get('href')
                name = node_l2.cssselect('a')[0].text_content().replace('AT', '').strip()

                is_new = is_updated = False
                category = Category.objects(key=link.rsplit('/', 1)).first()
                if not category:
                    is_new = True
                    category = Category(key = link.rsplit('/', 1))
                    category.is_leaf = True



    def crawl_listing(self, url, ctx='', **kwargs);
        pass

    def crawl_product(self, url, ctx='', **kwargs);
        pass

if __name__ == '__main__':
    ss = Server()
