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
from datetime import datetime
import re

header = {
    'Host': 'http://www.wine.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.2) Gecko/20121028 Firefox/15.2.1 PaleMoon/15.2.1',
}

req = requests.Session(prefetch=True, timeout=30, config=config, headers=header)

LOGIN_URL = 'https://www.wineshopper.com/Account/EntryNew.aspx?next=%7e%2fCurrent-Events.aspx'

class Server(object):
    def __init__(self):
        pass

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

    def crawl_category(self, ctx='', **kwargs):
        self.crawl_category_by_api(ctx, **kwargs)

    def crawl_listing(self, url, ctx='', **kwargs):
        pass

    def crawl_product(self, url, ctx='', **kwargs):
        self.crawl_product_from_api(url, ctx, **kwargs)


if __name__ == '__main__':
    # import zerorpc
    # from settings import CRAWLER_PORT
    # server = zerorpc.Server(Server())
    # server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
    # server.run()

    s = Server()
    # s.crawl_category()
    s.crawl_product(url="http://www.wine.com/V6/Antano-Viura-2009/wine/108770/detail.aspx")