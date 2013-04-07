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

header = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip,deflate,sdch',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Host':'www.ashford.com',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22'
}
HOST = 'http://%s' % header['Host']
req = requests.Session(config=config, headers=header)

class Server(object):
    def crawl_category(self, ctx='', **kwargs):
        res = requests.get(HOST)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)
        dept_nodes = tree.cssselect('div#top-navigation ul.navigation li.menu-item a')
        for dept_node in dept_nodes:
            key = dept_node.text.strip()
            if 'brand' in key.lower():
                continue

            combine_url = dept_node.get('href')
            match = re.search(r'https?://.+', combine_url)
            if not match:
                combine_url = '%s%s' % (HOST, combine_url)

            is_new = False; is_updated = False
            category = Category.objects(key=key).first()

            if not category:
                is_new = True
                category = Category(key=key)
                category.is_leaf = True

            if combine_url and combine_url != category.combine_url:
                category.combine_url = combine_url
                is_updated = True

            category.hit_time = datetime.utcnow()
            category.save()
            
            print category.key; print category.cats; print category.combine_url; print is_new; print is_updated; print;

            common_saved.send(sender=ctx, obj_type='Category', key=category.key, url=category.combine_url, \
                is_new=is_new, is_updated=((not is_new) and is_updated) )

    def crawl_listing(self, url, ctx='', **kwargs):
        res = requests.get(url)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)

        category = kwargs['category'] if kwargs.get('category') else Category.objects(key=kwargs.get('key')).first()
        if not category:
            common_failed.send(sender=ctx, url=url, reason='category %s not found in db' % kwargs.get('key'))
            return
        
        product_nodes = tree.cssselect('div#atg_store_prodList ul li')
        for product_node in product_nodes:
            info_node = product_node.cssselect('div.thumbnailInfo')[0]

            price = None; listprice = None
            price_node = info_node.cssselect('div.our_price')[0]
            weekly_price_node = price_node.cssselect('.newPrice_value')
            sale_price_node = price_node.cssselect('#salePrice')
            if weekly_price_node:
                price = weekly_price_node[0].text.strip()
            elif sale_price_node:
                price = sale_price_node[0].text.strip()
            else:
                price = ''.join(price_node.xpath('.//text()')).strip()
            listprice = info_node.cssselect('div.retail_price')[0].text.strip()
            listprice = re.sub('\n', '', listprice)

            # eliminate products of no discountIndexError:
            if price is None or listprice is None:
                # common_failed.send(sender=ctx, url=url, \
                #     reason='listing product %s.%s cannot crawl price info -> %s / %s' % (key, title, price, listprice))
                continue

            key = info_node.cssselect('div.product_id')[0].text.strip()
            brand = info_node.cssselect('a.sameBrandProduct')[0].text.strip()
            title_node = info_node.cssselect('a.product_gender_name')[0]
            # title = title_node.get('title')
            combine_url = title_node.get('href')
            match = re.search(r'https?://.+', combine_url)
            if not match:
                combine_url = '%s%s' % (HOST, combine_url)

            #
            is_new = False; is_updated = False
            product = Product.objects(key=key).first()
            if not product:
                is_new = True
                product = Product(key=key)
                product.updated = False
                product.event_type = False

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

            # if category.cats and set(category.cats).difference(product.dept):
            #     product.dept = list(set(category.cats) | set(product.dept or []))
            #     is_updated = True

            if category.key not in product.category_key:
                product.category_key.append(category.key)
                is_updated = True

            # To pick the product which fit our needs, such as a certain discount, brand, dept etc.
            selected = Picker(site='ashford').pick(product) if product.updated \
                else self.crawl_detail(ctx, is_new, is_updated, product)
            if not selected:
                continue

            if is_updated:
                product.list_update_time = datetime.utcnow()

            product.hit_time = datetime.utcnow()
            product.save()

        # Go to the next page to keep on crawling.
        next_link_node = tree.cssselect('div.atg_store_filter ul.atg_store_pager li.nextLink')
        if next_link_node:
            next_page = next_link_node[0].cssselect('a')[0].get('href')
            match = re.search(r'https?://.+', next_page)
            if not match:
                next_page = '%s%s' % (HOST, next_page)

            print next_page
            kwargs['category'] = category
            self.crawl_listing(url=next_page, ctx=ctx, **kwargs)

    def crawl_detail(self, ctx, is_new, is_updated, product):
        res = requests.get(product.combine_url)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)

        title = tree.cssselect('div#product_details div#product_info h1')[0].xpath('.//text()')[-1].strip()
        if title and not product.title:
            product.title = title
            is_updated = True

        # To pick the product which fit our needs, such as a certain discount, brand, dept etc.
        selected = Picker(site='ashford').pick(product)
        if not selected:
            return False

        image_nodes = tree.cssselect('div#prod_images ul.alt_imgs li')
        for image_node in image_nodes:
            if 'play_video_image' == image_node.get('id'):
                continue

            image_url = image_node.cssselect('a')[0].get('href')
            match = re.search(r'https?://.+', image_url)
            if not match:
                image_url = '%s%s' % (HOST, image_url)

            if image_url not in product.image_urls:
                product.image_urls.append(image_url)
                is_updated = True

        shipping_node = tree.cssselect('div#dynamic_messaging em.msg2 a')
        if shipping_node:
            shipping = ' '.join(shipping_node[0].xpath('.//text()'))

        info_node = tree.cssselect('div#info_tabs')[0]
        list_info = []
        listinfos = info_node.cssselect('div#prod_1 table')
        for listinfo in listinfos:
            caption = listinfo.cssselect('.caption')
            if caption:
                caption_info = caption[0].text
                if caption_info:
                    list_info.append(caption_info.strip())

            trs = listinfo.cssselect('tbody tr')
            for tr in trs:
                detail = ''
                th = tr.cssselect('th')
                td = tr.cssselect('td') 
                if th and th[0].text:
                    detail = th[0].text.strip() + ' '
                if td and td[0].text:
                    detail += td[0].text.strip()
                if detail:
                    list_info.append(detail)

            if caption or trs:
                list_info.append('\n')

        # # returned = '\n'.join(info_node.cssselect('div#prod_5')[0].xpath('.//text()'))
        # update product
        ready = False

        if title and not product.title:
            product.title = title
            is_updated = True

        if shipping and shipping != product.shipping:
            product.shipping = shipping
            is_updated = True

        # if returned and returned != product.returned:
        #     product.returned = returned
        #     is_updated = True

        if list_info and list_info != product.list_info:
            product.list_info = list_info
            is_updated = True

        if is_updated:
            if not product.updated:
                ready = True
            
            product.updated = True
            product.full_update_time = datetime.utcnow()

        common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, \
            is_new=is_new, is_updated=((not is_new) and is_updated), ready=ready)

        return True

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

    categories = Category.objects()
    for category in categories:
        print category.combine_url
        s.crawl_listing(url=category.combine_url, **{'key': category.key})