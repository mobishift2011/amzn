#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.zulily.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool

import os
import re
import sys
import time
import zerorpc
import lxml.html
import pytz

from urllib import quote, unquote
from datetime import datetime, timedelta

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *

req = requests.Session(prefetch=True, timeout=17, config=config, headers=headers)

class zulilyLogin(object):
    """.. :py:class:: zulilyLogin
        login, check whether login, fetch page.
    """
    def __init__(self):
        """.. :py:method::
            variables need to be used
        """
        self.login_url = 'https://www.zulily.com/auth'
        self.data = {
            'login[username]': login_email,
            'login[password]': login_passwd
        }
        self.reg_check = re.compile(r'https://www.zulily.com/auth/create.*')
        self._signin = False

    def login_account(self):
        """.. :py:method::
            use post method to login
        """
        req.post(self.login_url, data=self.data)
        self._signin = True

    def check_signin(self):
        """.. :py:method::
            check whether the account is login
        """
        if not self._signin:
            self.login_account()

    def fetch_page(self, url):
        """.. :py:method::
            fetch page.
            check whether the account is login, if not, login and fetch again
        """
        ret = req.get(url)

        if self.reg_check.match(ret.url) is not None: # need to authentication
            self.login_account()
            ret = req.get(url)
        if ret.ok: return ret.content
        return ret.status_code



class Server(object):
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    def __init__(self):
        self.siteurl = 'http://www.zulily.com'
        self.upcoming_url = 'http://www.zulily.com/upcoming_events'
        self.net = zulilyLogin()
        self.extract_event_id = re.compile(r'(http://www.zulily.com/e/(.*).html).*')
        self.extract_event_img = re.compile(r'(http://mcdn.zulily.com/images/cache/event/)\d+x\d+/(.+)')
        self.extract_product_img = re.compile(r'(http://mcdn.zulily.com/images/cache/product/)\d+x\d+/(.+)')
        self.extract_product_re = re.compile(r'http://www.zulily.com/p/(.+).html.*')

        self.returned_re = re.compile(r'<strong>Return Policy:</strong>(.*)<a')
        self.shipping_re = re.compile(r'<strong>Shipping:</strong>(.*)<a')

    def crawl_category(self, ctx):
        """.. :py:method::
            From top depts, get all the events
        """
        depts = ['girls', 'boys', 'women', 'baby-maternity', 'toys-playtime', 'home']
        debug_info.send(sender=DB + '.category.begin')

        self.upcoming_proc(ctx)
        for dept in depts:
            link = 'http://www.zulily.com/?tab={0}'.format(dept)
            self.get_event_list(dept, link, ctx)
        debug_info.send(sender=DB + '.category.end')

    def get_event_list(self, dept, url, ctx):
        """.. :py:method::
            Get all the brands from brand list.
            Brand have a list of product.

        :param dept: dept in the page
        :param url: the dept's url
        """
        cont = self.net.fetch_page(url)
        tree = lxml.html.fromstring(cont)
        nodes = tree.xpath('//div[@class="container"]/div[@id="main"]/div[@id="home-page-content"]/div[@class="clearfix"]//div[starts-with(@id, "eid_")]')
        
        for node in nodes:
            link = node.xpath('./a[@class="wrapped-link"]')[0].get('href')
            link, event_id = self.extract_event_id.match(link).groups()
            text = node.xpath('./a/span[@class="txt"]')[0]

            brand, is_new = Event.objects.get_or_create(event_id=event_id)
            if is_new:
                img = node.xpath('./a/span[@class="homepage-image"]/img/@src')[0]
                image = ''.join( self.extract_event_img.match(img).groups() )
                sale_title = text.xpath('./span[@class="category-name"]/span/text()')[0]

                brand.image_urls = [image]
                brand.sale_title = sale_title
                brand.short_desc = text.xpath('.//span[@class="description-highlights"]/text()')[0].strip()
                brand.start_end_date = text.xpath('./span[@class="description"]/span[@class="start-end-date"]')[0].text_content().strip()
                brand.urgent = True
            if dept not in brand.dept: brand.dept.append(dept) # events are mixed in different category
            brand.is_leaf = True
            brand.update_time = datetime.utcnow()
            brand.save()
            common_saved.send(sender=ctx, key=event_id, url=url, is_new=is_new, is_updated=False)


    def upcoming_proc(self, ctx):
        """.. :py:method::
            Get all the upcoming brands info 
        """
        upcoming_list = []
        cont = self.net.fetch_page(self.upcoming_url)
        tree = lxml.html.fromstring(cont)
        nodes = tree.xpath('//div[@class="event-content-list-wrapper"]/ul/li/a')
        for node in nodes:
            link = node.get('href')
            text = node.text_content()
            upcoming_list.append( (text, link) )
        self.upcoming_detail(upcoming_list, ctx)

    def upcoming_detail(self, upcoming_list, ctx):
        """.. :py:method::
        """
        for pair in upcoming_list:
            cont = self.net.fetch_page(pair[1])
            node = lxml.html.fromstring(cont).cssselect('div.event-content-wrapper')[0]
            calendar_file = node.cssselect('div.upcoming-date-reminder a.reminder-ical')[0].get('href')
            ics_file = self.net.fetch_page(calendar_file)
            event_id = re.compile(r'URL:http://www.zulily.com/e/(.+).html.*').search(ics_file).group(1)
            brand, is_new = Event.objects.get_or_create(event_id=event_id)
            if is_new:
                img = node.cssselect('div.event-content-image img')[0].get('src')
                image = ''.join( self.extract_event_img.match(img).groups() )
                sale_title = node.cssselect('div.event-content-copy h1')[0].text_content()
                sale_description = node.cssselect('div.event-content-copy div#desc-with-expanded')[0].text_content().strip()
                start_time = node.cssselect('div.upcoming-date-reminder span.reminder-text')[0].text_content() # 'Starts Sat 10/27 6am pt - SET REMINDER'
                events_begin = time_convert( ' '.join( start_time.split(' ', 4)[1:-1] ), '%a %m/%d %I%p%Y' ) #'Sat 10/27 6am'

                brand.image_urls = [image]
                brand.sale_title = sale_title 
                brand.sale_description = sale_description
                brand.events_begin = events_begin
                brand.update_time = datetime.utcnow()
                brand.save()
                common_saved.send(sender=ctx, key=event_id, url=pair[1], is_new=is_new, is_updated=not is_new)
            

    def crawl_listing(self, url, ctx):
        """.. :py:method::
            from url get listing page.
            from listing page get Eventi's description, endtime, number of products.
            Get all product's image, url, title, price, soldout

        :param url: listing page url
        """
        debug_info.send(sender=DB + '.crawl_list.begin')
        cont = self.net.fetch_page(url)
        tree = lxml.html.fromstring(cont)
        node = tree.cssselect('div.container>div#main>div#category-view')[0]
        event_id = self.extract_event_id.match(url).group(2)
        brand, is_new = Event.objects.get_or_create(event_id=event_id)
        if is_new or brand.sale_description is None:
            sale_description = node.cssselect('div#category-description>div#desc-with-expanded')
            if not sale_description:
                sale_description = node.cssselect('div#category-view-brand > div.category-description-bg > div.category-view-brand-description > p:first-of-type')
            if sale_description:
                brand.sale_description = sale_description[0].text_content().strip()

        items = node.cssselect('div#products-grid li.item')
        end_date = node.cssselect('div#new-content-header>div.end-date')[0].text_content().strip()
        end_date = end_date[end_date.find('in')+2:].strip() # '2 hours' or '1 day(s) 3 hours'
        days = int(end_date.split()[0]) if 'day' in end_date else 0
        hours = int(end_date.split()[-2]) if 'hour' in end_date else 0
        brand.events_end = datetime.utcnow() + timedelta(days=days, hours=hours)
        brand.num = len(items)
        brand.update_time = datetime.utcnow()
        brand.urgent = False
        brand.save()
        common_saved.send(sender=ctx, key=event_id, url=url, is_new=is_new, is_updated=False)

        for item in items: self.crawl_list_product(event_id, item, ctx)
        page_num = 1
        next_page_url = self.detect_list_next(node, page_num + 1)
        if next_page_url:
            self.crawl_list_next(url, next_page_url, page_num + 1, event_id, ctx)
        debug_info.send(sender=DB + '.crawl_list.end')

    def detect_list_next(self, node, page_num):
        """.. :py:method::
            detect whether the listing page have a next page

        :param node: the node generate by crawl_listing
        :param page_num: page number of this event
        """
        next_page = node.cssselect('div#pagination>a[href]') # if have next page
        if next_page:
            next_page_relative_url = next_page[-1].get('href')
            if str(page_num) in next_page_relative_url:
                return next_page_relative_url

    def crawl_list_next(self, url, page_text, page_num, event_id, ctx):
        """.. :py:method::
            crawl listing page's next page, that is page 2, 3, 4, ...

        :param url: listing page url
        :param page_text: this page's relative url
        :param page_num: page number of this event
        :param event_id: unique key in Event, which we can associate product with event
        """
        cont = self.net.fetch_page(url + page_text)
        tree = lxml.html.fromstring(cont)
        node = tree.cssselect('div.container>div#main>div#category-view')[0]
        items = node.cssselect('div#products-grid li.item')

        for item in items: self.crawl_list_product(event_id, item, ctx)
        next_page_url = self.detect_list_next(node, page_num + 1)
        if next_page_url:
            self.crawl_list_next(url, next_page_url, page_num + 1, event_id, ctx)

    def crawl_list_product(self, event_id, item, ctx):
        """.. :py:method::
            In listing page, Get all product's image, url, title, price, soldout

        :param event_id: unique key in Event, which we can associate product with event
        :param item: item of xml node
        """
        title_link = item.cssselect('div.product-name>a[title]')[0]
        title = title_link.get('title').strip()
        link = title_link.get('href')
        slug = self.extract_product_re.match(link).group(1)
        product, is_new = Product.objects.get_or_create(pk=slug)
        price_box = item.cssselect('a>div.price-boxConfig')
        is_updated = False
        if is_new:
            product.event_id = [event_id]
            img = item.cssselect('a.product-image>img')[0].get('src')
            image = ''.join( self.extract_product_img.match(img).groups() )
            product.image_urls = [image]
            product.title = title
            if price_box:
                product.price = price_box[0].cssselect('div.special-price')[0].text.strip().replace('$','').replace(',','')
                product.listprice = price_box[0].cssselect('div.old-price')[0].text.replace('original','').strip().replace('$','').replace(',','')
            else:
                product.price = item.cssselect('a.nohover')[0].text.strip().replace('$','').replace(',','')
            soldout = item.cssselect('a.product-image>span.sold-out')
            if soldout: product.soldout = True
            product.updated = False
        else:
            if event_id not in product.event_id:
                product.event_id.append(event_id)

            soldout = item.cssselect('a.product-image>span.sold-out')
            if price_box:
                special_price = price_box.cssselect('div.special-price')[0].text.strip().replace('$','').replace(',','')
            else:
                special_price = item.cssselect('a.nohover')[0].text.strip().replace('$','').replace(',','')
            if product.price != special_price:
                product.price = special_price
                is_updated = True
            if soldout and product.soldout != True:
                product.soldout = True
                is_updated = True
#        product.brand = sale_title
        product.list_update_time = datetime.utcnow()
        product.save()
        common_saved.send(sender=ctx, key=slug, url=self.siteurl + '/e/' + event_id + '.html', is_new=is_new, is_updated=is_updated)
        debug_info.send(sender=DB + ".crawl_listing", url=self.siteurl + '/e/' + event_id + '.html')


    def crawl_product(self, url, ctx):
        """.. :py:method::
            Got all the product information and save into the database

        :param url: product url
        """
        cont = self.net.fetch_page(url)
        if isinstance(cont, int):
            common_failed.send(sender=ctx, url=url, reason=cont)
            return
        tree = lxml.html.fromstring(cont)
        node = tree.cssselect('div.container>div#main>div#product-view')[0]
        info = node.cssselect('div#product-info')[0]
        list_info, image_urls, out_of_stocks, also_like, sizes_scarcity = [], [], [], [], []

#        summary = info.cssselect('div#product-description>div.description p:first-child')[0].text_content()
        summary = info.cssselect('div#product-description>div.description')
        description = summary[0].text_content().strip() if summary else ''
        for info in info.cssselect('div#product-description>div.description>ul>li'):
            list_info.append(info.text_content())
#        return_shipping = info.cssselect('ul#product-bullets>li')  # not work
#        returned = return_shipping[0].text_content()
#        shipping = return_shipping[1].text_content()
        returned = self.returned_re.search(cont).group(1).strip()
        m = self.shipping_re.search(cont)
        shipping = m.group(1).strip() if m else ''
        size_scarcity = info.cssselect('div.options-container-big div#product-size-dropdown>select>option[data-inventory-available]')
        for s_s in size_scarcity:
            sizes_scarcity.append( (s_s.text_content().strip(), s_s.get('data-inventory-available')) )
        for out_of_stock in info.cssselect('div#out-of-stock-notices>div.size-out-of-stock'):
            out_of_stocks.append( out_of_stock.text )

        images = node.cssselect('div#product-media>div#MagicToolboxSelectorsContainer>ul.reset>li>a>img')
        for img in images:
            picture = ''.join( self.extract_product_img.match(img.get('src')).groups() )
            image_urls.append(picture)
        also_like_items = node.cssselect('div#product-media>div#you-may-also-like>ul>li>a')
        for a_l in also_like_items:
            also_like.append( (a_l.get('title'), a_l.get('href')) )

        slug = self.extract_product_re.match(url).group(1)
        product, is_new = Product.objects.get_or_create(pk=slug)
        if description: product.summary = description
        if list_info: product.list_info = list_info
        product.returned = returned
        if shipping: product.shipping = shipping
        if sizes_scarcity: product.sizes_scarcity = sizes_scarcity
        if out_of_stocks: product.out_of_stocks = out_of_stocks
        if image_urls: product.image_urls = image_urls

        product.updated = True
        product.full_update_time = datetime.utcnow()
        product.save()
        common_saved.send(sender=ctx, key=slug, url=url, is_new=is_new, is_updated=not is_new)

        

if __name__ == '__main__':
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
    server.run()
