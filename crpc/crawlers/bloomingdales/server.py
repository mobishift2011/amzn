#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import re
import requests
import lxml.html
from datetime import datetime

from models import *
from crawlers.common.stash import *
from crawlers.common.events import common_saved

req = requests.Session(prefetch=True, timeout=30, config=config, headers=headers)

class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.bloomingdales.com'
        self.extract_product_key = re.compile('.*ID=(\d+)')

    def fetch_page(self, url):
        ret = req.get(url)
        if ret.ok:
            return ret.content
        else:
            return ret.status_code

    def crawl_category(self, ctx='', **kwargs):
        ret = self.fetch_page(self.siteurl)
        tree = lxml.html.fromstring(ret)
        for d in tree.cssselect('div#bl_nav_top_menu div[class^="bl_nav_top_section_navigation_options"]'):
            link = d.cssselect('a.white')[0].get('href')
            dept = d.cssselect('a img')[0].get('alt')
            if dept == 'Designers':
                self.crawl_designers_category(dept, link, ctx)
                continue
            self.crawl_to_leaf_cateogory(dept, link, ctx)

    def crawl_designers_category(self, dept, url, ctx):
        ret = self.fetch_page(url)
        base_url = re.compile('blm_insecureServer.put\("(.+)"\);').search(ret).group(1)
        pattern_url = re.compile('blm_nav_linkURL.put\("(.+)"\);').search(ret).group(1)
        for sub_dept in re.findall('blm_nav_items.put\({topCategory : "(.+?)",', ret):
            link = '{0}{1}'.format(base_url, pattern_url.replace('designerCat2', sub_dept).replace('designerCat', sub_dept))
            self.crawl_designer_category(dept, sub_dept, link, ctx)

    def crawl_designer_category(self, dept, sub_dept, url, ctx):
        ret = self.fetch_page(url)
        tree = lxml.html.fromstring(ret)
        for designer in tree.cssselect('div#se_localContentContainer div.se_designerColumn li.se_designerColumn a'):
            link = designer.get('href')
            link = link if link.startswith('http') else self.siteurl + link
            brand = designer.text_content().strip()

            self.save_category_db([dept, sub_dept, brand], brand, link + '&resultsPerPage=96', ctx)


    def crawl_to_leaf_cateogory(self, dept, url, ctx):
        ret = self.fetch_page(url)
        tree = lxml.html.fromstring(ret)
        for nav in tree.cssselect('div#gn_left_nav_container div.gn_left_nav_section'):
            sub_dept = nav.cssselect('div.gn_left_nav_top')[0].text_content().strip()
            if sub_dept == 'FASHION INDEX':
                continue
            elif sub_dept == 'All Designers':
                continue
            elif sub_dept == 'Sale':
                link = nav.cssselect('div.gn_left_nav_top a.gn_left_nav_sale')[0].get('href')
                self.save_category_db([dept, sub_dept], dept + '_' + sub_dept, link, ctx)
            else:
                for i in nav.cssselect('ul li.gn_left_nav2_standard a.gn_left_nav'):
                    link = i.get('href')
                    key = link.rsplit('=', 1)[-1]
                    sub_sub_dept = i.text_content().strip()
                    self.save_category_db([dept, sub_dept, sub_sub_dept], key, link, ctx)
                

    def save_category_db(self, cates, key, url, ctx):
        is_new = is_updated = False
        category = Category.objects(key=key).first()
        if not category:
            is_new = True
            category = Category(key=key)
            category.is_leaf = True
            category.cats = cates
        category.combine_url = url
        category.update_time = datetime.utcnow()
        category.save()
        common_saved.send(sender=ctx, obj_type='Category', key=key, url=url, is_new=is_new, is_updated=is_updated)



    def crawl_listing(self, url, ctx='', **kwargs):
        category = Category.objects(key=kwargs.get('key')).first()
        ret = self.fetch_page(url)
        tree = lxml.html.fromstring(ret)
        if url.endswith('resultsPerPage=96'):
            self.crawl_designers_listing(tree, category.key)
            return
        count = tree.cssselect('div#breadcrumbs span.productCount')
        count = int( count[0].text_content().strip() ) if count else 0
        pages = (count - 1) // 96 + 1

        for i in tree.cssselect('div#macysGlobalLayout div#thumbnails div.productThumbnail'):
            price = i.cssselect('div.prices div.priceSale span.priceSale')
            if not price:
                continue
            else:
                price = price[0].text_content().replace('Sale', '').replace('$', '').replace(',', '').strip()
            listprice = i.cssselect('div.prices div.priceSale span.priceBig')
            if not listprice:
                continue
            else:
                listprice = listprice[0].text_content().replace('$', '').repalce(',', '').strip()
            desc = i.cssselect('div.shortDescription a')[0]
            link = desc.get('href')
            link = link if link.startswith('http') else self.siteurl + link
            key = self.extract_product_key.match(link).group(1)
            title = desc.text_content().strip()
            self.save_product_to_db(key, link, title, price, listprice, category.key)

        for j in xrange(2, pages+1):
            ret = self.fetch_page('{0}&pageIndex={1}'.format(url, j))
            tree = lxml.html.fromstring(ret)
            for i in tree.cssselect('div#macysGlobalLayout div#thumbnails div.productThumbnail'):
                price = i.cssselect('div.prices div.priceSale span.priceSale')
                if not price:
                    continue
                else:
                    price = price[0].text_content().replace('Sale', '').replace('$', '').replace(',', '').strip()
                listprice = i.cssselect('div.prices div.priceSale span.priceBig')
                if not listprice:
                    continue
                else:
                    listprice = listprice[0].text_content().replace('$', '').repalce(',', '').strip()
                desc = i.cssselect('div.shortDescription a')[0]
                link = desc.get('href')
                link = link if link.startswith('http') else self.siteurl + link
                key = self.extract_product_key.match(link).group(1)
                title = desc.text_content().strip()

                self.save_product_to_db(key, link, title, price, listprice, category.key)

    def save_product_to_db(self, key, link, title, price, listprice, category_key):
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
        if price != product.price:
            product.price = price
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
            return

        if category_key not in product.category_key:
            product.category_key.append(category_key)
            is_updated = True
        if is_updated:
            product.list_update_time = datetime.utcnow()
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url,
                is_new=is_new, is_updated=((not is_new) and is_updated) )


    def crawl_designers_listing(self, tree, category_key, ctx)
        for i in tree.cssselect('div#se_localContentContainerNarrow div.productThumbnail'):
            price = i.cssselect('div.se_result_image div.prices div.priceSale span.priceSale')
            if not price:
                continue
            else:
                price = price[0].text_content().replace('Sale', '').replace('$', '').replace(',', '').strip()
            listprice = i.cssselect('div.se_result_image div.prices div.priceSale span.priceBig')
            if not listprice:
                continue
            else:
                listprice = listprice[0].text_content().replace('$', '').repalce(',', '').strip()
            link = i.cssselect('div.se_result_image div.shortDescription a[href]')[0].get('href')
            link = link if link.startswith('http') else self.siteurl + link
            key = self.extract_product_key.match(link).group(1)
            title = i.cssselect('div.se_result_image div.shortDescription a[href]')[0].text_content().strip()

            self.save_product_to_db(key, link, title, price, listprice, category.key)

    def crawl_product(self, url, ctx='', **kwargs):
        ret = fetch_page(url)
        tree = lxml.html.fromstring(ret)
        summary = tree.cssselect('div#pdp_tabs_body_left div.pdp_longDescription')[0].text_content()
        list_info = []
        for li in tree.cssselect('div#pdp_tabs_body_left ul li#productDetailsBulletText'):
            list_info.append( li.text_content().strip() )
        image_urls = []
        img = tree.cssselect('img#mainProductImageZoom')[0].get('src')
        wid = re.compile('.*wid=(\d+)').match(img).group(1)
        image_urls.append( img )

        is_new = is_updated = False
        product = Product.objects(key=key).first()
        if not product:
            is_new = True
            product = Product(key=key)
            product.event_type = False

        product.summary = summary
        product.image_urls = image_urls
        product.full_update_time = datetime.utcnow()
        product.updated = True
        product.save()
        ready = True
        common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url,
                is_new=is_new, is_updated=((not is_new) and is_updated), ready=ready)




if __name__ == '__main__':
    ss = Server()
    ss.crawl_category()
