#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
# 30312 It's time for high fashion Mon. Dec 03
# 30079 Playboy Wed. Dec 26
# 30791 Dress Your Home Mon. Dec 03
"""
crawlers.beyondtherack.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""

import lxml.html
from datetime import datetime

from models import *
from crawlers.common.stash import *
from crawlers.common.events import common_saved

headers = {
    'Host': 'www.beyondtherack.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0',
}

req = requests.Session(prefetch=True, timeout=30, config=config, headers=headers)

class beyondtherackLogin(object):
    """.. :py:class:: beyondtherackLogin
        login, check whether login, fetch page.
    """
    def __init__(self):
        """.. :py:method::
            variables need to be used
        """
        self.login_url = 'https://www.beyondtherack.com/auth/login'
        self.data = {
            'email': login_email,
            'passwd': login_passwd,
            'keepalive': 1,
            '_submit': 1,
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

        if 'https://www.beyondtherack.com/auth/' in ret.url: #login or register
            self.login_account()
            ret = req.get(url)
        if ret.ok: return ret.content

        return ret.status_code

    def fetch_listing_page(self, url):
        """.. :py:method::
        """
        ret = req.get(url)

        if 'https://www.beyondtherack.com/auth/' in ret.url: #login or register
            self.login_account()
            ret = req.get(url)
        if ret.ok and 'sku' in ret.url:
            return [ret.url, ret.content] 
        else:
            return ret.content

        return ret.status_code


class Server(object):
    """.. :py:class:: Server

        This is zeroRPC server class for ec2 instance to crawl pages.

    """
    def __init__(self):
        self.siteurl = 'http://www.beyondtherack.com'
        self.all_event_url = 'http://www.beyondtherack.com/event/calendar'
        self.net = beyondtherackLogin()
        self.dept_link = {
            'women':        'http://www.beyondtherack.com/event/calendar?category=1',
            'men':          'http://www.beyondtherack.com/event/calendar?category=2',
            'kids':         'http://www.beyondtherack.com/event/calendar?category=3',
            'home':         'http://www.beyondtherack.com/event/calendar?category=4',
            'curvy_closet': 'http://www.beyondtherack.com/event/calendar?category=10',
        }

        self.extract_event_id = re.compile('.*/event/showcase/(\d+)\??.*')
        self.extract_image_url = re.compile('background-image: url\(\'(.*)\'\);')


    def crawl_category(self, ctx=''):
        self.crawl_category_text_info(self.all_event_url, ctx)

        for dept, url in self.dept_link.iteritems():
            self.crawl_one_dept_image(dept, url, ctx)


    def crawl_category_text_info(self, url, ctx):
        """.. :py:method::
            Get all the events' text info from main url

        :param url: the main url of this site
        """
        content = self.net.fetch_page(url)
        if content is None or isinstance(content, int):
            common_failed.send(sender=ctx, key='', url=url,
                    reason='download error or {1} return'.format(content))
            return
        tree = lxml.html.fromstring(content)
        for dept in self.dept_link.keys():
            self.crawl_one_dept_text_info(dept, tree, ctx)


    def crawl_one_dept_text_info(self, dept, tree, ctx):
        """.. :py:method::

        :param dept: dept of this site
        :param tree: the xpath tree of main page
        """
        items = tree.cssselect('div.headerframe ul#nav > li.menu_item_{0} > div.submenu > table td > div.submenu-section > a'.format(dept))
        for item in items:
            link = item.get('href')
            event_id = self.extract_event_id.match(link).group(1)
            ending_soon = item.cssselect('div.menu-item-ending-soon')
            if ending_soon:
                sale_title = ending_soon[0].cssselect('div.link')[0].text_content()
            else:
                sale_title = item.cssselect('div.menu-item')[0].text_content()

            is_new, is_updated = False, False
            event = Event.objects(event_id=event_id).first()
            if not event:
                is_new = True
                event = Event(event_id=event_id)
                event.urgent = True
                event.combine_url = 'http://www.beyondtherack.com/event/showcase/{0}'.format(event_id)
            if dept not in event.dept: event.dept.append(dept)
            if not event.sale_title: event.sale_title = sale_title
            event.update_time = datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)


    def crawl_one_dept_image(self, dept, url, ctx):
        content = self.net.fetch_page(url)
        if content is None or isinstance(content, int):
            common_failed.send(sender=ctx, key=dept, url=url,
                    reason='download error \'{0}\' or {1} return'.format(dept, content))
            return
        tree = lxml.html.fromstring(content)
        items = tree.cssselect('div.pageframe > div.mainframe > a[href]')
        for item in items:
            link = item.get('href')
            if 'facebook' in link: continue
            event_id = self.extract_event_id.match(link).group(1)
            image_text = item.cssselect('span[style]')[0].get('style')
            image_url = self.extract_image_url.search(image_text).group(1)
        
            is_new, is_updated = False, False
            event = Event.objects(event_id=event_id).first()
            if not event:
                is_new = True
                event = Event(event_id=event_id)
                event.urgent = True
                event.combine_url = 'http://www.beyondtherack.com/event/showcase/{0}'.format(event_id)

            if dept not in event.dept: event.dept.append(dept)
            if image_url not in event.image_urls: event.image_urls.append(image_url)
            event.update_time = datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)


    def crawl_listing(self, url, ctx=''):
        event_id = url.rsplit('/', 1)[-1]
        content = self.net.fetch_listing_page(url)
        if isinstance(content, list):
            self.crawl_event_is_product(event_id, content[0], content[1])
            return
            
        if content is None or isinstance(content, int):
            common_failed.send(sender=ctx, key='', url=url,
                    reason='download listing error or {0} return'.format(content))
            return
        tree = lxml.html.fromstring(content)
        segment = tree.cssselect('div.pageframe > div#main-form')[0]
        events_end = segment.cssselect('div.clearfix div#eventTTL')
        events_end = datetime.utcfromtimestamp( float(events_end[0].get('eventttl')) )
        # both button and nth-last-of-type condition
        page_nums = segment.cssselect('div.clearfix form[method=get] > div.pagination > div.button:nth-last-of-type(1)')
        if page_nums:
            page_nums = int( page_nums[0].text_content() )
        
        prds = segment.cssselect('form[method=post] > div#product-list > div.product-row > div.product > div.section')
        for prd in prds: self.crawl_every_product_in_listing(event_id, url, prd, ctx)

        if isinstance(page_nums, int):
            for page_num in range(2, page_nums+1):
                page_url = '{0}?page={1}'.format(url, page_num)
                self.get_next_page_in_listing(event_id, page_url, page_num, ctx)

        event = Event.objects(event_id=event_id).first()
        if not event: event = Event(event_id=event_id)
        if event.urgent == True:
            event.urgent = False
            event.update_time = datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event_id, is_new=False, is_updated=False, ready=True)


    def crawl_every_product_in_listing(self, event_id, url, prd, ctx):
        soldout = True if prd.cssselect('div.section-img > div.showcase-overlay > a > div') else False
        link = prd.cssselect('div.section-img > a[href]')
        if link:
            link = link[0].get('href')
        else: # blank place in the last few products' place
            return
        key = re.compile('.*/event/sku/{0}/(\w+)\??.*'.format(event_id)).match(link).group(1)

        brand = prd.cssselect('div.clearfix > div[style]:first-of-type')[0].text_content()
        title = prd.cssselect('div.clearfix > div[style]:nth-of-type(2)')[0].text_content()
        listprice = prd.cssselect('div.clearfix > div[style] > div.product-price-prev')[0].text_content()
        price = prd.cssselect('div.clearfix > div[style] > div.product-price')[0].text_content()
        size_nodes = prd.cssselect('div.clearfix > div[style]:nth-of-type(4) > div[style] > select.size-selector > option')
        sizes = []
        for size in size_nodes:
            sizes.append( size.text_content().strip() )

        is_new, is_updated = False, False
        product = Product.objects(key=key).first()
        if not product:
            is_new = True
            product = Product(key=key)
            product.updated = False
            product.combine_url = 'http://www.beyondtherack.com/event/sku/{0}/{1}'.format(event_id, key)
            product.soldout = soldout
            product.brand = brand
            product.title = title
            product.listprice = listprice
            product.price = price
            product.sizes = sizes
        else:
            if soldout and product.soldout != soldout:
                product.soldout = True
                is_updated = True
        if event_id not in product.event_id: product.event_id.append(event_id)
        product.list_update_time = datetime.utcnow()
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=key, url=link, is_new=is_new, is_updated=is_updated)


    def get_next_page_in_listing(self, event_id, page_url, page_num, ctx):
        content = self.net.fetch_listing_page(page_url)
        if content is None or isinstance(content, int):
            common_failed.send(sender=ctx, key='', url=page_url,
                    reason='download listing error or {0} return'.format(content))
            return
        tree = lxml.html.fromstring(content)
        segment = tree.cssselect('div.pageframe > div#main-form')[0]
        prds = segment.cssselect('form[method=post] > div#product-list > div.product-row > div.product > div.section')
        for prd in prds: self.crawl_every_product_in_listing(event_id, page_url, prd, ctx)


    def crawl_event_is_product(self, event_id, product_url, content):
        """.. :py:method::

            event listing page url redirect to product page
        :param event_id: event id
        :param product_url: redirect to the product_url
        :param content: product_url's content
        """
        key = re.compile('http://www.beyondtherack.com/event/sku/\w+/(\w+)\??.*').match(product_url).group(1)
        tree = lxml.html.fromstring(content)
        list_info, summary, shipping, returned, image_urls = self.parse_product_info(tree)


    def crawl_product(self, url, ctx=''):
        key = url.rsplit('/', 1)[-1]
        content = self.net.fetch_page(url)
        if content is None or isinstance(content, int):
            common_failed.send(sender=ctx, key='', url=page_url,
                    reason='download product error or {0} return'.format(content))
            return
        tree = lxml.html.fromstring(content)
        list_info, summary, shipping, returned, image_urls = self.parse_product_info(tree)

        is_new, is_updated = False, False
        product = Product.objects(key=key).first()
        if not product:
            is_new = True
            product = Product(key=key)
        product.summary = summary
        product.list_info = list_info
        product.shipping = shipping
        product.returned = returned
        product.image_urls = image_urls
        product.full_update_time = datetime.utcnow()
        if product.updated == False:
            product.updated = True
            ready = True
        else: ready = False
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=casin, url=url, is_new=is_new, is_updated=is_updated, ready=ready)
            
    def parse_product_info(self, tree):
        """.. :py:method::

        :param tree: element tree of product page
        """
        nav = tree.cssselect('div.pageframe > div.mainframe > div.clearfix')[0]
        list_info = []
        for li in nav.cssselect('div > div > ul[style] > li'):
            list_info.append( li.text_content().strip() )
        summary, list_info = '; '.join(list_info), []
        for li in nav.cssselect('div > ul[style] > li'):
            list_info.append( li.text_content().strip() )
        shipping = nav.xpath('./div[@style="text-align: left;"]/div/a[@id="ship_map"]/parent::div[style]//text()') 
        returned = nav.xpath('./div[@style="text-align: left;"]//text()') 
        for img in nav.cssselect('div[style] > div > a.cloud-zoom-gallery > img'):
            image_urls.append( img.get('src').replace('small', 'large') )
        return list_info, summary, shipping, returned, image_urls


if __name__ == '__main__':
    import zerorpc
    from settings import CRAWLER_PORT
    server = zerorpc.Server(Server())
    server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
    server.run()
