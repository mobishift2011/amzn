#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ethan <ethan@favbuy.com>

"""
crawlers.saksfifthavenue.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.
"""
from crawlers.common.stash import *
from crawlers.common.events import common_saved, common_failed
from models import Category, Product
from deals.picks import Picker
import requests
import lxml.html
import traceback
from datetime import datetime
import re

header = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip,deflate,sdch',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Host':'www.saksfifthavenue.com',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22'
}
HOST = 'http://%s' % header['Host']
req = requests.Session(config=config, headers=header)

class Server(object):
    def crawl_category(self, ctx='', **kwargs):
        res = requests.get(HOST)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)
        primary_cat_nodes = tree.cssselect('div.nav ul.menu li.menu-column')

        for primary_cat_node in primary_cat_nodes:
            primary_cat = primary_cat_node.cssselect('a.menu-column-link')[0].text.strip()
            if primary_cat and 'designer' in primary_cat.lower():
                continue
            sub_cat_nodes = primary_cat_node.cssselect('ul.sub-menu li.sub-menu-column ul li a')

            for sub_cat_node in sub_cat_nodes:
                sub_cat = sub_cat_node.text.strip()
                combine_url = sub_cat_node.get('href')
                key = re.sub(HOST, '', combine_url)
                key = re.sub('/', '_', key)

                is_new = False; is_updated = False
                category = Category.objects(key=key).first()

                if not category:
                    is_new = True
                    category = Category(key=key)
                    category.is_leaf = True

                if primary_cat not in category.cats:
                    category.cats.append(primary_cat)
                    is_updated = True

                if combine_url and combine_url != category.combine_url:
                    category.combine_url = combine_url
                    is_updated = True

                category.hit_time = datetime.utcnow()
                category.save()
                
                # print category.key; print category.cats; print category.combine_url; print is_new; print is_updated; print

                common_saved.send(sender=ctx, obj_type='Category', key=category.key, url=category.combine_url, \
                    is_new=is_new, is_updated=((not is_new) and is_updated) )

    def crawl_listing(self, url, ctx='', **kwargs):
        res = requests.get(url, params={'Ns': 'P_sale_flag|1'})
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)

        category = Category.objects(key=kwargs.get('key')).first()
        if not category:
            print 'Category does not exist'
            common_failed.send(sender=ctx, url=url, reason='Category does not exist -> {0} .'.format(kwargs))
            return

        product_nodes = tree.cssselect('div#product-container div');
        no_discount_num = 0 # sometimes no discount product occurs between the  discount ones ordered by sale.

        for product_node in product_nodes:
            if not product_node.get('id') or 'product' not in product_node.get('id').lower():
                continue

            key = product_node.get('id')
            info_node = product_node.cssselect('div.product-text a')[0]
            price = None; listprice = None
            listprice_node = info_node.cssselect('span.product-price')
            price_node = info_node.cssselect('span.product-sale-price')
            if listprice_node:
                listprice = ''.join(listprice_node[0].xpath('.//text()')).strip()
            if price_node:
                price = ''.join(price_node[0].xpath('.//text()')).strip()

            if price is None or listprice is None:
                no_discount_num += 1
                if no_discount_num < 3:
                    continue
                return
            no_discount_num = 0

            brand = info_node.cssselect('p span.product-designer-name')[0].text
            if brand:
                brand = brand.strip()
            title = info_node.cssselect('p.product-description')[0].text.strip()
            combine_url = info_node.get('href')

            is_new = False; is_updated = False
            product = Product.objects(key=key).first()
            if not product:
                is_new = True
                product = Product(key=key)
                product.updated = False
                product.event_type = False

            if title and title != product.title:
                product.title = title
                is_updated = True
                product.update_history['title'] = datetime.utcnow()

            if brand and brand != product.brand:
                product.brand = brand
                is_updated = True

            if combine_url and combine_url != product.combine_url:
                product.combine_url = combine_url
                is_updated = True
                product.update_history['combine_url'] = datetime.utcnow()

            if price and price != product.price:
                product.price = price
                is_updated = True

            if listprice and listprice != product.listprice:
                product.listprice = listprice
                is_updated = True

            if category.cats and set(category.cats).difference(product.dept):
                product.dept = list(set(category.cats) | set(product.dept or []))
                is_updated = True

            if category.key not in product.category_key:
                product.category_key.append(category.key)
                is_updated = True

            if is_updated:
                product.list_update_time = datetime.utcnow()
            
            # To pick the product which fit our needs, such as a certain discount, brand, dept etc.
            selected = Picker(site='saksfifthavenue').pick(product)
            if not selected:
                continue

            product.hit_time = datetime.utcnow()
            product.save()
            
            # print product.brand; print product.title; print product.combine_url; print product.listprice, ' / ', product.price; print is_new; print is_updated
            # print

            common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, \
                is_new=is_new, is_updated=((not is_new) and is_updated) )

        # Go to the next page to keep on crawling.
        next_page = None
        page_nodes = tree.cssselect('div.pagination-container ol.pa-page-number li a')
        for page_node in page_nodes:
            if page_node.get('class') == 'next':
                href = page_node.get('href')
                match = re.search(r'https?://.+', href)
                next_page = href if match else '{0}/{1}'.format(HOST, href)
                break

        if next_page:
            print next_page
            self.crawl_listing(url=next_page, ctx=ctx, **kwargs)

    def crawl_product(self, url, ctx='', **kwargs):
        key = kwargs.get('key')
        product = Product.objects(key=key).first()

        if not product:
            common_failed.send(sender=ctx, url=url, reason='Product does not exist -> {0} .'.format(kwargs))
            return

        res = requests.get(url)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)
        
        image_urls = []
        pid = key.split('-')[-1]
        pic_modes = ('_ASTL', '', '_A1')

        for pic_mode in pic_modes:
            image_url = 'http://s7d9.scene7.com/is/image/saks/{0}{1}?scl=1'.format(pid, pic_mode)
            image_res = requests.get(image_url)
            try:
                image_res.raise_for_status()
                if image_url not in image_urls:
                    image_urls.append(image_url)
            except:
                continue

        info_node = tree.cssselect('div.pdp-item-container div.pdp-reskin-general-info')[0]
        brand = info_node.cssselect('h1.brand')[0].text.strip()
        try:
            title = info_node.cssselect('h2.description')[0].text.strip()
        except:
            title = None
        list_info_node = tree.cssselect('div.productCopy-container table tr td span#api_prod_copy1')[0]
        list_info = [li.text.strip() for li in list_info_node.cssselect('ul li')]

        # update product
        is_new = False; is_updated = False; ready = False

        if image_urls and image_urls != product.image_urls:
            product.image_urls = image_urls
            is_updated = True
            product.update_history['image_urls'] = datetime.utcnow()

        if brand and not product.brand:
            product.brand = brand
            is_updated = True

        if title and not product.title:
            product.title = title
            is_updated = True
            product.update_history['title'] = datetime.utcnow()

        if list_info and list_info != product.list_info:
            product.list_info = list_info
            is_updated = True
        
        if is_updated:
            if not product.updated:
                ready = True
            
            product.updated = True
            product.full_update_time = datetime.utcnow()
            product.save()

        common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, \
            is_new=is_new, is_updated=((not is_new) and is_updated), ready=ready)

        print product.dept
        print product.image_urls
        print product.brand
        print product.title
        print list_info
        print is_new
        print is_updated
        print ready
        print product.updated
        print



if __name__ == '__main__':
    # import zerorpc
    # from settings import CRAWLER_PORT
    # server = zerorpc.Server(Server())
    # server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
    # server.run()

    s = Server()
    # s.crawl_category()

    # categories = Category.objects()
    # for category in categories:
    #     print category.combine_url
    #     s.crawl_listing(url=category.combine_url, **{'key': category.key})
    #     print
    #     break
    
    for product in Product.objects():
        print product.combine_url
        print product.key
        s.crawl_product(product.combine_url, **{'key': product.key})
        break