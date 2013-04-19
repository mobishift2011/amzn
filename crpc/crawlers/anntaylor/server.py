#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import requests
import lxml.html
from datetime import datetime

from models import *
from crawlers.common.events import common_saved

class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.anntaylor.com'

    def crawl_category(self, ctx='', **kwargs):
        ret = requests.get(self.siteurl)
        tree = lxml.html.fromstring(ret.content)
        print tree.cssselect('div#main-hd div#nav-site ul.list-l1 li')
        for node in tree.cssselect('div#main-hd div#nav-site ul.list-l1 li'):
            dept_name = node.cssselect('div.changeCategorys')[0].text_content().replace('AT', '').strip()
            if dept_name == 'Lookbook': continue
            print dept_name
#            for node_l2 in node.cssselect('div.wrapper-l2 ul.list-l2 li'):
#                link = node_l2.cssselect('a')[0].get('href')
#                link = link if link.startswith('http') else self.siteurl + link
#                name = node_l2.cssselect('a')[0].text_content().replace('AT', '').strip()
#                if name == 'ANN Wedding Swatches Summer': continue
#                cats = [dept_name, name]
#
#                is_new = is_updated = False
#                category = Category.objects(key=link.rsplit('/', 1)[-1]).first()
#                if not category:
#                    is_new = True
#                    category = Category(key = link.rsplit('/', 1)[-1])
#                    category.is_leaf = True
#
#                if category.combine_url != link:
#                    category.combine_url = link
#                    is_updated = True
#                if set(cats).difference(category.cats):
#                    category.cats = cats
#                    is_updated = True
#
#                category.update_time = datetime.utcnow()
#                category.save()
#                common_saved.send(sender=ctx, obj_type='Category', key=category.key, url=category.combine_url,
#                        is_new=is_new, is_updated=((not is_new) and is_updated) )
#

    def crawl_listing(self, url, ctx='', **kwargs):
        pass

    def crawl_product(self, url, ctx='', **kwargs):
        pass

if __name__ == '__main__':
    ss = Server()
    ss.crawl_category()
