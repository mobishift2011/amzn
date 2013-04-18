#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ethan <ethan@favbuy.com>

"""
crawlers.landsend.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.
"""
from crawlers.common.stash import *
from crawlers.common.events import common_saved, common_failed
from models import Category, Product
from deals.picks import Picker
from powers.pipelines import parse_price
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
    'Host':'www.landsend.com',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22'
}
HOST = 'http://%s' % header['Host']
CANVAS_HOST = 'http://canvas.landsend.com'
req = requests.Session(config=config, headers=header)
THREHOLD_DISCOUNT = 0.5

class Server(object):
    def crawl_canvas_category(self, ctx='', **kwargs):
        url = CANVAS_HOST + '/canvas/'
        res = requests.get(url)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)
        primary_cat_nodes = tree.cssselect('div#tab-navigation div.navigation-container ul.first-level-menu li')

        for primary_cat_node in primary_cat_nodes:
            sub_cat_nodes = primary_cat_node.cssselect('ul.second-level-menu > li > a')
            if not sub_cat_nodes:
                continue

            primary_cat = primary_cat_node.cssselect('a span')
            if primary_cat:
                primary_cat = primary_cat[0].text
            else:
                continue
            
            for sub_cat_node in sub_cat_nodes:
                sub_cat = sub_cat_node.text
                combine_url = sub_cat_node.get('href')
                pattern = r'https?://.+\.landsend\.com/([^?]+)\??'
                match = re.search(pattern, combine_url)
                key = match.groups()[0].replace('/', '_') if match else None

                is_new = False; is_updated = False
                category = Category.objects(key=key).first()

                if not category:
                    is_new = True
                    category = Category(key=key)
                    category.is_leaf = True

                if primary_cat and primary_cat not in category.cats:
                    category.cats.append(primary_cat)
                    is_updated = True

                if combine_url and combine_url != category.combine_url:
                    category.combine_url = combine_url
                    is_updated = True

                category.hit_time = datetime.utcnow()
                category.save()

                common_saved.send(sender=ctx, obj_type='Category', key=category.key, url=category.combine_url, \
                    is_new=is_new, is_updated=((not is_new) and is_updated) )

                print category.key; print category.cats; print category.combine_url; print is_new; print is_updated; print

    def crawl_category(self, ctx='', **kwargs):
        self.crawl_canvas_category(ctx=ctx, **kwargs)
        # res = requests.get(HOST)
        # res.raise_for_status()
        # tree = lxml.html.fromstring(res.content)
        # primary_cat_nodes = tree.cssselect('div.tab-navigation ul.departments li.first-level-item')

        # for primary_cat_node in primary_cat_nodes:
        #     primary_cat = primary_cat_node.cssselect('h2 a')
        #     if primary_cat:
        #         primary_cat = primary_cat[0].text
        #     else:
        #         continue

        #     sub_cat_nodes = primary_cat_node.cssselect('ul.second-level-menu li.second-level-item a.second-level-link')
        #     for sub_cat_node in sub_cat_nodes:
        #         sub_cat = sub_cat_node.text
        #         combine_url = sub_cat_node.get('href')
        #         pattern = r'https?://{0}/([^?]+)\??'.format(header['Host'])
        #         match = re.search(pattern, combine_url)
        #         key = match.groups()[0].replace('/', '_') if match else None

        #         is_new = False; is_updated = False
        #         category = Category.objects(key=key).first()

        #         if not category:
        #             is_new = True
        #             category = Category(key=key)
        #             category.is_leaf = True

        #         if primary_cat and primary_cat not in category.cats:
        #             category.cats.append(primary_cat)
        #             is_updated = True

        #         if combine_url and combine_url != category.combine_url:
        #             category.combine_url = combine_url
        #             is_updated = True

        #         category.hit_time = datetime.utcnow()
        #         category.save()

        #         common_saved.send(sender=ctx, obj_type='Category', key=category.key, url=category.combine_url, \
        #             is_new=is_new, is_updated=((not is_new) and is_updated) )

        #         print category.key; print category.cats; print category.combine_url; print is_new; print is_updated; print

    def crawl_listing(self, url, ctx='', **kwargs):
        category = Category.objects(key=kwargs.get('key')).first()
        if not category:
            print 'Category does not exist'
            common_failed.send(sender=ctx, url=url, reason='Category does not exist -> {0} .'.format(kwargs))
            return

        res = requests.get(url)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)
        container_node = tree.cssselect('div#products')[0]
        product_nodes = container_node.cssselect('ul li.product')

        for product_node in product_nodes:
            price_node = product_node.cssselect('div.product-price')
            listprice_node = price_node[0].cssselect('.was-price')
            listprice = listprice_node[0].text.strip() if listprice_node and listprice_node[0].text else None
            price_node = price_node[0].cssselect('.reduced-price')            
            price = price_node[0].text.strip() if price_node and price_node[0].text else None
            if price is None or listprice is None:
                continue

            favbuy_price = parse_price(price)
            favbuy_listprice = parse_price(listprice)
            if not favbuy_price or not favbuy_listprice:
                continue
            discount = 1.0 * favbuy_price / favbuy_listprice
            if discount >= THREHOLD_DISCOUNT:
                continue

            key = product_node.get('data-product-number')
            title_node = product_node.cssselect('.product-name a')
            if title_node:
                title = title_node[0].text.strip() if title_node[0].text else title_node[0].text
                href = title_node[0].get('href')
                match = re.search(r'https?://.+', href)
                combine_url = href if match else '{0}{1}'.format(CANVAS_HOST, href)

            is_new = False; is_updated = False
            product = Product.objects(key=key).first()
            if not product:
                is_new = True
                product = Product(key=key, brand="Lands' End Canvas")
                product.updated = False
                product.event_type = False

            if title and title != product.title:
                product.title = title
                is_updated = True
                product.update_history['title'] = datetime.utcnow()

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
            # selected = Picker(site='landsend').pick(product)
            # if not selected:
            #     continue
            product.favbuy_price = str(favbuy_price)
            product.favbuy_listprice = str(favbuy_listprice)

            product.hit_time = datetime.utcnow()
            product.save()

            common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, \
                is_new=is_new, is_updated=((not is_new) and is_updated) )

            print product.brand; print product.title; print product.combine_url; print product.listprice, ' / ', product.price; print is_new; print is_updated; print

        # Go to the next page to keep on crawling.
        next_page = None
        page_node = tree.cssselect('div.paginationButtonNext a')

        if page_node:
            href = page_node[0].get('href')
            match = re.search(r'https?://.+', href)
            next_page = href if match else '{0}{1}'.format(CANVAS_HOST, href)

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
        image_nodes = tree.cssselect('ul.pp-image-viewer-gallery li a img')
        for image_node in image_nodes:
            src = image_node.get('src')
            if not src:
                continue
            if not src.startswith(('http:', 'https:')):
                src = 'http:' + src
            image_url = src.split('?')[0] + '?scl=3'
            if image_url not in image_urls:
                image_urls.append(image_url)

        list_info = []
        info_node = tree.cssselect('div.pp-product-description')[0]
        callout_info_node = info_node.cssselect('.pp-description-callout')
        if callout_info_node:
            callout_info = ''.join(callout_info_node[0].xpath('.//text()')).strip()
            if  callout_info:
                list_info.append(callout_info)

        li_info_nodes = info_node.cssselect('ul.noindent li.standardBulletText')
        for li_info_node in li_info_nodes:
            li_info = li_info_node.text
            if li_info:
                list_info.append(li_info.strip())

        p_nodes = info_node.cssselect('ul.noindent + p')
        for p_node in p_nodes:
            extra_infos = p_node.xpath('.//text()')
            for extra_info in extra_infos :
                list_info.append(extra_info.strip())

        # update product
        is_new = False; is_updated = False; ready = False

        if image_urls and image_urls != product.image_urls:
            product.image_urls = image_urls
            is_updated = True
            product.update_history['image_urls'] = datetime.utcnow()

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

        print product.image_urls; print product.title; print product.list_info; print is_new; print is_updated; print ready; print


if __name__ == '__main__':
    # import zerorpc
    # from settings import CRAWLER_PORT
    # server = zerorpc.Server(Server())
    # server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
    # server.run()

    s = Server()
    s.crawl_category()

    categories = Category.objects()
    for category in categories:
        print category.combine_url
        s.crawl_listing(url=category.combine_url, **{'key': category.key})

    for product in Product.objects():
        print product.combine_url
        print product.key
        s.crawl_product(product.combine_url, **{'key': product.key})