#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
from datetime import datetime

from models import *
from crawlers.common.stash import *

header = {
    'Host': 'www.shopbop.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Ubuntu Chromium/25.0.1364.160 Chrome/25.0.1364.160 Safari/537.22',
}

req = requests.Session(prefetch=True, timeout=30, config=config, headers=header)

class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.shopbop.com/'

    def crawl_category(self, ctx='', **kwargs):
        ret = req.get(self.siteurl).content
        top_nodes = ret.cssselect('ul#navList li.navCategory')
        for node in top_nodes:
            dept = node.cssselect('a')[0].text_content().strip()
            if dept == 'Designers':
                link = node.cssselect('a')[0].get('href')
                link = link if link.startswith('http') else self.siteurl + link
                self.save_category('designers', link, [dept], ctx)
                continue
            if dept = 'Sale':
                link = node.cssselect('a')[0].get('href')
                link = link if link.startswith('http') else self.siteurl + link
                key = link.rsplit('/', 1)[-1].split('.')[0]
                self.save_category('sale', link, [dept], ctx)
                continue

            sub_nodes = node.cssselect('ul.submenu li.menuItem a')
            for sub in sub_nodes:
                link = sub.get('href')
                link = link if link.startswith('http') else self.siteurl + link
                sub_dept = sub.text_content().strip()
                key = link.rsplit('/', 1)[-1].split('.')[0]
                self.save_category(key, link, [dept, sub_dept], ctx)


    def save_category(self, key, combine_url, cats, ctx):
        is_new = is_updated = False
        category = Category.objects(key=key).first()
        if not category:
            is_new = True
            category = Category(key=key)
            category.is_leaf = True
        category.cats = cats
        category.combine_url = combine_url
        category.save()
        common_saved.send(sender=ctx, obj_type='Category', key=key, url=combine_url, is_new=is_new, is_updated=is_updated)


    def crawl_listing(self, url, ctx='', **kwargs):
        pass

    def crawl_product(self, url, ctx='', **kwargs):
        pass
