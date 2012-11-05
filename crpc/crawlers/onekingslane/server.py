#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.onekingslane.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""
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

headers = {
    'Host': 'www.onekingslane.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.2) Gecko/20121028 Firefox/15.2.1 PaleMoon/15.2.1',
    'Referer': 'https://www.onekingslane.com/login',
}
config = { 
    'max_retries': 5,
    'pool_connections': 10, 
    'pool_maxsize': 10, 
}
req = requests.Session(prefetch=True, timeout=17, config=config, headers=headers)


class onekingslaneLogin(object):
    """.. :py:class:: onekingslaneLogin
        login, check whether login, fetch page.
    """
    def __init__(self):
        """.. :py:method::
            variables need to be used
        """
        self.login_url = 'https://www.onekingslane.com/login'
        self.data = { 
            'email': login_email,
            'password': login_passwd,
            'keepLogIn': 1,
            'sumbit.x': 54,
            'sumbit.y': 7,
            'returnUrl': '0',
        }   
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

        if ret.ok: return ret.content
        return ret.status_code



class Server(object):
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    def __init__(self):
        self.siteurl = 'https://www.onekingslane.com'
        self.upcoming_url = 'https://www.onekingslane.com/calendar'
        self.net = onekingslaneLogin()
        self.extract_eventid = re.compile('https://www.onekingslane.com/sales/(\d+)')
        self.extract_large_img = re.compile('(.*\?)\$.*\$')

    def crawl_category(self, ctx):
        """.. :py:method::
            From top depts, get all the events
        """
        debug_info.send(sender=DB + '.category.begin')

        self.upcoming_proc(ctx)
        self.get_sale_list(ctx)
        debug_info.send(sender=DB + '.category.end')

    def get_sale_list(self, ctx):
        """.. :py:method::
            Get all the brands from brand list.
            Brand have a list of product.

        :param dept: dept in the page
        :param url: the dept's url
        """
        cont = self.net.fetch_page(self.siteurl)
        tree = lxml.html.fromstring(cont)
        nodes = tree.cssselect('body.holiday > div#wrapper > div#okl-content > div#previewWrapper > div.eventsContainer > div.eventModule')
        for node in nodes:
            title = node.cssselect('div.eventInfo > div > h3')[0].text
            short_desc = node.cssselect('div.eventInfo > div > p')[0].text
            l = node.cssselect('a[href]')[0].get('href')
            link = l if l.startswith('http') else self.siteurl + l
            event_id = self.extract_eventid.match(link).group(1)

            brand, is_new = Event.objects.get_or_create(event_id=event_id)
            if is_new:
                event.sale_title = title
                event.short_desc = short_desc
                img = node.cssselect('div.eventStatus > a.trackEventPosition > img')[0].get('src')
                image = self.extract_large_img.match(img).group(1) + '$mp_hero_standard$'
                event.image_urls = [image]
            event.is_leaf = True
            event.update_time = datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, key=event_id, url=link, is_new=is_new, is_updated=not is_new)


    def upcoming_proc(self, ctx):
        """.. :py:method::
            Get all the upcoming brands info in upcoming url 
        """
        cont = self.net.fetch_page(self.upcoming_url)
        tree = lxml.html.fromstring(cont)
        nodes = tree.cssselect('body.holiday > div#wrapper > div#okl-content > div.calendar-r > div.day')
        for node in nodes:
            date = ' '.join( [d for d in node.cssselect('span.date')[0].text_content().split('\n') if d] )
            all_times = node.cssselect('div.all-times > h3')[0].text_content().split('PT')[0].split()[-1]
            date_begin = time_convert(date + ' ' + all_times + ' ', '%b %d %I%p %Y')
            markets = node.cssselect('div.all-times > ul > li')
            for market in markets:
                link = market.cssselect('h4 > a')[0].get('href')
                link = link if link.startswith('http') else self.siteurl + link
                event_id = self.extract_eventid.match(link).group(1)
                event, is_new = Event.objects.get_or_create(event_id=event_id)
                if is_new:
                    event.events_begin = date_begin
                    img = market.cssselect('h4 > a > img')[0].get('src') + '?$mp_hero_standard$'
                    event.image_urls = [img]
                    event.sale_title = market.cssselect('h4 > a')[0].text_content()
                    event.short_desc = market.cssselect('p.shortDescription')[0].text_content()
                    detail_tree = lxml.html.fromstring(self.net.fetch_page(link))
                    sale_description = detail_tree.cssselect('div#wrapper > div#okl-content > div.sales-event > div#okl-bio > div.event-description .description')
                    if sale_description:
                        event.sale_description = sale_description[0].text.strip()
                
                brand.update_time = datetime.utcnow()
                brand.save()
                common_saved.send(sender=ctx, key=event_id, url=link, is_new=is_new, is_updated=not is_new)

    def utcstr2datetime(self, date_str):
        """.. :py:method::
            covert time from the format into utcnow()
            '20121105T150000Z'
        """
        fmt = "%Y%m%dT%H%M%S"
        return datetime.strptime(date_str.rstrip('Z'), fmt)


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
        path = tree.cssselect('div#wrapper > div#okl-content > div.sales-event')
        event_id = self.extract_eventid.match(url).group(1)
        event, is_new = Event.objects.get_or_create(event_id=event_id)
        if not event.sale_description:
            sale_description = path.cssselect('div#okl-bio > div.event-description .description')
            if sale_description:
                event.sale_description = sale_description[0].text.strip()
        if not event.events_end:
            end_date = path.cssselect('div#okl-bio > h2.share')[0].get('data-end')
            event.events_end = self.utcstr2datetime(end_data)
        if is_new:
            event.sale_title = path.cssselect('div#okl-bio > h2.share > strong')[0].text

        items = path.cssselect('div#okl-product > ul.products > li[id^="product-tile-"]')
        event.num = len(items)
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, key=event_id, url=url, is_new=is_new, is_updated=not is_new)

        for item in items: self.crawl_list_product(event_id, item, ctx)
        debug_info.send(sender=DB + '.crawl_list.end')


    def crawl_list_product(self, event_id, item, ctx):
        """.. :py:method::
            In listing page, Get all product's image, url, title, price, soldout

        :param event_id: unique key in Event, which we can associate product with event
        :param item: item of xml node
        """
        product_id = item.get('data-product-id')
        product, is_new = Product.objects.get_or_create(pk=product_id)
        if is_new:
            product.event_id = [event_id]
            product.title = item.cssselect('h3 > a[data-linkname]')[0].text
            product.sell_rank = int(item.get('data-sortorder'))
            img = item.cssselect('a > img.productImage')[0].get('src')
            image = self.extract_large_img.match(img).group(1) + '$mp_hero_standard$'
            product.image_urls = [image]

            listprice = item.cssselect('ul > li.msrp').replace(',','').replace('Retail', '')
            price = item.cssselect('ul > li:nth-of-type(2)').replace(',','')
        else:
            if event_id not in product.event_id:
                product.event_id.append(event_id)

        if item.cssselect('a.sold-out'): product.soldout = True
        product.updated = False
        product.list_update_time = datetime.utcnow()
        product.save()
        common_saved.send(sender=ctx, key=product_id, url=self.siteurl + '/sales/' + event_id, is_new=is_new, is_updated=not is_new)
        debug_info.send(sender=DB + ".crawl_listing", url=self.siteurl + '/sales/' + event_id)


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
