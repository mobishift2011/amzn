#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import re
import requests
import lxml.html
from datetime import datetime

from crawlers.common.stash import *
from models import *
from crawlers.common.events import common_saved, common_failed
from deals.picks import Picker

header = {
    'Host': 'www.ebags.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Ubuntu Chromium/25.0.1364.160 Chrome/25.0.1364.160 Safari/537.22',
}

req = requests.Session(prefetch=True, timeout=30, config=config, headers=header)

class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.ebags.com'
        self.get_product_id = re.compile('.*productid=(\d+)')

    def fetch_page(self, url):
        ret = req.get(url)
        if ret.url.startswith('http://www.ebags.com/error/unknown'):
            return -404
        if ret.ok: return ret.content
        else: return ret.status

    def crawl_category(self, ctx='', **kwargs):
        ret = self.fetch_page(self.siteurl)
        if isinstance(ret, int):
            common_failed.send(sender=ctx, key='', url=self.siteurl,
                    reason='download home page failed: {0}'.format(ret))
            return
        tree = lxml.html.fromstring(ret)
        nodes = tree.cssselect('div#main div#navWrap ul#navCon > li')
        k_link = {}
        for node in nodes:
            try:
                link = node.cssselect('a.sliderNav')[0].get('href')
            except IndexError:
                # the last one is: Shop All Departments
                continue
            link = link if link.startswith('http') else self.siteurl + link
            key = re.compile('.+/department/(.+)\?origin=flyaway').match(link).group(1)
            k_link[key] = link

        for key, link in k_link.iteritems():
            ret = self.fetch_page(link)
            if isinstance(ret, int):
                common_failed.send(sender=ctx, key=key, url=link,
                        reason='download category page error: {0}'.format(ret))
                continue
            tree = lxml.html.fromstring(ret)
            list_node = tree.cssselect('#lnkSeeAllDepartment')[0]
            num = list_node.cssselect('span')[0].text_content().strip()
            num = int( re.compile('\((\d+)\)').match(num).group(1) )
            link = list_node.get('href')
            if 'category' not in link: continue
            link = link if link.startswith('http') else self.siteurl + link

            is_new = is_updated = False
            category = Category.objects(key=key).first()
            if not category:
                is_new = True
                category = Category(key=key)
                category.is_leaf = True
                category.cats = [key]
                category.pagesize = 144
            category.combine_url = link
            category.num = num
            category.update_time = datetime.utcnow()
            category.save()
            common_saved.send(sender=ctx, obj_type='Category', key=key, url=link, is_new=is_new, is_updated=is_updated)


    def crawl_listing(self, url, ctx='', **kwargs):
        category = Category.objects(key=kwargs.get('key')).first()
        ret = self.fetch_page(url)
        if isinstance(ret, int):
            common_failed.send(sender='ctx', key='', url=url,
                    reason="download listing page error: {0}".format(ret))
            return
        tree = lxml.html.fromstring(ret)
        nodes = tree.cssselect('div.mainCon div.ProductListWrap div.thisResultItem')

        for node in nodes:
            try:
                brand = node.cssselect('div.listInfoBox div.listBrand span.itemName')[0].text_content().strip()
            except:
                ret = self.fetch_page(url)
                tree = lxml.html.fromstring(ret)
                nodes = tree.cssselect('div.mainCon div.ProductListWrap div.thisResultItem')

        for node in nodes:
            try:
                brand = node.cssselect('div.listInfoBox div.listBrand span.itemName')[0].text_content().strip()
            except:
                continue
            title = node.cssselect('div.listInfoBox div.listModel span.itemModel')[0].text_content().strip()
            link = node.cssselect('div.listInfoBox div.listModel a')[0].get('href')
            link = link if link.startswith('http') else self.siteurl + link
            if link == 'http://www.ebags.com':
                continue
            key = self.get_product_id.match(link).group(1)
            price = node.cssselect('div.listInfoBox div.listPriceBox span.listPrice')[0].text_content().replace('$', '').strip()
            discount = ''
            for i in node.xpath('./div[@class="listInfoBox"]/div[@class="listPriceBox"]/text()'):
                if i.strip() and '%' in i:
                    discount = i.strip()
            if not discount: continue
            discount = 100 - int( re.compile('[^\d]*(\d+)%.*').match(discount).group(1) )
            discount = discount / 100.0
            shipping = 'free shipping' if node.cssselect('div.listInfoBox div.freeShippingDisplay') else ''

            is_new = is_updated = False
            product = Product.objects(key=key).first()
            if not product:
                is_new = True
                product = Product(key=key)
                product.event_type = False
                product.updated = False
                product.brand = brand
                if shipping:
                    product.shipping = shipping

            if title and title != product.title:
                product.title = title
                product.update_history.update({ 'title': datetime.utcnow() })
                is_updated = True
            if price and price != product.price:
                product.price = price
                product.update_history.update({ 'price': datetime.utcnow() })
                is_updated = True
            if link and link != product.combine_url:
                product.combine_url = link
                product.update_history.update({ 'combine_url': datetime.utcnow() })
                is_updated = True
            if discount and discount != product.discount:
                product.discount = discount
                is_updated = True

            selected = Picker(site=DB).pick(product, discount)
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
        ret = self.fetch_page(url)
        if isinstance(ret, int):
            common_failed.send(sender='ctx', key='', url=url,
                    reason="download detail page error: {0}".format(ret))
            return
        key = self.get_product_id.match(url).group(1)
        t = lxml.html.fromstring(ret)
        listprice = t.cssselect('div#divStrikeThroughPrice')[0].text_content().replace('$', '').strip()
        list_info, summary = [], []
        for l in t.cssselect('#model-overview-tab div.tab-leftcontent-container div.product-spec-line'):
            a = l.cssselect('div.left')[0].text_content().strip()
            b = l.cssselect('div.right')[0].text_content().strip()
            list_info.append(a + ' ' + b)
        for li in t.cssselect('#model-features-tab div.tab-leftcontent-container ul li'):
            summary.append( li.text_content().strip() )
        summary = '\n'.join(summary)

        image = t.cssselect('div#divHeroImage img')[0].get('src')
        image = image if image.startswith('http') else 'http:' + image
        link, hei, wid = re.compile('(.+\?).*&hei=(\d+)&wid=(\d+).*').match(image).groups()
        hei, wid = int(hei)*3, int(wid)*3
        img = '{0}&hei={1}&wid={2}'.format(link, hei, wid)
        image_urls = [img]

        is_new = is_updated = False
        product = Product.objects(key=key).first()
        if not product:
            is_new = True
            product = Product(key=key)
        if listprice and product.listprice != listprice:
            product.listprice = listprice
            is_updated = True

        product.list_info = list_info
        product.summary = summary
        product.image_urls = image_urls
        product.full_update_time = datetime.utcnow()
        if product.updated == False:
            product.updated = True
            ready = True
        else: ready = False
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=key, url=url, is_new=is_new, is_updated=is_updated, ready=ready)


if __name__ == '__main__':
    ss = Server()
    ss.crawl_category()
    exit()
    ss.crawl_listing('http://www.ebags.com/category/wallets-and-accessories?items=144?page=14')

