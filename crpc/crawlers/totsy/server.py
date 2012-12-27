#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
from datetime import datetime, timedelta

from crawlers.common.stash import *
from crawlers.common.events import common_saved, common_failed
from models import *

req = requests.Session(prefetch=True, timeout=30, config=config, headers=headers)

class totsyLogin(object):
    """.. :py:class:: totsyLogin
        login, check whether login, fetch page.
    """
    def __init__(self):
        """.. :py:method::
            variables need to be used
        """
        self.login_url = 'https://www.totsy.com/customer/account/login/'
        self.data = { 
            'login[username]': login_email,
            'login[password]': login_passwd,
        }    

        self._signin = False
        self.extract_product_id = re.compile('http://www.totsy.com/sales/.+/(.+).html')

    def login_account(self):
        """.. :py:method::
            use post method to login
        """
        req.get(self.login_url)
        req.post('https://www.totsy.com/customer/account/loginPost/', data=self.data)
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
        try:
            ret = req.get(url)
        except requests.exceptions.Timeout:
            ret = req.get(url)

        if 'https://www.totsy.com/customer/account/login' in ret.url:
            self.login_account()
            ret = req.get(url)
        if ret.ok: return ret.content

        return ret.status_code

    def fetch_listing_page(self, url):
        """.. :py:method::
            fetch listing page.
            check whether the page is redirect to product(event is product)
        """
        ret = req.get(url)

        if 'https://www.totsy.com/customer/account/login' in ret.url:
            self.login_account()
            ret = req.get(url)

        if ret.ok:
            m = self.extract_product_id.match(ret.url)
            if m: # event is product
                key = m.group(1)
                return key, ret.url, ret.content
            else:
                return ret.content

        return ret.status_code


class Server(object):
    def __init__(self):
        self.eventurl = 'http://www.totsy.com/event'
        self.net = totsyLogin()
        self.extract_event_id = re.compile('http://www.totsy.com/sales/(.+).html')
        self.extract_events_end = re.compile("getTimerHtml\(.+('|\")(.+)('|\")\);")
        self.extract_product_id = re.compile('http://www.totsy.com/sales/.+/(.+).html')


    def crawl_category(self, ctx=''):
        """.. :py:method::
        """
        content = self.net.fetch_page(self.eventurl)
        if content is None or isinstance(content, int):
            common_failed.send(sender=ctx, key='', url=url,
                    reason='download event page failed: {0}'.format(content))
        tree = lxml.html.fromstring(content)
        nodes = tree.cssselect('div#stickywrap section#events-live ul.thumbnails > li.catalog-event')
        for node in nodes:
            self.parse_event_node(node, ctx)

        upcoming_nodes = tree.cssselect('div#stickywrap section#events-upcoming > ul.thumbnails > li.catalog-event')
        for node in upcoming_nodes:
            self.parse_upcoming_node(node, ctx)

    def parse_event_node(self, node, ctx):
        """.. :py:method::
            parse every event node
        """
        link = node.cssselect('a.thumbnail')[0].get('href')
        event_id = self.extract_event_id.match(link).group(1)
        sale_title = node.cssselect('a.thumbnail > hgroup')[0].text_content().strip()
        nav = node.cssselect('a.thumbnail > div.more > div.more-content > section.container > h6')
        dept, ages = [], []
        for n in nav:
            if n.text_content() == 'Categories:':
                for d in n.getnext().text_content().split('\n'):
                    if d.strip(): dept.append(d.strip())
            elif n.text_content() == 'Ages:': 
                for d in n.getnext().text_content().split('\n'):
                    if d.strip(): ages.append(d.strip())
        text = node.cssselect('a.thumbnail > script')[0].text_content()
        ends = self.extract_events_end.search(text).group(2) # 'December 23, 2012, 8:00:00' the timezone when you regist
        utc_events_end = datetime.strptime(ends, '%B %d, %Y, %X') - timedelta(hours=8) # -8 hours, set beijing to utc

        event, is_new, is_updated = self.get_or_create_event(event_id, link, sale_title)
        [event.dept.append(d) for d in dept if d not in event.dept]
        [event.ages.append(d) for d in ages if d not in event.ages]
        event.events_end = utc_events_end
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=link, is_new=is_new, is_updated=is_updated)

    def parse_upcoming_node(self, node, ctx):
        """.. :py:method::
            parse every upcoming event node
        """
        link = node.cssselect('span.echoShare')[0].get('data-producturl')
        event_id = self.extract_event_id.match(link).group(1)
        sale_title = node.cssselect('span.echoShare')[0].get('data-productname')
        text = node.cssselect('div.thumbnail > script')[0].text_content()
        begin = self.extract_events_end.search(text).group(2) # 'December 23, 2012, 8:00:00' the timezone when you regist
        utc_events_begin = datetime.strptime(begin, '%B %d, %Y, %X') - timedelta(hours=8) # -8 hours, set beijing to utc

        event, is_new, is_updated = self.get_or_create_event(event_id, link, sale_title)
        if is_new:
            content = self.net.fetch_page(link)
            tree = lxml.html.fromstring(content)
            nav = tree.cssselect('div#mainContent > section.event-landing > div.intro')[0]
            img = nav.cssselect('div > div.category-image > img')[0].get('src')
            sale_description = nav.cssselect('div.intro-content > p')[0].text_content()
            event.image_urls = [img]
            event.sale_description = sale_description
        event.events_begin = utc_events_begin
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=link, is_new=is_new, is_updated=is_updated)

    def get_or_create_event(self, event_id, link, sale_title):
        """.. :py:method::
        :param event_id:
        :param link: event listing url
        :param sale_title: event title 
        """
        is_new, is_updated = False, False
        event = Event.objects(event_id=event_id).first()
        if not event:
            is_new = True
            event = Event(event_id=event_id)
            event.urgent = True
            event.combine_url = link
            event.sale_title = sale_title
        return event, is_new, is_updated


    def crawl_listing(self, url, ctx=''):
        """.. :py:method::
        """
        event_id = self.extract_event_id.match(url).group(1)
        ret = self.net.fetch_listing_page(url)
        if isinstance(ret, tuple):
            self.crawl_event_is_product(event_id, ret[0], ret[1], ret[2], ctx)
            return
        elif ret is None or isinstance(ret, int):
            common_failed.send(sender=ctx, key=event_id, url=url,
                    reason='download event listing page failed: {0}'.format(ret))
            return
        else:
            pass

        tree = lxml.html.fromstring(ret)
        nodes = tree.cssselect('div#mainContent > section.event-landing > div.row > div.event-products > ul.event_prod_grid > li')
        for node in nodes:
            image = node.cssselect('div.thumbnail > a.product-image')[0]
            title = image.get('title')
            link = image.get('href')
            key = self.extract_product_id.match(link).group(1)
            pprice = node.cssselect('div.thumbnail > div.caption > div.price-wrap > div.price-box')[0]
            listprice = pprice.cssselect('p.old-price > span.price')[0].text_content().strip()
            price = pprice.cssselect('span.special-price')[0].text_content().strip()
            soldout = True if node.cssselect('img.out-of-stock') else False

            is_new, is_updated = False, False
            product = Product.objects(key=key).first()
            if not product:
                is_new = True
                product = Product(key=key)
                product.combine_url = link
                product.updated = False
                product.title = title
                product.listprice = listprice
                product.price = price
                product.soldout = soldout
            else:
                if soldout and product.soldout != True:
                    product.soldout = True
                    is_updated = True
            if event_id not in product.event_id: product.event_id.append(event_id)
            product.list_update_time = datetime.utcnow()
            product.save()
            common_saved.send(sender=ctx, obj_type='Product', key=key, url=link, is_new=is_new, is_updated=is_updated)

        event = Event.objects(event_id=event_id).first()
        if not event: event = Event(event_id=event_id)
        ready = None
        if not event.image_urls:
            nav = tree.cssselect('div#mainContent > section.event-landing > div.intro')[0]
            event.image_urls = [ nav.cssselect('div > div.category-image > img')[0].get('src') ]
            event.sale_description = nav.cssselect('div.intro-content > p')[0].text_content()
            ready = False
        if event.urgent == True:
            event.urgent = False
            ready = True
        if ready is not None:
            event.update_time = datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event_id, is_new=False, is_updated=False, ready=ready)


    def crawl_event_is_product(self, event_id, key, url, content, ctx):
        """.. :py:method::
        """
        tree = lxml.html.fromstring(content)

        is_new, is_updated, product = self.save_product_detail(key, *self.parse_product(tree))
        nav = tree.cssselect('div#mainContent > section#pageheader > div.row')[0]
        soldout_price = nav.cssselect('div.product-main > div.product-addtocart div#product-main-info')[0]
        soldout = True if soldout_price.cssselect('div.availability') else False
        if is_new:
            product.title = nav.cssselect('div.product-main > div.page-header > h3')[0].text_content()
            product.price = soldout_price.cssselect('div.product-prices > div.product-prices-main > div.price-box > span.special-price')[0].text_content()
            product.listprice = soldout_price.cssselect('div.product-prices > div.product-prices-main > div.product-price-was')[0].text_content().replace('Was', '').strip()
            product.combine_url = url
            product.soldout = soldout
            product.updated = True
            ready = True
        else:
            if soldout and product.soldout != True:
                product.soldout = True
                is_updated = True
            ready = False
        if event_id not in product.event_id: product.event_id.append(event_id)
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=key, url=url, is_new=is_new, is_updated=is_updated, ready=ready)


    def crawl_product(self, url, ctx=''):
        """.. :py:method::
        """
        key = self.extract_product_id.match(url).group(1)
        content = self.net.fetch_page(url)
        if isinstance(content, int):
            common_failed.send(sender=ctx, key=key, url=url,
                    reason='download product page failed: {0}'.format(content))
            return
        if content is None: content = self.net.fetch_page(url)
        tree = lxml.html.fromstring(content)
        is_new, is_updated, product = self.save_product_detail(key, *self.parse_product(tree))

        if product.updated == False:
            product.updated = True
            ready = True
        else: ready = False
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=key, url=url, is_new=is_new, is_updated=is_updated, ready=ready)

    def parse_product(self, tree):
        """.. :py:method::
            parse product detail page
        """
        nav = tree.cssselect('div#mainContent > section#pageheader > div.row')[0]
        image_urls = []
        imgs = nav.cssselect('div.product-media > div.more-views > ul.thumbnails > li > div.thumbnail')
        for img in imgs:
            image_urls.append( img.cssselect('a')[0].get('href') )
        cont = nav.cssselect('div.product-main > div > div.product-content')[0]
        summary = cont.cssselect('div.product_desc')[0].text.strip()
        list_info = []
        for s in cont.xpath('div[@class="product_desc"]/text()'):
            if s.strip(): list_info.append( s.strip() )
        summary = '; '.join(list_info)
        list_info = []
        for li in cont.cssselect('div.product_desc > ul > li'):
            list_info.append(li.text_content().strip())

        ship = cont.cssselect('div#shipping-returns')
        if not ship: ship = cont.cssselect('div#shipping')
        shipping = ship[0].cssselect('p:first-of-type')[0].text_content()
        returned = ship[0].cssselect('p:nth-of-type(2)')[0].text_content()
        return image_urls, summary, list_info, shipping, returned

    def save_product_detail(self, key, image_urls, summary, list_info, shipping, returned):
        """.. :py:method::
            get a product from mongodb, save some fields
        """
        is_new, is_updated = False, False
        product = Product.objects(key=key).first()
        if not product:
            is_new = True
            product = Product(key=key)
        [product.image_urls.append(img) for img in image_urls if img not in product.image_urls]
        product.summary = summary
        product.list_info = list_info
        product.shipping = shipping
        product.returned = returned
        product.full_update_time = datetime.utcnow()
        return is_new, is_updated, product


if __name__ == '__main__':
    Server().crawl_listing('http://www.totsy.com/sales/fashion-boots-under-30.html')
    Server().crawl_listing('http://www.totsy.com/sales/healthy-surprise-1.html')
    Server().crawl_listing('http://www.totsy.com/sales/whitening-lightning-dec.html')
