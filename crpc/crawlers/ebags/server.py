#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import re
import requests
import lxml.html
from datetime import datetime

from crawlers.common.stash import *
from crawlers.common.events import common_saved, common_failed
from models import Category, Product

header = {
    'Host': 'www.ebags.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Ubuntu Chromium/25.0.1364.160 Chrome/25.0.1364.160 Safari/537.22',
}

req = requests.Session(prefetch=True, timeout=30, config=config, headers=header)

class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.ebags.com'

    def fetch_page(self, url):
        ret = req.get(url)
        if ret.ok: return ret.content
        else: return ret.status

    def crawl_category(self, ctx='', **kwargs):
        ret = self.fetch_page(self.siteurl)
        if isinstance(ret, int):
            common_failed.send(sender=ctx, key='', url=self.siteurl,
                    reason='download home page failed: {0}'.format(ret))
        tree = lxml.html.fromstring(ret)
        nodes = tree.cssselect('div#main div#navWrap ul#navCon > li')
        k_link = {}
        for node in nodes:
            try:
                link = node.cssselect('a.sliderNav')[0].get('href')
            except IndexError:
                # the last one is: Shop All Departments
                continue
            link = link if link.startswith('http') else self.siteurl + link
            key = re.compile('.+/department/(.+)\?origin=flyaway').match(link).group(1)
            k_link[key] = link

        for key, link in k_link.iteritems():
            ret = self.fetch_page(link)
            if isinstance(ret, int):
                common_failed.send(sender=ctx, key=key, url=link,
                        reason='download category page error: {0}'.format(ret))
            tree = lxml.html.fromstring(ret)
            list_node = tree.cssselect('#lnkSeeAllDepartment')[0]
            num = list_node.cssselect('span')[0].text_content().strip()
            num = int( re.compile('\((\d+)\)').match(num).group(1) )
            link = list_node.get('href')
            if 'category' not in link: continue
            link = link if link.startswith('http') else self.siteurl + link

            is_new = is_updated = False
            category = Category.objects(key=key).first()
            if not category:
                is_new = True
                category = Category(key=key)
                category.is_leaf = True
                category.combine_url = link
                category.cats = [key]
                category.pagesize = 144
            category.num = num
            category.update_time = datetime.utcnow()
            category.save()
            common_saved.send(sender=ctx, obj_type='Category', key=key, url=link, is_new=is_new, is_updated=is_updated)


    def crawl_listing(self, url, ctx='', **kwargs):
        ret = self.fetch_page(url)
        if isinstance(ret, int):
            common_failed.send(sender='ctx', key='', url=url,
                    reason="download listing page error: {0}".format(ret))
        tree = lxml.html.fromstring(ret)
        nodes = tree.cssselect('div.mainCon div.ProductListWrap div.thisResultItem')
        for node in nodes:
            node.cssselect('')

    def crawl_product(self, url, ctx='', **kwargs):
        pass

if __name__ == '__main__':
    Server().crawl_category()
