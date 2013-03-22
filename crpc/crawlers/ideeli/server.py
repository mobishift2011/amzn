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

header = { 
    'Accept': 'text/html, application/xhtml+xml, application/xml, text/javascript, text/xml, */*',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate',
    'Host': 'www.ideeli.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Ubuntu Chromium/25.0.1364.160 Chrome/25.0.1364.160 Safari/537.22',
}

req = requests.Session(prefetch=True, timeout=25, config=config, headers=header)

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
            'login': login_email[DB],
            'password': login_passwd,
            'x': 64,
            'y': 20,
        }   

        self.current_email = login_email[DB]
        self._signin = {}

    def login_account(self):
        """.. :py:method::
            use post method to login
        """
        self.data['login'] = self.current_email
        req.post(self.login_url, data=self.data)
        self._signin[self.current_email] = True

    def check_signin(self, username=''):
        """.. :py:method::
            check whether the account is login
        """
        if username == '':
            self.login_account()
        elif username not in self._signin:
            self.current_email = username
            self.login_account()
        else:
            self.current_email = username

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

    def fetch_product_page(self, url):
        """.. :py:method::
            fetch product page.
            check whether the account is login, if not, login and fetch again
        """
        ret = req.get(url)

        if 'https://www.ideeli.com/login' in ret.url: #login
            self.login_account()
            ret = req.get(url)
        if 'https://www.ideeli.com/login' in ret.url: #login
            self.login_account()
            ret = req.get(url)
        if ret.url == u'http://www.ideeli.com/events/latest':
            ret = req.get(url)
            if ret.url == u'http://www.ideeli.com/events/latest':
                return -302
        if ret.ok:
            return ret.url, ret.content

        return ret.status_code


class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.ideeli.com'
        self.homepage = 'http://www.ideeli.com/events/latest/' # urllib.basejoin need '/' in the end of the string
        self.event_img_prefix = 'http://lp-img-production.ideeli.com/'
        self.net = ideeliLogin()
        self.extract_event_id = re.compile('.*/events/(\w+)/latest_view')
        self.extract_product_id = re.compile('http://www.ideeli.com/events/\w+/offers/\w+/latest_view/(\w+)')

    def crawl_category(self, ctx='', **kwargs):
        if kwargs.get('login_email'): self.net.check_signin( kwargs.get('login_email') )
        else: self.net.check_signin()

        depts = ['women', 'shoes', 'home', ]
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
            return
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
        sale_title = brand + ' ' + title if title else brand
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
        if event.events_begin != events_begin:
            event.update_history.update({ 'events_begin': datetime.utcnow() })
            event.events_begin = events_begin
        if event.events_end != events_end:
            event.update_history.update({ 'events_end': datetime.utcnow() })
            event.events_end = events_end
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=link, is_new=is_new, is_updated=is_updated)

    def crawl_listing(self, url, ctx='', **kwargs):
        if kwargs.get('login_email'): self.net.check_signin( kwargs.get('login_email') )
        else: self.net.check_signin()

        event_id = self.extract_event_id.match(url).group(1)
        content = self.net.fetch_page( url )
        try:
            data = json.loads(content)['colors']
        except ValueError:
            content = self.net.fetch_page( url )
            if content is None or isinstance(content, int):
                common_failed.send(sender=ctx, key=event_id, url=url,
                        reason='download listing page failed: {0}'.format(content))
                return
            data = json.loads(content)['colors']
            
        product_ids = []
        for d in data:
            key = str(d[0])
            soldout = not d[1]['available']
            brand = d[1]['product_brand_name']
            title = d[1]['strapline']
            color = d[1]['color_name']
            listprice = d[1]['offer_retail_price'].replace('$', '').replace(',', '').strip()
            price = str(d[1]['numeric_offer_price'])
            price = (price[:-2] + '.' + price[-2:]).replace('$', '').replace(',', '').strip()
            returned = lxml.html.fromstring(d[1]['offer_return_policy']).text_content()
            shipping = d[1]['offer_shipping_window'].replace('<br />', ' ')
            sizes = d[1]['pretty_sizes']
            link = d[1]['offer_url']
            link = link if link.startswith('http') else self.siteurl + link
            # product_path = d[1]['product_path'] # /products/2044450?color_id=2975222&sku_id=10722246
            categories = d[1]['categories']
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
                product.cats = categories
                product.offer_id = offer_id
            else:
                if product.soldout != soldout:
                    product.soldout = soldout
                    product.update_history.update({ 'soldout': datetime.utcnow() })
                    is_updated = True
                if product.listprice != listprice:
                    product.listprice = listprice
                    product.update_history.update({ 'listprice': datetime.utcnow() })
                if product.price != price:
                    product.price = price
                    product.update_history.update({ 'price': datetime.utcnow() })

            if event_id not in product.event_id: product.event_id.append(event_id)
            product.list_update_time = datetime.utcnow()
            product.save()
            common_saved.send(sender=ctx, obj_type='Product', key=key, url=link, is_new=is_new, is_updated=is_updated)
            product_ids.append(key)

        event = Event.objects(event_id=event_id).first()
        if not event: event = Event(event_id=event_id)
        if event.urgent == True:
            event.urgent = False
            ready = True
        else:    ready = False
        event.product_ids = product_ids
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event_id, is_new=False, is_updated=False, ready=ready)

        
    def crawl_product(self, url, ctx='', **kwargs):
        if kwargs.get('login_email'): self.net.check_signin( kwargs.get('login_email') )
        else: self.net.check_signin()

        key = self.extract_product_id.match(url).group(1)
        ret = self.net.fetch_product_page( url )
        if ret == -302:
            common_failed.send(sender=ctx, key='', url=url, reason='product page redirect home: {0}'.format(ret))
            return

        if ret is None or isinstance(ret, int):
            ret = self.net.fetch_product_page( url )
            if ret is None or isinstance(ret, int):
                common_failed.send(sender=ctx, key='', url=url,
                        reason='download product page failed: {0}'.format(ret))
                return
        tree = lxml.html.fromstring(ret[1])
        nav = tree.cssselect('div#container > div#content > div#latest_container > div#latest > div.event > div.offer_container')[0]
        info = nav.cssselect('div#offer_sizes_colors > div.details_tabs_content > div.spec_on_sku')[0]
        list_info = []
        for li in info.cssselect('ul > li'):
            list_info.append( li.text_content().strip() )
        summary, list_info = '; '.join(list_info), [] # some products have mixed all list_info into summary
        list_info_revise = info.cssselect('p') # maybe one p label or 2, type list
        if list_info_revise:
            for i in list_info_revise:
                list_info.extend( i.xpath('.//text()') )
        list_info = [i.strip() for i in list_info if i.strip()] # get rid of ' ' and \n
        list_info_revise = []
        idx = 0
        while idx < len(list_info):
            if idx+1 != len(list_info) and (list_info[idx].strip()[-1] == ':' or list_info[idx+1].strip()[0] == ':'):
                if list_info[idx+1].strip()[-1] == ':':
                    idx += 1
                else:
                    list_info_revise.append( ''.join((list_info[idx], list_info[idx+1])) )
                    idx += 2
            else:
                list_info_revise.append(list_info[idx])
                idx += 1
        images = nav.cssselect('div#offer_photo_and_desc > div#images_container_{0} > div.image_container > a.MagicZoom'.format(key))
        image_urls = []
        for image in images:
            image_urls.append( image.get('href') )

        is_new, is_updated = False, False
        product = Product.objects(key=key).first()
        if not product:
            is_new = True
            product = Product(key=key)
        product.summary = summary
        product.list_info = list_info_revise
        [product.image_urls.append(img) for img in image_urls if img not in product.image_urls]
        product.full_update_time = datetime.utcnow()
        if product.updated == False:
            product.updated = True
            ready = True
        else: ready = False
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=key, url=url, is_new=is_new, is_updated=is_updated, ready=ready)


if __name__ == '__main__':
    import zerorpc
    from settings import CRAWLER_PORT
    server = zerorpc.Server(Server())
    server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
    server.run()
