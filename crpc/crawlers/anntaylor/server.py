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
            node.cssselect('')


    def crawl_listing(self, url, ctx='', **kwargs);
        pass

    def crawl_product(self, url, ctx='', **kwargs);
        pass

if __name__ == '__main__':
    ss = Server()
