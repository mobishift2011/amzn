#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

"""
crawlers.6pm.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.
"""
from crawlers.common.stash import *
from crawlers.common.events import common_saved, common_failed
from models import Product
import requests
import lxml.html
import re

header = {
    'Host': 'http://www.6pm.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0',
}

req = requests.Session(prefetch=True, timeout=25, config=config, headers=header)

class Server(object):
    def __init__(self):
        pass

    def crawl_category(self, ctx='', **kwargs):
        url = 'http://www.6pm.com/'
        res = requests.get(url)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)

        TODAY_DEALS_node = tree.cssselect('div.imageFarm')[0]
        category_nodes = TODAY_DEALS_node.cssselect('a')

        for category_node in category_nodes:
            href = category_node.get('href')
            img_node = category_node.cssselect('img')[0]
            key = img_node.get('class')

            print href
            print img_node
            print key
            print 



    def crawl_listing(self, url, ctx='', **kwargs):
        res = requests.get(url)
        res.raise_for_status()

        tree = lxml.html.fromstring(res.content)
        product_nodes = tree.cssselect('div#searchResults')[0].cssselect('a')

        for product_node in product_nodes:
            data_style_id = product_node.get('data-style-id')
            data_product_id = product_node.get('data-product-id')
            if not data_style_id or not data_product_id:
                common_failed.send(sender=ctx, url=url, reason='deal product no data_style_id or data_product_id')
                continue

            key = '%s_%s' % (data_style_id, data_product_id)
            brand = product_node.cssselect('span.brandName')[0].text.strip()
            title = ('%s %s' % (brand, product_node.cssselect('span.productName')[0].text)).strip()
            price = product_node.cssselect('span.price-6pm')[0].text.strip()
            combine_url = product_node.get('href')

            if not key:
                common_failed.send(sender=ctx, url=url, reason='deal product no key')
                continue

            match = re.search(r'https?://+', combine_url)
            if not match:
                combine_url = 'http://www.6pm.com%s' % (combine_url)

            is_new = False
            is_updated = False
            product = Product.objects(key=key).first()
            is_new = bool(product)

            if is_new:
                product = Product(key=key)

            if brand != product.brand:
                product.brand = brand
                is_updated = True

            if title != product.title:
                product.title = title
                is_updated = True

            if price != product.price:
                product.price = price
                is_updated = True

            if combine_url != product.combine_url:
                product.combine_url = combine_url
                is_updated = True

            if is_new:
                product.updated = False
                product.save()
            else:
                if is_updated:
                    product.save()

            print product.key
            print product.brand
            print product.title
            print product.price
            print product.combine_url
            print is_new
            print is_updated
            print

            common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, is_new=is_new, is_updated=is_updated)

        # TODO About Paginator
        
    def crawl_product(self, url, ctx='', **kwargs):
        res = requests.get(url)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)

        product = Product() #TODO
        is_new = False
        is_updated = False
        ready = False

        # breadcumbs, also treated as depts of the product
        categories = tree.cssselect('div#breadcrumbs #crumbs a')
        for category in categories:
            if category.strip() not in product.dept:
                product.dept.append(category.strip())
                is_updated = True

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
        list_price = price_node('.oldPrice')[0].text.strip()
        price = price_node('.price')[0].text.strip()

        # shipping info of the product
        shipping = sale_info_node('li#shipping a span')[0].text

        # update product
        if list_info != product.list_info:
            product.list_info = list_info
            is_updated = True

        if price != product.price:
            product.price = price
            is_updated = True

        if list_price != product.list_price:
            product.list_price = list_price
            is_updated = True

        if shipping != product.shipping:
            product.shipping = shipping
            is_updated = True

        if is_updated:
            if not product.updated:
                product.updated = True
                ready = True
            product.save()

        common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, \
            is_new=is_new, is_updated=is_updated, ready=ready)


if __name__ == '__main__':
    # import zerorpc
    # from settings import CRAWLER_PORT
    # server = zerorpc.Server(Server())
    # server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
    # server.run()

    s = Server()
    s.crawl_category()
    #s.crawl_listing(url='http://www.6pm.com/naturalizer-women-shoes/CK_XAVIBacABAeICAwoBGA.zso?zbfid=14779&s=isNew/desc/goLiveDate/desc/recentSalesStyle/desc/')
    # s.crawl_product('http://www.6pm.com/jessica-simpson-sleeveless-dress-white?zfcTest=mat%3A1')