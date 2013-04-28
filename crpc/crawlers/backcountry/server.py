#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import requests
import json
import lxml.html
from datetime import datetime

from models import *
from crawlers.common.stash import *
from crawlers.common.events import common_saved, common_failed
from deals.picks import Picker
from powers.pipelines import unescape

req = requests.Session(prefetch=True, timeout=30, config=config, headers=headers)

class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.backcountry.com'
        self.mobileurl = 'http://m.backcountry.com'

    def crawl_category(self, ctx='', **kwargs):
        ret = req.get(self.mobileurl)

        tree = lxml.html.fromstring(ret.content)
        for node in tree.cssselect('div.page div.body article.homepage section.stretch'):
            path = node.cssselect('div.hd')[0].text_content().strip()
            for sub_node in node.cssselect('div.bd section.stretch'):
                sub_path = sub_node.cssselect('div.hd')[0].text_content().strip()
                for leaf in sub_node.cssselect('div.bd ul.list1 li'):
                    link = leaf.cssselect('a')[0].get('href')
                    title = leaf.cssselect('a')[0].text_content().strip()
                    cats = [path, sub_path, title]
                    if title.startswith('All'):
                        self.crawl_leaf_category(link, cats, ctx)


    def crawl_leaf_category(self, link, cats, ctx):
        ret = req.get(link)
        tree = lxml.html.fromstring(ret.content)
        for node in tree.cssselect('div.body article.categories section.stretch'):
            path = node.cssselect('div.hd h2.category-title')[0].text_content()
            for leaf in node.cssselect('div.bd ul.list1 li'):
                url = leaf.cssselect('a')[0].get('href')
                title = leaf.cssselect('a')[0].text_content().strip()
                if title.startswith('All'):
                    key = url.rsplit('/', 1)[-1]
                    cats.append(title)

                    is_new = is_updated = False
                    category = Category.objects(key=key).first()
                    if not category:
                        is_new = True
                        category = Category(key=key)
                        category.is_leaf = True

                    if category.combine_url != url:
                        category.combine_url = url 
                        is_updated = True
                    if set(cats).difference(category.cats):   
                        category.cats = cats
                        is_updated = True

                    category.update_time = datetime.utcnow()
                    category.save()
                    common_saved.send(sender=ctx, obj_type='Category', key=category.key, url=category.combine_url, \
                                        is_new=is_new, is_updated=((not is_new) and is_updated) )

    def crawl_listing(self, url, ctx='', **kwargs):

        category_key = url.rsplit('/', 1)[-1]
        category = Category.objects(key=category_key).first()

        ret = req.get(url)
        tree = lxml.html.fromstring(ret.content)
        num = int( tree.cssselect('span#prod_total')[0].text_content() )
        page = (num - 1) // 60 + 1
        cat = tree.cssselect('input#cat')[0].get('value')
        subcat = tree.cssselect('input#subcat')[0].get('value')

        for i in xrange(page):
            link = 'http://m.backcountry.com/store/group/ajax/get_results.html?cat={0}&offset={1}&subcat={2}'.format(cat, i, subcat)
            ret = req.get(link)
            try:
                js = json.loads(ret.content.decode('utf-8', 'ignore'))
            except Exception as e:
                js = json.loads( unescape(ret.content.decode('utf-8', 'ignore')).replace('\t', '') )
            for prd in js['products']:
                brand = prd['brand_name']
                listprice = prd['full_price'].replace('$', '').replace(',', '')
                if 'lowest_price' not in prd:
                    continue
                price = prd['lowest_price'].replace('$', '').replace(',', '')
                combine_url = prd['url']
                title = unescape( prd['title'] )
                key = combine_url.rsplit('/', 1)[-1]

                is_new = is_updated = False
                product = Product.objects(key=key).first()
                if not product:
                    is_new = True
                    product = Product(key=key)
                    product.event_type = False
                    product.updated = False

                if title != product.title:
                    product.title = title
                    product.update_history.update({ 'title': datetime.utcnow() })
                    is_updated = True

                if combine_url != product.combine_url:
                    product.combine_url = combine_url
                    product.update_history.update({ 'combine_url': datetime.utcnow() })
                    is_updated = True

                if price != product.price:
                    product.price = price
                    is_updated = True

                if listprice != product.listprice:
                    product.listprice = listprice
                    is_updated = True

                selected = Picker(site=DB).pick(product)
                if not selected:                                                                                
                    continue

                if category.key not in product.category_key:
                    product.category_key.append(category.key)
                    is_updated = True

                if is_updated:
                    product.list_update_time = datetime.utcnow()

                product.save()
                common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url,
                        is_new=is_new, is_updated=((not is_new) and is_updated) )


    def crawl_product(self, url, ctx='', **kwargs):
        url = url.replace('www.backcountry.com', 'm.backcountry.com')
        ret = req.get(url)
        tree = lxml.html.fromstring(ret.text)
        summary = tree.cssselect('article.product section.description div.bd')[0].text_content().strip()
        list_info = tree.cssselect('article.product section.details div.bd dl.specs')[0].text_content().replace(':\n',':').split('\n')
        list_info = [i.strip() for i in list_info if i.strip()]
        image = tree.cssselect('article.product p.media-photo a.media-zoom')[0].get('href')
        image_urls = [image]

        key = url.rsplit('/', 1)[-1]
        is_new = is_updated = False
        product = Product.objects(key=key).first()
        if not product:
            is_new = True
            product = Product(key=key)
            product.event_type = False

        product.summary = summary
        product.list_info = list_info
        product.image_urls = image_urls

        if product.updated == False:
            product.updated = True
            ready = True
        else: ready = False
        product.full_update_time = datetime.utcnow()
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=url, is_new=is_new, is_updated=is_updated, ready=ready)


if __name__ == '__main__':
    ss = Server()
    ss.crawl_listing('http://m.backcountry.com/mens-t-shirts')
