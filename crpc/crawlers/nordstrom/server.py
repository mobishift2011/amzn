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

header = {
    'Host': 'http://shop.nordstrom.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0',
}

req = requests.Session(prefetch=True, timeout=25, config=config, headers=header)

SALE_PAGE = 'http://shop.nordstrom.com/c/sale?origin=topnav&cm_sp=Top%20Navigation-_-Sale-_-Sale'

class Server(object):
    def __init__(self):
        pass

    def crawl_category(self, ctx='', **kwargs):
        res = requests.get(SALE_PAGE)
        res.raise_for_status()

        tree = lxml.html.fromstring(res.content)
        a_nodes = tree.cssselect('div#TilesZone div.dlp-tiles-row ul li a.shop-link')
        
        for a_node in a_nodes:
            href = a_node.get('href')
            key = a_node.get('name')

            if not key:
                common_failed.send(sender=ctx, url=href, reason='Sale has no key')
                continue

            if not href:
                common_failed.send(sender=ctx, url=href, reason='Sale %s has no href' % key)

            is_new = False; is_updated = False
            category = Category.objects(key=key).first()

            if not category:
                is_new = True
                category = Category(key=key)

            if href != category.combine_url:
                category.combine_url = href
                is_updated = True

            category.hit_time = datetime.utcnow()
            category.save()

            print category.key
            print category.combine_url
            print category.hit_time
            print is_new
            print is_updated
            print

            common_saved.send(sender=ctx, obj_type='Category', key=category.key, url=category.combine_url, \
                is_new=is_new, is_updated=((not is_new) and is_updated) )

    def crawl_listing(self, url, ctx='', **kwargs):
        res = requests.get(url)
        res.raise_for_status()

        tree = lxml.html.fromstring(res.content)

        arrow_nodes = tree.cssselect('div.fashion-results-pager ul.arrows li')
        for arrow_node in arrow_nodes:
            if 'next' in arrow_node.get('class'):
                next_page = arrow_node.cssselect('a')[0].get('href') \
                    if 'disabled' not in arrow_node.get('class') else None
                break

        product_nodes = tree.cssselect('div.row > div')
        for product_node in product_nodes:
            key = product_node.get('data-style-id')
            if not key:
                common_failed.send(sender=ctx, url=url, reason='listing product has no key')
                continue

            try:
                info_node = product_node.cssselect('div.info')[0]

                a_node = info_node.cssselect('a')[0]
                title = a_node.text.strip()

                combine_url = a_node.get('href')
                if not combine_url:
                    common_failed.send(sender=ctx, url=url, reason='listing product %s.%s cannot crawl combine_url' % (key, title))
                    continue

                match = re.search(r'https?://.+', combine_url)
                if not match:
                    combine_url = 'http://shop.nordstrom.com%s' % (combine_url)

                price = None; listprice = None
                price_nodes = info_node.cssselect(".price")
                for price_node in price_nodes:
                    if 'regular' in price_node.get('class'):
                        listprice = price_node.text
                    elif 'sale' in price_node.get('class'):
                        price = price_node.text

                if price is None or listprice is None:
                    common_failed.send(sender=ctx, url=url, \
                        reason='listing product %s.%s cannot crawl price info -> %s / %s' % (key, title, price, listprice))
                    continue

            except IndexError:
                print traceback.format_exc()
                common_failed.send(sender=ctx, url=url, reason='listing product %s -> %s' % (key, traceback.format_exc()))
                continue


            is_new = False; is_updated = False

            product = Product.objects(key=key).first()
            if not product:
                is_new = True
                product = Product(key=key)

            if combine_url != product.combine_url:
                product.combine_url = combine_url
                is_updated = True

            if title != product.title:
                product.title = title
                is_updated = True

            if price != product.price:
                product.price = price
                is_updated = True

            if listprice != product.listprice:
                product.listprice = listprice
                is_updated = True

            if is_updated:
                product.list_update_time = datetime.utcnow()

            product.hit_time = datetime.utcnow()
            product.save()

            print product.title
            print product.combine_url
            print product.listprice
            print product.price
            print is_new
            print is_updated
            print

            common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, \
                is_new=is_new, is_updated=((not is_new) and is_updated) )

        # Go to the next page to keep on crawling.
        if next_page:
            print next_page, ctx, '\n'
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

        breadcrumbs_nodes = tree.cssselect('ul.breadcrumbs li a')
        depts = [breadcrumbs_node.text.strip() for breadcrumbs_node in breadcrumbs_nodes[1:]] \
            if len(breadcrumbs_nodes) > 1 else []

        product_node = tree.cssselect('div.product-content')[0]
        
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
            shipping = ship_and_ret_node[0].text.strip()
            returns = shipping

        list_info = []
        descs = product_node.cssselect('div#productdetails #pdList')[0].xpath('.//text()')
        for desc in descs:
            d = re.sub(r'\r|\n|\t', '', desc)
            if d:
                list_info.append(d.strip())

        # update product
        is_new = False; is_updated = False; ready = False

        if depts and set(depts).difference(product.dept or []):
            product.dept = list(set(depts) | set(product.dept or []))
            is_updated = True

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
                # To pick the product which fit our needs, such as a certain discount, brand, dept etc.
                selected = Picker(site='nordstrom').pick(product)
                if not selected:
                    product.delete()
                    return

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
        print product.listprice
        print product.price
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
    #     s.crawl_listing(category.combine_url, 'ctx.test.%s'%category.key)
    for product in Product.objects():
        s.crawl_product(product.combine_url, **{'key': product.key})