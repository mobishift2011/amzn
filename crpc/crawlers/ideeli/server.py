#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

"""
crawlers.ideeli.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.
"""
import urllib
import json
import lxml.html

from models import *
from crawlers.common.events import common_saved, common_failed
from crawlers.common.stash import *

headers = { 
    'Host': 'www.ideeli.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0',
}

req = requests.Session(prefetch=True, timeout=30, config=config, headers=headers)

class ideeliLogin(object):
    """.. :py:class:: beyondtherackLogin
        login, check whether login, fetch page.
    """
    def __init__(self):
        """.. :py:method::
            variables need to be used
        """
        self.login_url = 'https://www.ideeli.com/login'
        self.data = { 
            'login': login_email,
            'password': login_passwd,
            'x': 64,
            'y': 20,
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

        if 'https://www.ideeli.com/login' in ret.url: #login
            self.login_account()
            ret = req.get(url)
        if ret.ok: return ret.content

        return ret.status_code


class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.ideeli.com'
        self.homepage = 'http://www.ideeli.com/events/latest/' # urllib.basejoin need '/' in the end of the string
        self.event_img_prefix = 'http://lp-img-production.ideeli.com/'
        self.net = ideeliLogin()
        self.extract_event_id = re.compile('.*/events/(\w+)/latest_view')

    def crawl_category(self, ctx=''):
        depts = ['women', 'men', 'home', 'holiday',]
        for dept in depts:
            self.crawl_one_dept(dept, ctx)

    def crawl_one_dept(self, dept, ctx):
        """.. :py:method::

        :param dept: department
        """
        url = urllib.basejoin(self.homepage, dept)
        content = self.net.fetch_page( url )
        if content is None or isinstance(content, int):
            common_failed.send(sender=ctx, key=dept, url=url,
                    reason='download this department failed: {0}'.format(content))
        tree = lxml.html.fromstring(content)
        nav = 'div#container > div#content > div#on_sale_today > div#{0}_channel'.format(dept)
        nav = tree.cssselect(nav)[0]

        nodes = nav.cssselect('div > div#on_sale_left_col > div#on_sale_today_channel > div#latest_events_container > div.event_unit > a[href]')
        for node in nodes: self.parse_one_event_node(dept, node, ctx)

        # only 'women' have events on ending_soon_tabs
        nodes = nav.cssselect('div#ending_soon_tabs ul#ending_soon_carousel_women > li > div.event_unit > a[href]')
        for node in nodes: self.parse_one_event_node(dept, node, ctx)


    def parse_one_event_node(self, dept, node, ctx):
        """.. :py:method::

        :param dept: department
        :param node: xpath node
        """
        link = node.get('href')
        m = self.extract_event_id.match(link)
        if not m: return # here need to be careful when webpage change their scheme
        event_id = m.group(1)
        link = link if link.startswith('http') else self.siteurl + link
        img = node.cssselect('img[data-src]')[0].get('data-src')
        img = img if img.startswith('http') else urllib.basejoin(self.event_img_prefix, img)
        brand = node.cssselect('div > span.event_grid_cta > b:first-of-type')[0].text_content()
        title = node.cssselect('div > span.event_grid_cta > span.title')[0].text_content().strip()
        sale_title = brand + title if title else brand
        begin = node.cssselect('div > span.event_grid_cta > span.starts_in > span.starting_in_timer')[0].text_content()
        end = node.cssselect('div > span.event_grid_cta > span.ends_in > span.ending_soon_timer')[0].text_content()
        events_begin = datetime.utcfromtimestamp( float(begin) )
        events_end = datetime.utcfromtimestamp( float(end) )

        is_new, is_updated = False, False
        event = Event.objects(event_id=event_id).first()
        if not event:
            is_new = True
            event = Event(event_id=event_id)
            event.urgent = True
            event.combine_url = link
            event.sale_title = sale_title
        if dept not in event.dept: event.dept.append(dept)
        if img not in event.image_urls: event.image_urls.append(img)
        event.events_begin = events_begin
        event.events_end = events_end
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=link, is_new=is_new, is_updated=is_updated)

    def crawl_listing(self, url, ctx=''):
        event_id = self.extract_event_id.match(url).group(1)
        content = self.net.fetch_page( url )
        if content is None or isinstance(content, int):
            common_failed.send(sender=ctx, key='', url=url,
                    reason='download listing page failed: {0}'.format(content))
        data = json.loads(content)['colors']
        for d in data:
            key = str(d[0])
            soldout = not d[1]['available']
            brand = d[1]['product_brand_name']
            title = d[1]['strapline']
            color = d[1]['color_name']
            listprice = d[1]['offer_retail_price']
            price = str(d[1]['numeric_offer_price'])
            price = price[:-2] + '.' + price[-2:]
            returned = d[1]['offer_return_policy']
            shipping = d[1]['offer_shipping_window']
            sizes = d[1]['pretty_sizes']
            link = d[1]['offer_url']
            link = link if link.startswith('http') else self.siteurl + link
            offer_id = d[1]['offer_id']

            is_new, is_updated = False, False
            product = Product.objects(key=key).first()
            if not product:
                is_new = True
                product = Product(key=key)
                product.updated = False
                product.combine_url = link
                product.soldout = soldout
                product.brand = brand
                product.title = title
                product.color = color
                product.listprice = listprice
                product.price = price
                product.returned = returned
                product.shipping = shipping
                product.sizes = sizes
                product.offer_id = offer_id
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
        if event.urgent == True:
            event.urgent = False
            event.update_time = datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event_id, is_new=False, is_updated=False, ready=True)

        


if __name__ == '__main__':
    import zerorpc
    from settings import CRAWLER_PORT
    server = zerorpc.Server(Server())
    server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
    server.run()
