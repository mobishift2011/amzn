#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ethan <ethan@favbuy.com>

"""
crawlers.macys.server
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

HOST = 'http://www1.macys.com'
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www1.macys.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22',
    'X-Requested-With': 'XMLHttpRequest',
}
req = requests.Session(prefetch=True, timeout=25, config=config, headers=header)

class Server(object):
    def __init__(self):
        pass

    def crawl_category(self, ctx='', **kwargs):
        site_map = 'http://www1.macys.com/cms/slp/2/Site-Index'
        res = requests.get(site_map)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)
        dept_nodes = tree.cssselect('div#sitemap_wrapper div.sitelink_container')
        for dept_node in dept_nodes:
            dept = dept_node.cssselect('h2')[0].text.strip()
            subdept_nodes = dept_node.cssselect('a')
            for subdept_node in subdept_nodes:
                sub_dept = subdept_node.text.strip()
                combine_url = subdept_node.get('href')
                id_match = re.search(r'id=(\d+)', combine_url)
                url_id = '_'+id_match.groups()[0] if id_match else ''
                cats = [dept, sub_dept]
                key = '_'.join(cats) + url_id

                is_new = False; is_updated = False
                category = Category.objects(key=key).first()

                if not category:
                    is_new = True
                    category = Category(key=key)

                if combine_url and combine_url != category.combine_url:
                    category.combine_url = combine_url
                    is_updated = True

                if set(cats).difference(category.cats):
                    category.cats = list(set(cats) | set(category.cats))
                    is_updated = True

                category.hit_time = datetime.utcnow()
                category.save()

                common_saved.send(sender=ctx, obj_type='Category', key=category.key, url=category.combine_url, \
                    is_new=is_new, is_updated=((not is_new) and is_updated) )

                print category.key
                print category.cats
                print category.combine_url
                print is_new
                print is_updated
                print

    def crawl_listing(self, url, ctx='', **kwargs):
        sale_url = url# + '#!fn=SPECIAL_OFFERS%3DSales%2520%2526%2520Discounts%26sortBy%3DORIGINAL%26productsPerPage%3D40&!qvp=iqvp'
        res = req.get(url)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)
        product_nodes = tree.cssselect('div#macysGlobalLayout div#thumbnails div.productThumbnail')

        for product_node in product_nodes:
            key = product_node.get('id')
            if not key:
                common_failed.send(sender=ctx, url=url, reason='listing product has no key')
                continue

            try:
                href_node = product_node.cssselect('div.shortDescription a')[0]
                title = href_node.xpath('text()')[-1].strip()
            except:
                print traceback.format_exc()
                common_failed.send(sender=ctx, url=url, reason='listing product %s -> %s' % (key, traceback.format_exc()))
                continue

            combine_url = href_node.get('href')
            match = re.search(r'https?://.+', combine_url)
            if not match:
                combine_url = '%s%s' % (HOST, combine_url)

            price = None; listprice = None
            price_nodes = product_node.cssselect('div.prices span')
            for price_node in price_nodes:
                if  price_node.get('class') and 'priceSale' in price_node.get('class'):
                    price = price_node.xpath('text()')[-1].strip()
                else:
                    listprice = price_node.text.strip() if price_node.text else listprice

            # eliminate products of no discount
            if price is None or listprice is None:
                # common_failed.send(sender=ctx, url=url, \
                #     reason='listing product %s.%s cannot crawl price info -> %s / %s' % (key, title, price, listprice))
                continue

            is_new = False; is_updated = False
            product = Product.objects(key=key).first()
            if not product:
                is_new = True
                product = Product(key=key)

            if title and title != product.title:
                product.title = title
                is_updated = True

            if combine_url and combine_url != product.combine_url:
                product.combine_url = combine_url
                is_updated = True

            if price and price != product.price:
                product.price = price
                is_updated = True

            if listprice and listprice != product.listprice:
                product.listprice = listprice
                is_updated = True

            category = Category.objects(key=kwargs.get('key')).first()
            if not category:
                common_failed.send(sender=ctx, url=url, reason='category %s not found in db' % kwargs.get('key'))
                continue

            if category.cats and set(category.cats).difference(product.dept):
                product.dept = list(set(category.cats) | set(product.dept or []))
                is_updated = True

            if category.key not in product.category_key:
                product.category_key.append(category.key)
                is_updated = True

            if is_updated:
                product.list_update_time = datetime.utcnow()
            
            
            product.hit_time = datetime.utcnow()
            product.save()

            common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, \
                is_new=is_new, is_updated=((not is_new) and is_updated) )

            print product.title
            print product.combine_url
            print product.listprice
            print product.price
            print is_new
            print is_updated
            print

        # Go to the next page to keep on crawling.
        tree.cssselect('div#paginateTop')

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
        pass


if __name__ == '__main__':
    # import zerorpc
    # from settings import CRAWLER_PORT
    # server = zerorpc.Server(Server())
    # server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
    # server.run()

    s = Server()
    # s.crawl_category()

    s.crawl_listing('http://www1.macys.com/shop/womens-clothing/womens-swimwear?id=8699')
    # counter = 0
    # categories = Category.objects()
    # for category in categories:
    #     counter += 1
    #     print '~~~~~~~~~~', counter
    #     print category.combine_url; print
    #     s.crawl_listing(category.combine_url, **{'key': category.key})

    # for product in Product.objects():
    #     s.crawl_product(product.combine_url, **{'key': product.key})