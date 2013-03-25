#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ethan <ethan@favbuy.com>

"""
crawlers.6pm.server
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

HOST = 'http://www.6pm.com'
header = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip,deflate,sdch',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Host':'www.6pm.com',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22'
}
req = requests.Session(config=config, headers=header)

class Server(object):
    def __init__(self):
        pass

    def crawl_category(self, ctx='', **kwargs):
        res = requests.get(HOST)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)
        dept_nodes = tree.cssselect('div#nav div#moreDeptsWrap ul li a')
        for dept_node in dept_nodes:
            dept = dept_node.text.strip()
            href = dept_node.get('href')
            match = re.search(r'https?://.+', href)
            if not match:
                href = '%s%s' % (HOST, href)

            res = requests.get(href)
            res.raise_for_status()
            tree = lxml.html.fromstring(res.content)
            sub_dept_nodes = tree.cssselect('div#tcSideCol h5 a')
            for sub_dept_node in sub_dept_nodes:
                sub_dept = sub_dept_node.text.strip()
                cats = [dept, sub_dept]
                key = '_'.join(cats)
                combine_url = sub_dept_node.get('href')
                match = re.search(r'https?://.+', combine_url)
                if not match:
                    combine_url = '%s%s' % (HOST, combine_url)

                is_new = False; is_updated = False
                category = Category.objects(key=key).first()
                
                if not category:
                    is_new = True
                    category = Category(key=key)
                    category.is_leaf = True

                if set(cats).difference(category.cats):
                    category.cats = list(set(cats) | set(category.cats))
                    is_updated = True

                if combine_url and combine_url != category.combine_url:
                    category.combine_url = combine_url
                    is_updated = True

                category.hit_time = datetime.utcnow()
                category.save()
                
                common_saved.send(sender=ctx, obj_type='Category', key=category.key, url=category.combine_url, \
                    is_new=is_new, is_updated=((not is_new) and is_updated) )

    def crawl_listing(self, url, ctx='', **kwargs):
        res = requests.get(url)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)

        product_nodes = tree.cssselect('div#searchResults a')
        for product_node in product_nodes:
            price = None; listprice = None
            price = product_node.cssselect('.price-6pm')[0].text
            listprice_node = product_node.cssselect('.discount')
            listprice = ''.join(listprice_node[0].xpath('text()')) if listprice_node else None

            # eliminate products of no discountIndexError:
            if price is None or listprice is None:
                # common_failed.send(sender=ctx, url=url, \
                #     reason='listing product %s.%s cannot crawl price info -> %s / %s' % (key, title, price, listprice))
                continue

            key = product_node.get('data-product-id')
            if not key:
                common_failed.send(sender=ctx, url=url, reason='listing product has no key')
                continue

            combine_url = product_node.get('href')
            key = '%s_%s' % (key, combine_url.split('/')[-1])
            match = re.search(r'https?://.+', combine_url)
            if not match:
                combine_url = '%s%s' % (HOST, combine_url)

            brand = product_node.cssselect('.brandName')[0].text.strip()
            title = product_node.cssselect('.productName')[0].text.strip()

            is_new = False; is_updated = False
            product = Product.objects(key=key).first()
            if not product:
                is_new = True
                product = Product(key=key)

            if title and title != product.title:
                product.title = title
                is_updated = True

            if brand and brand != product.brand:
                product.brand = brand
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
            
            # To pick the product which fit our needs, such as a certain discount, brand, dept etc.
            selected = Picker(site='6pm').pick(product)
            if not selected:
                continue

            product.hit_time = datetime.utcnow()
            product.save()

            common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, \
                is_new=is_new, is_updated=((not is_new) and is_updated) )


            print product.key; print product.brand; print product.title; \
            print product.price, ' / ', product.listprice; print product.combine_url; \
            print product.dept; print

        # Go to the next page to keep on crawling.
        next_page = None
        page_node = tree.cssselect('div.pagination')
        if not page_node:
            return

        last_node =page_node[0].cssselect('.last')
        if last_node:
            next_page = page_node[0].cssselect('a')[-1].get('href')

        if next_page:
            match = re.search(r'https?://.+', next_page)
            if not match:
                next_page = '%s%s' % (HOST, next_page)
            print next_page
            self.crawl_listing(url=next_page, ctx=ctx, **kwargs)

    def crawl_product(self, url, ctx='', **kwargs):
        key = kwargs.get('key')
        product = Product.objects(key=key).first()

        if not product:
            print 'product not exists -> %s' % kwargs
            common_failed.send(sender=ctx, url=url, reason='product not exists -> %s' % kwargs)
            return

        res = requests.get(url, params={'zfcTest': 'mat:1'})
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)

        is_new = False; is_updated = False; ready = False

        # breadcumbs, also treated as depts of the product
        # categories = tree.cssselect('div#breadcrumbs #crumbs a')
        # for category in categories:
        #     if category.strip() not in product.dept:
        #         product.dept.append(category.strip())
        #         is_updated = True

        theater_node = tree.cssselect('div#theater')[0]
        stage_node = theater_node.cssselect('div#productStage')[0]

        # original display/large image of the product
        image_nodes = stage_node.cssselect('div#productImages > ul > li img')
        for image_node in image_nodes:
            thumbnail_url = image_node.get('src')
            image_url = re.sub('_THUMBNAILS', '', thumbnail_url)

            if image_url not in product.image_urls:
                product.image_urls.append(image_url)
                is_updated = True

        # description list infos of the product
        li_infos = stage_node.cssselect('div#prdInfo > div#prdInfoText > div.description ul')[0].xpath('.//text()')
        list_info = [li_info.replace('\n', '') for li_info in li_infos if li_info != '\n']

        # original and sale price of the product
        sale_info_node = theater_node.cssselect('div#productForm form#prForm ul')[0]

        price_node = sale_info_node.cssselect('li#priceSlot')[0]
        listprice = price_node.cssselect('.oldPrice')[0].text.strip()
        price = price_node.cssselect('.price')[0].text.strip()

        # shipping info of the product
        shipping = sale_info_node.cssselect('li.shipping a')[0].xpath('.//text()')
        shipping = ''.join(shipping)

        # update product
        if list_info and list_info != product.list_info:
            product.list_info = list_info
            is_updated = True

        if price and price != product.price:
            product.price = price
            is_updated = True

        if listprice and not product.listprice and listprice != product.listprice:
            product.listprice = listprice
            is_updated = True

        if shipping != product.shipping:
            product.shipping = shipping
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
        print product.listprice
        print product.price
        print product.shipping
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

    counter = 0
    categories = Category.objects()
    for category in categories:
        counter += 1
        print '~~~~~~~~~~', counter
        print category.cats
        print category.combine_url; print
        s.crawl_listing(category.combine_url, **{'key': category.key})

    # for product in Product.objects(updated=False):
    #     print product.combine_url
    #     try:
    #         s.crawl_product(product.combine_url, **{'key': product.key})
    #     except requests.exceptions.HTTPError:
    #         continue
    #     except:
    #         print traceback.format_exc()
    #         break