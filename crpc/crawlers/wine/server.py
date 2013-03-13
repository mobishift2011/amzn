#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ethan <ethan@favbuy.com>

"""
crawlers.wine.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.
"""
from crawlers.common.stash import *
from crawlers.common.events import common_saved, common_failed
from models import Product
from deals.picks import Picker
import requests
import lxml.html
import traceback
from datetime import datetime, timedelta
import re

WINESHOPPER_HOST = 'www.wineshopper.com'

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Content-Length': '3473',
    'Host': WINESHOPPER_HOST,
    'Origin': 'http://' + WINESHOPPER_HOST,
    'Referer': 'http://www.wineshopper.com/default.aspx?next=~/Current-Events.aspx',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11'
}

req = requests.Session(prefetch=True, config=config, headers=header)

def login_deal_page():
    LOGIN_PAGE = 'http://www.wineshopper.com/default.aspx'
    LOGIN_URL = 'https://www.wineshopper.com/Account/EntryNew.aspx'
    url = 'http://www.wineshopper.com/Current-Events.aspx'
    res = req.get(url)
    res.raise_for_status()
    tree = lxml.html.fromstring(res.content)
    
    if  LOGIN_PAGE in res.url:
        form = tree.cssselect('form#aspnetForm')[0]
        data = {
            '__LASTFOCUS': form.cssselect('input#__LASTFOCUS')[0].get('value'),
            '__EVENTTARGET': form.cssselect('input#__EVENTTARGET')[0].get('value'),
            '__EVENTARGUMENT': form.cssselect('input#__EVENTARGUMENT')[0].get('value'),
            '__VIEWSTATE': form.cssselect('input#__VIEWSTATE')[0].get('value'),
            '__PREVIOUSPAGE': form.cssselect('input#__PREVIOUSPAGE')[0].get('value'),
            '__EVENTVALIDATION': form.cssselect('input#__EVENTVALIDATION')[0].get('value'),
            'ctl00$Content$SignInNew$txtEmailAddress': '2012luxurygoods@gmail.com',
            'ctl00$Content$SignInNew$txtPassword': 'abcd1234',
            'ctl00$Content$SignInNew$btnSubmitAlt': '',
        }

        res = req.post(LOGIN_URL, data=data)
        return res

class Server(object):
    def __init__(self):
        pass

    def crawl_deal_node(self, event_node, ctx='', **kwargs):
        title_node = event_node.cssselect('h2 a')[0]
        title = title_node.text.strip()
        combine_url = title_node.get('href')
        desc = ''.join(event_node.cssselect('h3')[0].xpath('.//text()')).strip()

        pattern = r'\?eventId=(\d+)'
        key = re.search(pattern, combine_url).groups()[0]
        key = 'event_%s' % key

        match = re.search(r'https?://.+', combine_url)
        if not match:
            combine_url = 'http://%s%s' % (WINESHOPPER_HOST, combine_url)

        shop_block_node = event_node.cssselect('div.shopBlock')
        soldout = True \
            if shop_block_node and 'soldout' in shop_block_node[0].get('id').lower() \
                else False

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

        if desc and desc != product.short_desc:
            product.short_desc = desc
            is_updated = True

        products_end = kwargs.get('products_end')
        if products_end and products_end != product.products_end:
            product.products_end = products_end
            is_updated = True

        if soldout and soldout != product.soldout:
            product.soldout = soldout
            is_updated = True

        if is_updated:
            product.list_update_time = datetime.utcnow()

        product.hit_time = datetime.utcnow()
        product.save()

        print product.key
        print product.title
        print product.combine_url
        print product.short_desc
        print product.products_end
        print product.soldout
        print product.updated
        print is_new
        print is_updated
        print 

        common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, \
            is_new=is_new, is_updated=((not is_new) and is_updated) )

    def crawl_category_by_deals(self, ctx='', **kwargs):
        res = login_deal_page()
        now = datetime.utcnow()
        res.raise_for_status()
        content = res.content
        tree = lxml.html.fromstring(content)
        pattern = r"until: '\+(\d+)d \+(\d+)h \+(\d+)m \+(\d+)'"

        event_nodes = tree.cssselect('div.subEvents div.subEvent')
        for event_node in event_nodes:
            script_text = event_node.cssselect('script')[0].text
            days, hours, minutes, seconds = (int(t) for t in re.search(pattern, script_text).groups())
            products_end = now + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
            products_end = products_end.replace(second=0, microsecond=0) # To eliminate the deviation that will lead to the update.
            self.crawl_deal_node(event_node.cssselect('div.subEvent div.rightBlock')[0], ctx=ctx, products_end=products_end)

        feature_node = tree.cssselect('div.featureEvent div.leftBlock')[0]
        feature_script_text = tree.cssselect('div#content script')[0].text
        days, hours, minutes, seconds = (int(t) for t in re.search(pattern, feature_script_text).groups())
        feature_products_end = now + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        feature_products_end = feature_products_end.replace(second=0, microsecond=0) # To eliminate the deviation that will lead to the update.
        self.crawl_deal_node(feature_node, ctx=ctx, products_end=feature_products_end)

    def crawl_category_by_api(self, ctx='', **kwargs):
        payload = {
            'apikey': '3c703ecba587c33cede89712cd17ede5',
            'size': 600,
            'offset': kwargs.get('offset', 0)
        }
        url = 'http://services.wine.com/api/beta2/service.svc/json/catalog'
        res = requests.get(url, params=payload)
        res.raise_for_status()
        json_res = res.json
        if json_res['Status']['ReturnCode'] != 0:
            common_failed.send(sender=ctx, url=url, reason='Product data feed error: %s -> %s' \
                % (json_res['Status']['ReturnCode'], json_res['Status']['Messages'])); return

        # Finish when go over the last page of the data.
        product_list = json_res['Products']['List']
        if not product_list:
            return

        for element in product_list:
            key = element['Id']
            title = element['Name']
            combine_url = element['Url']
            dept_type = element['Type']
            appellation = element['Appellation']['Name'] if element.get('Appellation') else None
            varietal, winetype = (element['Varietal']['Name'], element['Varietal']['WineType']['Name']) if element.get('Varietal') else (None, None)
            vineyard = element['Vineyard']['Name'] if element.get('Vineyard') else None
            price = element['PriceMin']
            listprice = element['PriceRetail']
            rating = element['Ratings']['HighestScore']

            is_new = False; is_updated = False
            product = Product.objects(key=str(key)).first()
            if not product:
                is_new = True
                product = Product(key=str(key))

            if title and title != product.title:
                product.title = title
                is_updated = True

            if combine_url and combine_url != product.combine_url:
                product.combine_url = combine_url
                is_updated = True

            if dept_type and dept_type not in product.dept:
                product.dept.append(dept_type)
                is_updated = True

            if winetype and winetype not in product.dept:
                product.dept.append(winetype)
                is_updated = True

            if appellation and ('Appellation: %s' % appellation) not in product.list_info:
                product.list_info.append(('Appellation: %s' % appellation))
                is_updated = True

            if varietal and ('Varietal: %s' % varietal) not in product.list_info:
                product.list_info.append(('Varietal: %s' % varietal))
                is_updated = True

            if vineyard and ('Vineyard: %s' % vineyard) not in product.list_info:
                product.list_info.append(('Vineyard: %s' % vineyard))
                is_updated = True

            if price and str(price) != product.price:
                product.price = str(price)
                is_updated = True

            if listprice and str(listprice) != product.price:
                product.listprice = str(listprice)
                is_updated = True

            if rating and str(rating) != product.rating:
                product.rating = str(rating)

            if is_updated:
                if is_new:
                    # To pick the product which fit our needs, such as a certain discount, brand, dept etc.
                    selected = Picker(site='wine').pick(product)
                    if not selected:
                        continue

                product.list_update_time = datetime.utcnow()
                product.hit_time = datetime.utcnow()
                product.save()

            print product.title
            print product.dept
            print product.combine_url
            print product.price, product.listprice
            print product.rating
            for list_info in product.list_info:
                print list_info
            print is_new
            print is_updated
            print

            common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, \
                is_new=is_new, is_updated=((not is_new) and is_updated) )

        # To crawl the next page of the product data.
        offset = payload['offset'] + payload['size']
        self.crawl_category_by_api(ctx, offset=offset)

    def crawl_product_from_api(self, url, ctx='', **kwargs):
        res = requests.get(url)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)

        image_nodes = tree.cssselect('div#wineImage image')
        image_urls = [image_node.get('src') for image_node in image_nodes]

        soldout_node = tree.cssselect("span#ctl00_BodyContent_wctAbstract_lblSoldOut")
        # soldout = True if soldout_node and "sold out" in soldout_node[0].text
        print soldout_node

        span_node = tree.cssselect('table.grossTable tr td div span')
        print len(span_node)

    def crawl_product_by_deals(self, url, ctx='', **kwargs):
        key = kwargs.get('key', '')
        product = Product.objects(key=key).first()

        if not product:
            common_failed.send(sender=ctx, url=url, reason='product not exists -> %s' % kwargs)
            return

        login_deal_page()
        res = req.get(url)
        res.raise_for_status()
        tree = lxml.html.fromstring(res.content)
        product_node = tree.cssselect('div.product')[0]

        image_nodes = product_node.cssselect('div.leftBlock div.label img')
        image_urls = [image_node.get('src') for image_node in image_nodes]

        right_node = product_node.cssselect('div.rightBlock')[0]
        title = right_node.cssselect('div.contentBlock h1')[0].text.strip()
        list_info = [right_node.cssselect('div.details')[0].text_content().strip()]

        shop_node = right_node.cssselect('div.shopBlock')[0]
        price_nodes = shop_node.cssselect('div.priceBlock div.price span')
        listprice = None; price = None
        for price_node in price_nodes:
            if 'retail' in price_node.get('class'):
                listprice = price_node.text.strip()
            if 'sales' in price_node.get('class'):
                price = price_node.text.strip()

        # update product
        is_new = False; is_updated = False; ready = False

        if title and not product.title:
            product.title = title
            is_updated = True

        if image_urls and image_urls != product.image_urls:
            product.image_urls = image_urls
            is_updated = True

        if price and price != product.price:
            product.price = price
            is_updated = True

        if listprice and listprice != product.listprice:
            product.listprice = listprice
            is_updated = True

        if list_info and list_info != product.list_info:
            product.list_info = list_info
            is_updated = True

        if is_updated:
            ready = True if not product.updated else False
            product.updated = True
            product.full_update_time = datetime.utcnow()
            product.save()

        print product.key, product.title
        print product.image_urls
        print product.price, '/', product.listprice
        print product.updated
        print ready
        print is_new
        print is_updated
        print

        common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, \
            is_new=is_new, is_updated=((not is_new) and is_updated), ready=ready)

    def crawl_category(self, ctx='', **kwargs):
        self.crawl_category_by_deals(ctx, **kwargs)
        # self.crawl_category_by_api(ctx, **kwargs)

    def crawl_listing(self, url, ctx='', **kwargs):
        pass

    def crawl_product(self, url, ctx='', **kwargs):
        if kwargs.get('key', '').startswith('event_'):
            self.crawl_product_by_deals(url, ctx, **kwargs)
        else:
            self.crawl_product_from_api(url, ctx, **kwargs)


if __name__ == '__main__':
    # import zerorpc
    # from settings import CRAWLER_PORT
    # server = zerorpc.Server(Server())
    # server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
    # server.run()

    s = Server()
    # s.crawl_category()
    for product in Product.objects():
        s.crawl_product(product.combine_url, ctx='wine.product.'+product.key, key=product.key)