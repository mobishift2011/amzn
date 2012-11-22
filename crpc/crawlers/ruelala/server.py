#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SimplyToImpress.com 11/21 at 8AM ET http://www.ruelala.com/event/promoReel/id/61083
Oakley Ski Gear     11/21 at 11AM ET http://www.ruelala.com/event/promoReel/id/59788

crawlers.ruelala.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""
from gevent import monkey
monkey.patch_all()
import os

from models import *
from crawlers.common.stash import *
from crawlers.common.events import common_saved, common_failed, debug_info, warning_info
from datetime import datetime, timedelta
import lxml.html
import urllib
import re

headers = { 
    'Host': 'www.ruelala.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0',
    'Referer': 'http://www.ruelala.com/event',
    'Cookie': 'X-CCleaned=1; optimizelyEndUserId=oeu1349667187777r0.2759982226275626; optimizelyBuckets=%7B%7D; CoreID6=87382265939413496671878&ci=90210964; userEmail=huanzhu@favbuy.com; optimizelySegments=%7B%7D; symfony=r81cu3qbbjn7nc63g60i0nap34; Liberty.QuickBuy.canQuickBuy=0; 90210964_clogin=l=1353388560&v=1&e=1353390811310; cmTPSet=Y; pgts=1353390708; NSC_SVF_QPPM_BMM=ffffffff096c9d3a45525d5f4f58455e445a4a423660; Liberty.QuickBuy.eventId=59006; Liberty.QuickBuy.styleNum=3030858912; aid=1001; urk=bfb8a96cc255d42649093b974d212aaf8e65848b; urkm=fcac147b49ab4bb16bd30d2e5d1eb378e9a88acd; uid=9471446; rusersign=pM7Qg9lgkbwXKJPogkVGFZhYlxK24aB5VG2HZqFs5c7gnbMTPD8UnzYFPE2XNVPPHYWwV1ggSb%2BY%0D%0AxiGhHijdA%2BoGACCoVFx6E3gXyWE1%2BGEeaj2By3%2F037JRnKetYPhGZzCL8a94TkR0vahredOnZEvG%0D%0Ah%2F9KsgIT6lFXzqJZlfeZpIW8aBOK%2BR0eD%2FXHTODsFmDkwrERuEFnz6v5ooQrYGCJ1VVM2gUursgz%0D%0AtXYeleOLaVtU8Yy7BrMFBHnJqi3rw0NCZ8h%2B5jil1%2Fv1zzfZgolqoYseZRgySn%2BzI2%2FdmXFc%2BhL5%0D%0ApIWw6vJc32madG277NVZbAqiSOUTRBxGM4MMZw%3D%3D; ruserbase=eyJpZCI6W3siaWQiOjk0NzE0NDYsInR5cGUiOiJydWVsYWxhIn1dLCJ0cmFja2luZyI6W3sibmFt%0D%0AZSI6InJlZmVycmVySWQiLCJ2YWx1ZSI6Ik9UUTNNVFEwTmc9PSJ9LHsibmFtZSI6ImVLZXkiLCJ2%0D%0AYWx1ZSI6ImFIVmhibnBvZFVCbVlYWmlkWGt1WTI5dCJ9XX0%3D; ssids=59504; uhv=8e4314db871b3222e41a856ffe55a0a332ba2635055bf4e597fed31ef6052bf6; siteid=full; stid=aHVhbnpodUBmYXZidXkuY29tOjEzNjg5NDI3MzI6NFovUHJDMHd2RGcwb1ViWi9QUVpXZDM3Y3dRQ3Y1R0ljMkFZSG5CajFYOD0='
}

req = requests.Session(prefetch=True, timeout=30, config=config, headers=headers)

class ruelalaLogin(object):
    """.. :py:class:: ruelalaLogin
        login, check whether login, fetch page.
    """
    def __init__(self):
        """.. :py:method::
            variables need to be used
        """
        self.login_url = 'http://www.ruelala.com/access/gate'
        self.data = {
            'email': login_email,
            'password': login_passwd,
            'loginType': 'gate',
            'rememberMe': 1, 
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

        if ret.status_code == 401: # need to authentication
            self.login_account()
            ret = req.get(url)
        if ret.ok: return ret.content

        # if this event is a product, event will redirect to product page.
        # So it is the product page unauthorized, fetch_page the product url next time
        if ret.status_code == 401:
            return ret.url

    def fetch_image(self, url):
        ret = req.get(url)
        return ret.status_code


class Server(object):
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    
    def __init__(self):
        self.siteurl = 'http://www.ruelala.com'
        self.net = ruelalaLogin()
        self.countdown_num = re.compile("countdownFactory.create\(('|\")(\\d+)('|\"), ('|\")(\\d+)('|\"), ('|\")('|\")\);")
        self.url2eventid = re.compile('http://www.ruelala.com/event/(\d+)')

    def crawl_category(self, ctx=''):
        """.. :py:method::
            From top depts, get all the events
        """
        categorys = ['women', 'men', 'living', 'kids', 'gifts']
        for category in categorys:
            url = 'http://www.ruelala.com/category/{0}'.format(category)
            if category == 'gifts':
                self._get_gifts_event_list(category, url, ctx)
            else:
                self._get_event_list(category, url, ctx)


    def _get_gifts_event_list(self, dept, url, ctx):
        """.. :py:method::
            Get gifts events, these events have no time.
            
            Problem may exist: these events off sale, update_listing will get nothing.
        """
        cont = self.net.fetch_page(url)
        tree = lxml.html.fromstring(cont)
        nodes = tree.cssselect('body > div.container > div#canvasContainer > section#gift-center > div#gc-wrapper a[href]')
        for node in nodes:
            link = node.get('href')
            event_id = link.rsplit('/', 1)[-1]
            link = link if link.startswith('http') else self.siteurl + link

            event = Event.objects(event_id=event_id).first()
            is_new = False
            if not event:
                is_new = True
                event = Event(event_id=event_id)
                event.dept = [dept]
                event.combine_url = link
                event.urgent = True
            event.update_time = datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, key=event_id, is_new=is_new, is_updated=False)

    def _get_event_list(self, dept, url, ctx):
        """.. :py:method::
            Get all the events from event list.
        """
        cont = self.net.fetch_page(url)
        tree = lxml.html.fromstring(cont)
        nodes = tree.cssselect('body.wl-default > div.container > div#categoryMain > section#categoryDoors > article[id^="event-"]')
        for node in nodes:
            event, event_id, link = self.parse_event(dept, node, ctx)

            num, isodate = self.is_parent_event(dept, event_id, link, ctx)
            if num == -1 or 0: # event is product or event is special
                countdown = re.compile("countdownFactory.create\(('|\"){0}('|\"), ('|\")(\\d+)('|\"), ('|\")('|\")\);".format(event_id)).search(cont).group(4)
                event.events_end = datetime.utcfromtimestamp(float(countdown[:-3]))
                event.is_leaf = False
                event.save()
            if num >= 1:
                if num > 1: event.is_leaf = False
                event.events_end = isodate
                event.save()
            if num == 0:
                pass


    def is_parent_event(self, dept, event_id, url, ctx):
        """.. :py:method::
            check whether event is parent event
            -2 real error
            -1 event is product
            0 closing day found: common_failed signal send
            1 closing day found: this is a listing page, return UTC events_end time
            > 1 closing days found: parent event.

            [("'", '61313', "'", "'", '1353686400000', "'"),
             ("'", '61312', "'", "'", '1353686400000', "'"),
             ("'", '61311', "'", "'", '1353686400000', "'")]

            child event's listing page, the time pair is: (parent_event_id, child_events_end)
            I found parent and child event share the same events_end on the website

        :param event_id: event id
        :param url: parent event url or listing page url
        :rtype: number -- 0(fail), >=1(success)
                events_end: isoformat events_end
        """
        cont = self.net.fetch_page(url)
        if cont.startswith('http://'): # event is a product.
            self.crawl_event_is_product(event_id, cont, ctx)
            return -1, 0
        countdown_num = self.countdown_num.findall(cont)
        if len(countdown_num) == 0:
            common_failed.send(sender=ctx, site=DB, key='', url=url, reason='Url has no closing time.')
            return 0, 0

        elif len(countdown_num) == 1:
            if countdown_num[0][1] == event_id:
                return 1, datetime.utcfromtimestamp( float(countdown_num[0][4][:-3]) )
            else:
                common_failed.send(sender=ctx, site=DB, key='', url=url, reason='Url has 1 closing time but event_id not matching.')
                return -2, 0
        elif len(countdown_num) > 1:
            tree = lxml.html.fromstring(cont)
            nodes = tree.cssselect('div#main > section#experienceParentWrapper > section#children > article[id^="event-"]')
            for node in nodes:
                event, child_event_id, link = self.parse_event(dept, node, ctx, child=True)

                for item in countdown_num:
                    if item[1] == child_event_id:
                        event.events_end = datetime.utcfromtimestamp( float(item[4][:-3]) )
                        event.save()
                        break
            return len(countdown_num), [datetime.utcfromtimestamp( float(item[4][:-3]) ) for item in countdown_num if item[1] == event_id][0]


    def parse_event(self, dept, node, ctx, child=False):
        """.. :py:method::

        :rtype: (whether this event is_new, event object in database)
        """
        link = node.cssselect('a.eventDoorLink')[0].get('href')
        event_id = link.rsplit('/', 1)[-1]
        link = link if link.startswith('http') else self.siteurl + link
        sale_title = node.cssselect('footer.eventFooter > a.eventDoorContent > div.eventName')[0].text

        event = Event.objects(event_id=event_id).first()
        if not event:
            is_new = True
            event = Event(event_id=event_id)
            event.dept = [dept]
            event.combine_url = link
            event.urgent = True
            event.sale_title = sale_title
            sm = 'http://www.ruelala.com/images/content/events/{event_id}/{event_id}_doorsm.jpg'.format(event_id=event_id)
            lg = 'http://www.ruelala.com/images/content/events/{event_id}/{event_id}_doorlg.jpg'.format(event_id=event_id)
            event.image_urls = [sm] if child else [sm, lg]
        else:
            is_new = False
            if dept not in event.dept: event.dept.append(dept)

        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, key=event_id, is_new=is_new, is_updated=False)
        return event, event_id, link


    def crawl_event_is_product(self, event_id, url, ctx):
        """.. :py:method::
            event is product, get event url, redirect to product url.
            get product url. and parse
        """
        cont = self.net.fetch_page(url)
        product_id = re.compile('http://.*.ruelala.com/product/detail/eventId/\d{1,10}/styleNum/(\d{1,10})/viewAll/0').search(url).group(1)
        tree = lxml.html.fromstring(cont)
        prd = tree.cssselect('div#main section#productAttributes')[0]

        title = prd.cssselect('h2#productName')[0].text_content()
        summary = prd.cssselect('p#shortDesc')[0].text_content()
        returned = prd.cssselect('a#returnsLink')[0].text_content()
        limit = prd.cssselect('div#cartLimit > div#cartLimit')[0].text_content()
        price_node = prd.cssselect('div#productDetailContentWrapper div#packageDetails > section.productPrices')
        listprice = price_node[0].cssselect('span#strikePrice')
        price = price_node[0].cssselect('span#salePrice')

        shipping = tree.cssselect('div#main > div#customContentWrapper > div#customContentTabs > div#expTerms')
        detail = tree.cssselect('div#main > div#customContentWrapper > div#customContentTabs > div#expDetails')
        shipping = shipping[0].text_content() if shipping else ''
        detail = detail[0].text_content() if detail else ''

        product = Product.objects(key=product_id).first()
        is_new, is_updated = False, False
        if not product:
            is_new = True
            product = Product(key=product_id)
            image_count = self.num_image_urls(product_id)
            product.image_urls = self._make_img_urls(product_id, image_count)
            product.title = title
            product.summary = summary
            product.returned = returned
            product.limit = limit
            product.shipping = shipping
            product.detail = detail
            product.listprice = listprice[0].text_content() if listprice else ''
            product.price = price[0].text_content() if price else ''
            product.updated = True
            product.combine_url = url
            ready = 'Product'
        else: ready = None
        product.full_update_time = datetime.utcnow()
        product.save()
        common_saved.send(sender=ctx, key=product_id, is_new=is_new, is_updated=is_updated, ready=ready)


    def crawl_listing(self, url, ctx=''):
        """.. :py:method::
        """
        cont = self.net.fetch_page(url)
        tree = lxml.html.fromstring(cont)
        event_id = self.url2eventid.match(url).group(1)
        nodes = tree.cssselect('div#main > div#productContainerThreeUp > div#productGrid > article.product')
        for node in nodes:
            prd = node.xpath('./div/a[@class="prodName"]')[0]
            title = prd.text_content()
            link = prd.get('href')
            link = link if link.startswith('http') else self.siteurl + link
            product_id = self._url2product_id(link)
            strike_price = node.xpath('./div/span[@class="strikePrice"]')
            strike_price = strike_price[0].text if strike_price else ''
            price = node.xpath('./div/span[@class="productPrice"]')
            price = price[0].text if price else ''
            scarcity = node.xpath('./div/em[@class="childWarning"]')
            scarcity = scarcity[0].text_content() if scarcity else ''
            soldout = node.cssselect('a span.soldOutOverlay')

            product = Product.objects(key=product_id).first()
            is_new, is_updated = False, False
            if not product:
                is_new = True
                product = Product(key=product_id)
                product.event_id = [event_id]
                product.title = title
                product.combine_url = link
                product.listprice = strike_price
                product.price = price
                product.updated = False
                product.soldout = True if soldout else False
            else:
                if product.price != price or product.listprice != strike_price:
                    product.price = price
                    product.listprice = strike_price
                    is_updated = True
                if soldout and product.soldout != True:
                    product.soldout = True
                    is_updated = True
                if event_id not in product.event_id: product.event_id.append(event_id)
            product.list_update_time = datetime.utcnow()
            product.save()
            common_saved.send(sender=ctx, key=product_id, is_new=is_new, is_updated=is_updated)

        event = Event.objects(event_id=event_id).first()
        if not event: event = Event(event_id=event_id)
        if event.urgent == True:
            event.urgent = False
            event.update_time = datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, key=event_id, is_new=False, is_updated=False, ready='Event')


    def num_image_urls(self, product_id):
        """
        the keyworld `RLLZ` in url  meaning large size(about 800*1000), `RLLA` meaning small size (about 10*10)

        :rtype: detect how many image_urls on the product
        """
        prefix = 'http://www.ruelala.com/images/product/'
        for i in xrange(1, 1000):
            sub = '%s/%s_RLLA_%d.jpg' %(product_id[:6], product_id, i+1)
            status = self.net.fetch_image(prefix + sub)
            if status == 404:
                return i

    def _make_img_urls(slef, product_key, img_count):
        """
        the keyworld `RLLZ` in url  meaning large size(about 800*1000), `RLLD` meaning small size (about 400 *500)
        http://www.ruelala.com/images/product/131385/1313856984_RLLZ_1.jpg
        http://www.ruelala.com/images/product/131385/1313856984_RLLZ_2.jpg

        http://www.ruelala.com/images/product/131385/1313856984_RLLZ_1.jpg
        http://www.ruelala.com/images/product/131385/1313856984_RLLZ_2.jpg
        """
        urls = []
        prefix = 'http://www.ruelala.com/images/product/'
        for i in range(0, img_count):
            subfix = '%s/%s_RLLZ_%d.jpg' %(product_key[:6], product_key, i+1)
            url = urllib.basejoin(prefix, subfix)
            urls.append(url)
        return urls

    def crawl_product(self, url, ctx=''):
        """.. :py:method::
            Got all the product basic information and save into the database
        """
        cont = self.net.fetch_page(url)
        tree = lxml.html.fromstring(cont)
        product_id = self._url2product_id(url)
        node = tree.cssselect('div.container section#productContainer')[0]

        list_info = []
        for li in node.cssselect('section#info ul li'):
            list_info.append(li.text_content())
        returned = []
        for p in node.cssselect('section#shipping'):
            returned.append(p.text_content())
        
        #########################
        # section 2 productAttributes
        #########################
        
        attribute_node = node.cssselect('section#productAttributes')[0]
        size_list = attribute_node.cssselect('section#productSelectors ul#sizeSwatches li.swatch a')
        if size_list:
            sizes = [s.text for s in size_list]
        else: sizes = []
        shipping = attribute_node.cssselect('div#readyToShip')
        shipping = shipping[0].text_content() if shipping else ''
        limit = attribute_node.cssselect('div#cartLimit')
        limit = limit[0].text_content() if limit else ''
        ship_rule = attribute_node.cssselect('div#returnsLink ')
        ship_rule = ship_rule[0].text_content() if ship_rule else ''

        colors, image_urls = [], []
        color = attribute_node.cssselect('section#productSelectors ul#colorSwatches > li > a')
        if color:
            for c in color:
                colors.append( c.get('title').lower() )
            for c in colors:
                image_urls.append('http://www.ruelala.com/images/product/{0}/{1}_RLLZ_{2}.jpg'.format(product_id[:6], product_id, c))

        if not image_urls:
            image_count = self.num_image_urls(product_id)
            image_urls = self._make_img_urls(product_id, image_count)

        product, is_new = Product.objects.get_or_create(key=product_id)
        product.image_urls = image_urls
        product.list_info = list_info
        product.returned = '; '.join(returned)
        product.sizes = sizes
        product.shipping = shipping
        product.limit = limit
        product.ship_rule = ship_rule
        product.color = '; '.join(colors) if colors else ''
        if product.updated == False:
            product.updated = True
            ready = 'Product'
        else:
            ready = None
        product.full_update_time = datetime.utcnow()
        product.save()
        common_saved.send(sender=ctx, key=product_id, url=url, is_new=is_new, is_updated=not is_new, ready=ready)


    def _url2product_id(self, url):
        # http://www.ruelala.com/event/product/60118/1411878707/0/DEFAULT
        # or event is product http://www.ruelala.com/product/detail/eventId/59935/styleNum/4112936424/viewAll/0
        m = re.compile('http://.*ruelala.com/event/product/\d{1,10}/(\d{6,10})/\d{1}/DEFAULT').search(url)
        return m.group(1)



if __name__ == '__main__':
    server = Server()
    #server.crawl_listing('http://www.ruelala.com/event/59935')
    url = 'http://www.ruelala.com/event/product/60496/6020835935/1/DEFAULT'
    server.crawl_product(url)
