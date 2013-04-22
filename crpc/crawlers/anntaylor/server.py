#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import re
import requests
import lxml.html
from datetime import datetime

from models import *
from crawlers.common.events import common_saved
from deals.picks import Picker

class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.anntaylor.com'

    def crawl_category(self, ctx='', **kwargs):
        ret = requests.get(self.siteurl)
        tree = lxml.html.fromstring(ret.content)
        for node in tree.cssselect('div#main-hd div#nav-site ul.list-l1 > li'):
            dept_name = node.cssselect('div.changeCategorys')
            if not dept_name: continue
            dept_name = dept_name[0].text_content().replace('AT', '').strip()
            if dept_name == 'Lookbook': continue
            for node_l2 in node.cssselect('div.wrapper-l2 ul.list-l2 li'):
                link = node_l2.cssselect('a')[0].get('href')
                link = link if link.startswith('http') else self.siteurl + link
                name = node_l2.cssselect('a')[0].text_content().replace('AT', '').strip()
                if name == 'ANN Wedding Swatches Summer': continue
                cats = [dept_name, name]

                is_new = is_updated = False
                category = Category.objects(key=link.rsplit('/', 1)[-1]).first()
                if not category:
                    is_new = True
                    category = Category(key = link.rsplit('/', 1)[-1])
                    category.is_leaf = True

                if category.combine_url != link:
                    category.combine_url = link
                    is_updated = True
                if set(cats).difference(category.cats):
                    category.cats = cats
                    is_updated = True

                category.update_time = datetime.utcnow()
                category.save()
                common_saved.send(sender=ctx, obj_type='Category', key=category.key, url=category.combine_url,
                        is_new=is_new, is_updated=((not is_new) and is_updated) )


    def crawl_listing(self, url, ctx='', **kwargs):
        self.crawl_listing_page(url, 1, ctx)


    def crawl_listing_page(self, url, page_num, ctx):
        category_key = url.rsplit('/', 1)[-1]
        ret = requests.get(url)
        tree = lxml.html.fromstring(ret.content)
        for node in tree.cssselect('div#main-bd-inner div.products div.grid div.gu div.product'):
            link = node.cssselect('div.overlay a.clickthrough')[0].get('href')
            link = link if link.startswith('http') else self.siteurl + link

            desc = node.cssselect('div.overlay div.fg div.description')[0]
            price = desc.cssselect('div.price p.sale')[0].text_content().replace('$', '').replace(',', '').strip()
            listprice = desc.cssselect('div.price p.was')
            listprice = listprice[0].text_content().replace('was', '').replace('Was', '').replace('$', '').replace(',', '').strip() if listprice else price

            title = desc.cssselect('div.messaging')[0].text_content().strip()
            off_sale = desc.cssselect('div.messaging p.POS')
            off_sale = off_sale[0].text_content().strip() if off_sale else ''
            title = title.replace(off_sale, '').strip()

            if not off_sale and price == listprice:
                continue
            discount = re.compile('[^\d]*(\d+)%').match(off_sale)
            discount = float( discount.group(1) ) if discount else 0
            price = (100 -  discount) / 100.0 * float(price)

            link = re.compile('([^\?]+)').match(link).group(1)
            key = link.rsplit('/', 1)[-1]
            is_new = is_updated = False
            product = Product.objects(key=key).first()
            if not product:
                is_new = True
                product = Product(key=key)
                product.event_type = False
                product.updated = False

            if title != product.title:
                product.title = title
                is_updated = True
                product.update_history.update({ 'title': datetime.utcnow() })
            if str(price) != product.price:
                product.price = str(price)
                is_updated = True
                product.update_history.update({ 'price': datetime.utcnow() })
            if listprice != product.listprice:
                product.listprice = listprice
                is_updated = True
                product.update_history.update({ 'listprice': datetime.utcnow() })
            if link != product.combine_url:
                product.combine_url = link
                is_updated = True
                product.update_history.update({ 'combine_url': datetime.utcnow() })

            selected = Picker(site=DB).pick(product)
            if not selected:
                continue

            if category_key not in product.category_key:
                product.category_key.append(category_key)
                is_updated = True
            if is_updated:
                product.list_update_time = datetime.utcnow()
            product.save()
            common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url,
                    is_new=is_new, is_updated=((not is_new) and is_updated) )

        next_url = tree.cssselect('div#ProductToolbarTemplate ul.tools li.paginateGrid ol.pages a.next')
        if next_url:
            if page_num > 20:
                return
            next_url = next_url[0].get('href')
            next_url = next_url if next_url.startswith('http') else self.siteurl + next_url
            self.crawl_listing_page(next_url, page_num+1, ctx)
       


    def crawl_product(self, url, ctx='', **kwargs):
        ret = requests.get(url)
        if not ret.ok:
            common_failed.send(sender=ctx, key='', url=url, reason='download error return: {0}'.format(ret.status_code))
            return
        tree = lxml.html.fromstring(ret.content)
        node = tree.cssselect('div#main-bd-inner div.grid div.info-product div.g-productInfo')[0]
        summary = node.cssselect('div.description')[0].text_content().strip()
        list_info = node.xpath('.//div[@class="details"]//text()')
        list_info = [i for i in list_info if i.strip()]

        key = url.rsplit('/', 1)[-1]
        image = tree.cssselect('img#productImage')[0].get('src')
        profileid = re.compile('.*profileId=(\d+)&').match(image).group(1)
        image_urls = []
        image = 'http://richmedia.channeladvisor.com/ViewerDelivery/productXmlService?profileid={0}&itemid={1}'.format(profileid, key)
        t = lxml.html.fromstring( requests.get(image).content )
        for img in t.xpath('//image[@type="source"]'):
            image_urls.append( img.get('path') )

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
    ss.crawl_listing('http://www.anntaylor.com/ann/cat/AT-Apparel/AT-Sweaters/cata000011')
