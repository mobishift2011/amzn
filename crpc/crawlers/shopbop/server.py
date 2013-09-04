#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
from datetime import datetime

from models import *
from crawlers.common.stash import *
from crawlers.common.events import common_failed, common_saved
from deals.picks import Picker

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,en-US;q=0.8,en;q=0.6',
    'Host': 'www.shopbop.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Ubuntu Chromium/25.0.1364.160 Chrome/25.0.1364.160 Safari/537.22',
}

req = requests.Session(prefetch=True, timeout=30, config=config, headers=header)

class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.shopbop.com'

    def fetch_page(self, url):
        ret = req.get(self.siteurl)
        if ret.ok: return ret.content
        else: return ret.status_code

    def crawl_category(self, ctx='', **kwargs):
        ret = self.fetch_page(self.siteurl)
        if isinstance(ret, int):
            common_failed.send(sender=ctx, key='', url=self.siteurl,
                    reasone='download home page error: {0}'.format(ret))
            return
        tree = lxml.html.fromstring(ret)
        top_nodes = tree.cssselect('ul#navList li.navCategory')
        for node in top_nodes:
            dept = node.cssselect('a')[0].text_content().strip()
            if dept == 'Designers':
                continue
                link = node.cssselect('a')[0].get('href')
                link = link if link.startswith('http') else self.siteurl + link

                ret = requests.get(link, headers=header).content
                tr = lxml.html.fromstring(ret)
                for br in tr.cssselect('div[id^="column"] div.brandGrouping a.designerLink'):
                    href = br.get('href')
                    href = href if href.startswith('http') else self.siteurl + href
                    key = br.text_content().strip()
                    num = self.crawl_number_in_listing(href)
                    self.save_category(key, href, num, [dept, key], ctx)
                continue
            if dept == 'Sale':
                link = node.cssselect('a')[0].get('href')
                link = link if link.startswith('http') else self.siteurl + link
                key = link.rsplit('/', 1)[-1].split('.')[0]
                num = self.crawl_number_in_listing(link)
                self.save_category('sale', link, num, [dept], ctx)
                continue
            if dept == 'Boutiques':
                for sub in node.cssselect('ul.submenu li.menuItem a'):
                    link = sub.get('href')
                    link = link if link.startswith('http') else self.siteurl + link
                    sub_dept = sub.text_content().strip()

                    ret = requests.get(link, headers=header).content
                    tr = lxml.html.fromstring(ret)
                    for atag in tr.cssselect('div#leftNavigation ul.leftNavCategory li.leftNavCategoryLi ul.leftNavSubcategory li a'):
                        link = atag.get('href')
                        link = link if link.startswith('http') else self.siteurl + link
                        sub_sub_dept = atag.text_content().strip()
                        key = link.rsplit('/', 1)[-1].split('.')[0]
                        if not key.isdigit(): continue
                        num = self.crawl_number_in_listing(link)
                        self.save_category(key, link, num, [dept, sub_dept, sub_sub_dept], ctx)
                continue
            if dept == 'Lookbooks':
                break

            sub_nodes = node.cssselect('ul.submenu li.menuItem a')
            for sub in sub_nodes:
                link = sub.get('href')
                link = link if link.startswith('http') else self.siteurl + link
                sub_dept = sub.text_content().strip()
                key = link.rsplit('/', 1)[-1].split('.')[0]
                num = self.crawl_number_in_listing(link)
                self.save_category(key, link, num, [dept, sub_dept], ctx)


    def save_category(self, key, combine_url, num, cats, ctx):
        is_new = is_updated = False
        category = Category.objects(key=key).first()
        if not category:
            is_new = True
            category = Category(key=key)
            category.is_leaf = True
            category.pagesize = 100
        category.num = num
        category.cats = cats
        category.combine_url = combine_url
        category.save()
        common_saved.send(sender=ctx, obj_type='Category', key=key, url=combine_url, is_new=is_new, is_updated=is_updated)


    def crawl_number_in_listing(self, url):
#        ret = self.fetch_page(url)
#        if isinstance(ret, int):
#            common_failed.send(sender=ctx, key='', url=url,
#                    reasone='download listing page error: {0}'.format(ret))
#            return
        ret = requests.get(url, headers=header).content
        tree = lxml.html.fromstring(ret)
        num = tree.cssselect('div#searchResultCount')[0].text_content().strip()
        num = int( re.compile('(\d+).*').match(num).group(1) )
        return num

    def crawl_listing(self, url, ctx='', **kwargs):
        category = Category.objects(key=kwargs.get('key')).first()
        ret = requests.get(url, headers=header).content
        if isinstance(ret, int):
            common_failed.send(sender=ctx, key='', url=url,
                    reasone='download listing page error: {0}'.format(ret))
            return
        tree = lxml.html.fromstring(ret)
        for prd in tree.cssselect('table#productTable tr td div#productContainer'):
            price = prd.cssselect('div.productInfo span.salePrice')
            if not price:
                continue
            else:
                price = price[0].text_content().replace(',', '').replace('$', '').strip()
            brand = prd.cssselect('div.productInfo div.productBrand')[0].text_content().strip()
            title = prd.cssselect('div.productInfo div.productTitle')[0].text_content().strip()
            link = prd.cssselect('a.productDetailLink')[0].get('href')
            link = link if link.startswith('http') else self.siteurl + link
            # image = prd.cssselect('a.productDetailLink img.image')[0].get('src')
            combine_url, key = re.compile('(.+v=1/(\d+).htm).*').match(link).groups()
            detail = self.crawl_detail(combine_url)
            if detail is None:
                continue
            listprice, summary, shipping, image_urls = detail

            is_new = is_updated = False
            product = Product.objects(key=key).first()
            if not product:
                is_new = True
                product = Product(key=key)
                product.event_type = False
                product.updated = False
                product.brand = brand

            if title and title != product.title:
                product.title = title
                product.update_history.update({ 'title': datetime.utcnow() })
                is_updated = True
            if price and price != product.price:
                product.price = price
                product.update_history.update({ 'price': datetime.utcnow() })
                is_updated = True
            if listprice and listprice != product.listprice:
                product.listprice = listprice
                product.update_history.update({ 'listprice': datetime.utcnow() })
                is_updated = True
            if combine_url and combine_url != product.combine_url:
                product.combine_url = combine_url
                product.update_history.update({ 'combine_url': datetime.utcnow() })
                is_updated = True

            selected = Picker(site=DB).pick(product)
            if not selected:
                continue

            if category.key not in product.category_key:
                product.category_key.append(category.key)
                is_updated = True
            if is_updated:
                product.list_update_time = datetime.utcnow()

            product.summary = summary
            product.shipping = shipping
            product.image_urls = image_urls
            product.full_update_time = datetime.utcnow()
            product.updated = True
            product.save()
            ready = True
            common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url,
                    is_new=is_new, is_updated=((not is_new) and is_updated), ready=ready)

    def crawl_detail(self, url):
        ret = requests.get(url, headers=header).content
        if isinstance(ret, int):
            common_failed.send(sender=ctx, key='', url=url,
                    reasone='download product page error: {0}'.format(ret))
            return
        tree = lxml.html.fromstring(ret)
        listprice = tree.cssselect('div#productPrices div.priceBlock span.originalRetailPrice')
        if not listprice:
            return
        else:
            listprice = listprice[0].text_content().replace(',', '').replace('$', '').strip()
        summary = tree.cssselect('div#longDescriptionContainer')[0].text_content().strip()
        shipping = tree.cssselect('div#freeDeliveriesContainer')[0].text_content().strip()
        image_urls = []
        for i in tree.cssselect('ul#thumbnailList li.thumbnailListItem img.thumbImages'):
            img = i.get('src')
            img = ''.join( re.compile('(.*)_\d+x\d+(.*)').match(img).groups() )
            if img not in image_urls:
                image_urls.append(img)
        return listprice, summary, shipping, image_urls


    def crawl_product(self, url, ctx='', **kwargs):
        pass


if __name__ == '__main__':
    ss = Server()
    ss.crawl_category()
