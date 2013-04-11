#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ethan <ethan@favbuy.com>

"""
crawlers.nordstrom.server
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

HOST = 'http://shop.nordstrom.com'
header = {
    'Host': HOST,
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0',
}
req = requests.Session(prefetch=True, timeout=25, config=config, headers=header)

class Server(object):
    def __init__(self):
        pass

    def crawl_listing_of_no_leaf(self, page_node, ctx='', **kwargs):
        href_set = set()
        href_nodes = page_node.cssselect('div.main-content-right a')
        for href_node in href_nodes:
            href = href_node.get('href') or ''
            if '/c/' in href:
                match = re.search(r'https?://.+', href)
                if not match:
                    href = 'http://shop.nordstrom.com%s' % (href)
                href_set.add(href)
        for url in href_set:
            print url
            self.crawl_listing(url=url, ctx=ctx, **kwargs)

    def crawl_category(self, ctx='', **kwargs):
        res = requests.get(HOST)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)
        primary_dept_nodes = tree.cssselect('nav#primary-nav > ul li.tab')

        for primary_dept_node in primary_dept_nodes:
            primary_dept = primary_dept_node.cssselect('h2 a span')[0].text
            if primary_dept.lower() == 'brands':
                continue

            sub_dept = None
            sub_dept_nodes = primary_dept_node.cssselect('div.nav-category div.nav-category-column ul li a')
            for sub_dept_node in sub_dept_nodes:
                sub_dept = sub_dept_node.text
                combine_url = sub_dept_node.get('href')
                key = combine_url.split('/')[-1]

                match = re.search(r'https?://.+', combine_url)
                if not match:
                    combine_url = '%s%s' % (HOST, combine_url)

                is_new = False; is_updated = False
                category = Category.objects(key=key).first()

                if not category:
                    is_new = True
                    category = Category(key=key)
                    category.is_leaf = True

                if primary_dept not in category.cats:
                    category.cats.append(primary_dept)
                    is_updated = True

                if sub_dept not in category.cats:
                    category.cats.append(sub_dept)
                    is_updated = True

                if combine_url and ((category.combine_url and combine_url.split('?')[0] != category.combine_url.split('?')[0]) \
                    or not category.combine_url):
                        category.combine_url = combine_url
                        is_updated = True

                category.hit_time = datetime.utcnow()
                category.save()

                common_saved.send(sender=ctx, obj_type='Category', key=category.key, url=category.combine_url, \
                    is_new=is_new, is_updated=((not is_new) and is_updated) )

                # print category.key; print category.cats; print category.combine_url; print is_new; print is_updated; print

    def crawl_listing(self, url, ctx='', **kwargs):
        if url.startswith('http://blogs.nordstrom.com'):
            return
        try:
            res = requests.get(url, params={'sort': 'sale'})
        except requests.exceptions.ConnectionError:
            return

        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)
        listing_node = tree.cssselect('div.fashion-results')

        if listing_node:
            listing_node = listing_node[0]
        else:
            if tree.cssselect('div#brandsIndex'):
                return

            self.crawl_listing_of_no_leaf(tree, ctx=ctx, **kwargs)
            return

        product_nodes = listing_node.cssselect('div.row > div')
        if not product_nodes:
            self.crawl_listing_of_no_leaf(tree, ctx=ctx, **kwargs)
            return
        
        category = Category.objects(key=kwargs.get('key')).first()
        no_discount_num = 0 # sometimes no discount product occurs between the  discount ones ordered by sale.
        for product_node in product_nodes:
            if not product_node.get('id'):
                continue

            key = product_node.get('data-style-id')
            if not key:
                common_failed.send(sender=ctx, url=url, reason='listing product has no data-style-id')
                continue

            try:
                info_node = product_node.cssselect('div.info')[0]
                a_node = info_node.cssselect('a')[0]
                title = a_node.text.strip()

                price = None; listprice = None
                price_nodes = info_node.cssselect(".price")
                for price_node in price_nodes:
                    if 'regular' in price_node.get('class'):
                        listprice = price_node.text
                    elif 'sale' in price_node.get('class'):
                        price = price_node.text
                
                if price is None or listprice is None:
                    no_discount_num += 1
                    if no_discount_num < 3:
                        continue
                    # common_failed.send(sender=ctx, url=url, \
                    #     reason='listing product %s.%s cannot crawl price info -> %s / %s' % (key, title, price, listprice))
                    return

                combine_url = a_node.get('href')
                if not combine_url:
                    common_failed.send(sender=ctx, url=url, reason='listing product %s.%s cannot crawl combine_url' % (key, title))
                    continue

                match = re.search(r'https?://.+', combine_url)
                if not match:
                    combine_url = 'http://shop.nordstrom.com%s' % (combine_url)

            except IndexError:
                print traceback.format_exc()
                common_failed.send(sender=ctx, url=url, reason='listing product %s -> %s' % (key, traceback.format_exc()))
                continue


            is_new = False; is_updated = False
            product = Product.objects(key=key).first()
            if not product:
                is_new = True
                product = Product(key=key)
                product.updated = False
                product.event_type = False

            if combine_url and combine_url != product.combine_url:
                product.combine_url = combine_url
                is_updated = True

            if title and title != product.title:
                product.title = title
                is_updated = True

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
            selected = Picker(site='nordstrom').pick(product)
            if not selected:
                continue

            product.hit_time = datetime.utcnow()
            product.save()
            
            # print product.title
            # print product.combine_url
            # print product.listprice
            # print product.price
            # print is_new
            # print is_updated
            # print

            common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, \
                is_new=is_new, is_updated=((not is_new) and is_updated) )

        # Go to the next page to keep on crawling.
        try:
            arrow_node = tree.cssselect('div.fashion-results-header div.fashion-results-pager ul.arrows li.next')[0]
        except IndexError:
            common_failed.send(sender=ctx, url=url, reason=traceback.format_exc())
            return
        next_page = arrow_node.cssselect('a')[0].get('href') \
            if 'disabled' not in arrow_node.get('class') else None

        if next_page:
            print next_page
            self.crawl_listing(url=next_page, ctx=ctx, **kwargs)

    def crawl_product(self, url, ctx='', **kwargs):
        key = kwargs.get('key')
        product = Product.objects(key=key).first()

        if not product:
            common_failed.send(sender=ctx, url=url, reason='product not exists -> %s' % kwargs)
            return

        res = requests.get(url)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)

        product_node = tree.cssselect('div.product-content')
        if not product_node:
            product_node = tree.cssselect('div.OutfitPage')

        product_node = product_node[0]
        thumbnail_nodes = product_node.cssselect('ul.thumbnails li.fashion-photo img')
        image_urls = [re.sub('Mini', 'Large', thumbnail_node.get('src')) for thumbnail_node in thumbnail_nodes]

        brand_node = product_node.cssselect('div.brand-content ul li a')
        brand = brand_node[0].text.strip() if brand_node else ''

        title_node = product_node.cssselect('div.rightcol h1')
        title = title_node[0].text.strip() if title_node else ''

        listprice = None; price = None
        price_nodes = product_node.cssselect('div#itemNumberPrice ul.itemNumberPriceRow li.price span.price')
        for price_node in price_nodes:
            if 'regular' in price_node.get('class'):
                listprice = price_node.text.strip()
            if 'sale' in price_node.get('class'):
                price = price_node.text.strip()


        shipping = None; returns = None
        ship_and_ret_node = product_node.cssselect('div.shippingDisplay .description')
        if  ship_and_ret_node:
            shipping = ship_and_ret_node[0].text.strip() if ship_and_ret_node[0].text else ''
            returns = shipping

        list_info = []
        descs = product_node.cssselect('div#productdetails #pdList')[0].xpath('.//text()')
        for desc in descs:
            d = re.sub(r'\r|\n|\t', '', desc)
            if d:
                list_info.append(d.strip())

        # update product
        is_new = False; is_updated = False; ready = False

        # if depts and set(depts).difference(proct('ul.thumbnails li.fashion-photo img')
        #     product.dept = list(set(depts) | set(product.dept or []))
        #     is_updated = True

        if image_urls and image_urls != product.image_urls:
            product.image_urls = image_urls
            is_updated = True

        if brand and brand != product.brand:
            product.brand = brand
            is_updated = True

        if title and not product.title:
            product.title = title
            is_updated = True

        if listprice and listprice != product.listprice:
            product.listprice = listprice
            is_updated = True

        if price and price != product.price:
            product.price = price
            is_updated = True

        if shipping and shipping != product.shipping:
            product.shipping = shipping
            is_updated = True

        if returns and returns != product.returned:
            product.returned = returns
            is_updated = True

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

        # print product.dept
        # print product.image_urls
        # print product.brand
        # print product.title
        # print product.listprice
        # print product.price
        # print is_new
        # print is_updated
        # print ready
        # print product.updated
        # print


if __name__ == '__main__':
    # import zerorpc
    # from settings import CRAWLER_PORT
    # server = zerorpc.Server(Server())
    # server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
    # server.run()

    s = Server()
    # s.crawl_category()

    counter = 0
    categories = Category.objects()
    for category in categories:
        counter += 1
        print '~~~~~~~~~~', counter
        print category.combine_url; print
        s.crawl_listing(category.combine_url, **{'key': category.key})

        #style 1 auxpage
        # if category.combine_url == 'http://shop.nordstrom.com/c/spring-fervor?origin=topnav&cm_sp=Top Navigation-_-Women-_-Spring Trend Guide':
        #     s.crawl_listing(category.combine_url, **{'key': category.key})
        #     continue

    # for product in Product.objects():
    #     s.crawl_product(product.combine_url, **{'key': product.key})