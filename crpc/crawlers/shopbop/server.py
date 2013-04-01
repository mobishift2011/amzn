#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
from datetime import datetime

from models import *
from crawlers.common.stash import *
from crawlers.common.events import common_failed, common_saved

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,en-US;q=0.8,en;q=0.6',
    'Host': 'www.shopbop.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Ubuntu Chromium/25.0.1364.160 Chrome/25.0.1364.160 Safari/537.22',
}

req = requests.Session(prefetch=True, timeout=30, config=config, headers=header)

class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.shopbop.com/'

    def fetch_page(self, url):
        ret = req.get(self.siteurl)
        if ret.ok: return ret.content
        else: return ret.status_code

    def crawl_category(self, ctx='', **kwargs):
        ret = self.fetch_page(self.siteurl)
        if isinstance(ret, int):
            common_failed.send(sender=ctx, key='', url=self.siteurl,
                    reasone='download home page error: {0}'.format(ret))
            print ret, '--'
            return
        tree = lxml.html.fromstring(ret)
        top_nodes = tree.cssselect('ul#navList li.navCategory')
        for node in top_nodes:
            dept = node.cssselect('a')[0].text_content().strip()
            if dept == 'Designers':
                link = node.cssselect('a')[0].get('href')
                link = link if link.startswith('http') else self.siteurl + link
                self.save_category('designers', link, [dept], ctx)
                continue
            if dept == 'Sale':
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

if __name__ == '__main__':
    ss = Server()
    ss.crawl_category()
