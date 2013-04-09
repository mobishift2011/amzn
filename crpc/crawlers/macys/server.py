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
from models import *
from deals.picks import Picker

import json
import lxml.html
import traceback
import re
from datetime import datetime

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Host': 'www1.macys.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22',
    'X-Requested-With': 'XMLHttpRequest',
}
req = requests.Session(prefetch=True, timeout=30, config=config, headers=header)

class Server(object):
    def __init__(self):
        self.siteurl = 'http://www1.macys.com'

    def fetch_page(self, url):
        ret = req.get(url)
        if ret.ok: return ret.content
        else: return ret.status_code

    def crawl_category(self, ctx='', **kwargs):
        site_map = 'http://www1.macys.com/cms/slp/2/Site-Index'
        ret = self.fetch_page(site_map)
        if isinstance(ret, int):
            common_failed.send(sender=ctx, key='', url=site_map, reason='download sitemap return: {0}'.format(ret))
            return
        tree = lxml.html.fromstring(ret)
        dept_nodes = tree.cssselect('div#sitemap_wrapper div.sitelink_container')
        for dept_node in dept_nodes:
            dept = dept_node.cssselect('h2')[0].text.strip()
            if dept == 'Promotions': continue
            subdept_nodes = dept_node.cssselect('a')
            for subdept_node in subdept_nodes:
                sub_dept = subdept_node.text.strip()
                if sub_dept == 'Shop All ' + dept:
                    self.crawl_clearance(dept, subdept_node.get('href').strip(), ctx)
                    continue
                combine_url = subdept_node.get('href')
                id_match = re.search(r'id=(\d+)', combine_url)
                url_id = '_'+id_match.groups()[0] if id_match else ''
                cats = [dept, sub_dept]
                key = '_'.join(cats) + url_id

                self.save_category(key, combine_url, cats, ctx)


    def crawl_clearance(self, dept, url, ctx):
        ret = self.fetch_page(url)
        if isinstance(ret, int):
            common_failed.send(sender=ctx, key='', url=url,
                reason='download category clearance url error return: {0}'.format(ret))
            return
        tree = lxml.html.fromstring(ret)
        clearance = tree.cssselect('div#localNavigationContainer ul.nav_cat_sub_2 li.nav_cat_item_hilite')
        if clearance:
            combine_url = clearance[-1].cssselect('a')[0].get('href')
            id_match = re.search(r'id=(\d+)', combine_url)
            url_id = '_'+id_match.groups()[0] if id_match else ''
            cats = [dept, 'clearance']
            key = '_'.join(cats) + url_id

            self.save_category(key, combine_url, cats, ctx)


        brands_nodes = tree.cssselect('div#localNavigationContainer ul.nav_cat_sub_2 li.nav_cat_item_bold')
        for brand in brands_nodes:
            if brand.cssselect('span') and 'brands' in brand.cssselect('span')[0].text_content().lower():
                for b in brand.cssselect('ul.nav_cat_sub_3 li a'):
                    combine_url = b.get('href')
                    if combine_url.startswith('javascript'): continue
                    id_match = re.search(r'id=(\d+)', combine_url)
                    url_id = '_'+id_match.groups()[0] if id_match else ''
                    cats = [dept, b.text_content()]
                    key = '_'.join(cats) + url_id

                    self.save_category(key, combine_url, cats, ctx)

        

    def save_category(self, key, combine_url, cats, ctx):
        is_new = False; is_updated = False
        category = Category.objects(key=key).first()

        if not category:
            is_new = True
            category = Category(key=key)
            category.is_leaf = True

        if combine_url and combine_url != category.combine_url:
            category.combine_url = combine_url
            is_updated = True

        if set(cats).difference(category.cats):
            category.cats = list(set(cats) | set(category.cats))
            is_updated = True

        category.update_time = datetime.utcnow()
        category.save()

        common_saved.send(sender=ctx, obj_type='Category', key=category.key, url=category.combine_url, \
            is_new=is_new, is_updated=((not is_new) and is_updated) )


    def crawl_listing(self, url, ctx='', **kwargs):
        ret = self.fetch_page(url)
        if isinstance(ret, int):
            common_failed.send(sender=ctx, key='', url=url,
                reason='download listing url error return: {0}'.format(ret))
            return
        tree = lxml.html.fromstring(ret)
        product_nodes = tree.cssselect('div#macysGlobalLayout div.thumbnails div.productThumbnail')

        category = Category.objects(key=kwargs.get('key')).first()
        if not category:
            common_failed.send(sender=ctx, url=url, reason='category %s not found in db' % kwargs.get('key'))
            return

        for product_node in product_nodes:
            key = product_node.get('id')
            if not key:
                common_failed.send(sender=ctx, url=url, reason='listing product has no key')
                continue

            try:
                href_node = product_node.cssselect('div.shortDescription a')[0]
                title = href_node.xpath('text()')[-1].strip()
            except:
                common_failed.send(sender=ctx, url=url, reason='listing product %s -> %s' % (key, traceback.format_exc()))
                continue

            combine_url = href_node.get('href')
            match = re.search(r'https?://.+', combine_url)
            if not match:
                combine_url = '%s%s' % (self.siteurl, combine_url)

            discount = product_node.cssselect('div.badgeJSON')
            if discount:
                discount = discount[0].text_content()
            if discount and discount[1:-1]:
                js = json.loads(discount[1:-1])
                off = re.compile('[^\d]*(\d+)%').match( js['BADGE_TEXT']['HEADER'] )
                if off:
                    discount = int( off.group(1) ) / 100.0
                else: discount = 0
            else:
                discount = 0

            price = None; listprice = None
            price_nodes = product_node.cssselect('div.prices span')
            for price_node in price_nodes:
                if  price_node.get('class') and 'priceSale' in price_node.get('class'):
                    price = price_node.xpath('text()')[-1].strip()
                else:
                    if listprice is None:
                        listprice = price_node.text.strip() if price_node.text else listprice

            # eliminate products of no discount
            if price is None or listprice is None:
                # common_failed.send(sender=ctx, url=url, \
                #     reason='listing product %s.%s cannot crawl price info -> %s / %s' % (key, title, price, listprice))
                continue
            price = re.compile('[^\d]*(\d+\.?\d*)').match(price).group(1)
            price = price.replace('Sale', '').replace('Your Choice', '').replace('Now', '').replace('$', '').replace(',', '').strip()
            listprice = re.compile('[^\d]*(\d+\.?\d*)').match(listprice).group(1)
            listprice = listprice.replace('Reg.', '').replace('Orig.', '').replace('$', '').replace(',', '').strip()

            if '-' in price:
                price = price.split('-')[0]
            if '-' in listprice:
                listprice = listprice.split('-')[0]
            discount = ( float(price) - float(price) * discount ) / float(listprice)

            is_new = False; is_updated = False
            product = Product.objects(key=key).first()
            if not product:
                is_new = True
                product = Product(key=key)
                product.updated = False
                product.event_type = False

            if title and title != product.title:
                product.title = title
                product.update_history.update({ 'title': datetime.utcnow() })
                is_updated = True

            if combine_url and combine_url != product.combine_url:
                product.combine_url = combine_url
                product.update_history.update({ 'combine_url': datetime.utcnow() })
                is_updated = True

            if price and price != product.price:
                product.price = price
                is_updated = True

            if listprice and listprice != product.listprice:
                product.listprice = listprice
                is_updated = True

            # To pick the product which fit our needs, such as a certain discount, brand, dept etc.
            if discount:
                selected = Picker(site=DB).pick(product, discount)
                if not selected:
                    continue
            else:
                selected = Picker(site=DB).pick(product)
                if not selected:
                    continue

            if category.cats and set(category.cats).difference(product.dept):
                product.dept = list(set(category.cats) | set(product.dept or []))
                is_updated = True

            if category.key not in product.category_key:
                product.category_key.append(category.key)
                is_updated = True

            if is_updated:
                product.list_update_time = datetime.utcnow()
            
            product.save()

            common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, \
                is_new=is_new, is_updated=((not is_new) and is_updated) )


    def crawl_product(self, url, ctx='', **kwargs):
        ret = self.fetch_page(url)
        if isinstance(ret, int):
            common_failed.send(sender=ctx, key='', url=url,
                reason='download product url error return: {0}'.format(ret))
            return
        tree = lxml.html.fromstring(ret)
        available = tree.cssselect('div#productDescription ul.similarItems li > span')
        if available:
            if 'unavailable' in available[0].text_content():
                product = Product.objects(key=kwargs.get('key')).first()
                if product: product.delete()
                return

        summary = tree.cssselect('div#longDescription')[0].text_content().strip()
        list_info = tree.cssselect('ul#bullets')[0].text_content().strip().split('\n')
        shipping = tree.cssselect('div#pdpshippingNreturn ul.prodInfoList')[0].text_content().strip()
        image = tree.cssselect('div#imageZoomer meta[itemprop]')[0].get('content')
        image_url, width, height = re.compile('(.+tif)\?wid=(\d+)&hei=(\d+).*').match(image).groups()
        width, height = int(width)*13, int(height)*13
        image_urls = ['{0}?wid={1}&hei={2}'.format(image_url, width, height)]
        imgs = tree.cssselect('div#imageZoomer ul#altImages li img')
        for i in imgs:
            img_url = re.compile('(.+tif).*').match( i.get('src') ).group(1)
            img_url = '{0}?wid={1}&hei={2}'.format(img_url, width, height)
            if img_url not in image_urls:
                image_urls.append(img_url)
#        print 'summary: ', [summary]
#        print 'list_info: ', [list_info]
#        print 'shipping: ', [shipping]

        is_new = is_updated = False
        product = Product.objects(key=kwargs.get('key')).first()
        if not product:
            is_new = True
            product = Product(key=kwargs.get('key'))
        product.summary = summary
        product.list_info = list_info
        product.shipping = shipping
        product.image_urls = image_urls
        product.full_update_time = datetime.utcnow()
        if product.updated == False:
            product.updated = True
            ready = True
        else: ready = False
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=url, is_new=is_new, is_updated=is_updated, ready=ready)
        


if __name__ == '__main__':
    # import zerorpc
    # from settings import CRAWLER_PORT
    # server = zerorpc.Server(Server())
    # server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
    # server.run()

    s = Server()
    s.crawl_category()
#
#    s.crawl_listing('http://www1.macys.com/shop/womens-clothing/womens-swimwear?id=8699&viewall=true', key='8699')
#    counter = 0
#    categories = Category.objects()
#    for category in categories:
#         counter += 1
#         print '~~~~~~~~~~', counter
#         print category.combine_url; print
#         s.crawl_listing(category.combine_url + '&viewall=true', **{'key': category.key})
#
#    for product in Product.objects():
#        s.crawl_product(product.combine_url, **{'key': product.key})
