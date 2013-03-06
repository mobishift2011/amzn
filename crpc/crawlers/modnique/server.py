#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

"""
crawlers.modnique.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.
need to investigate whether 'the-shops' in category, not event.
"""
import lxml.html
import pytz
import json
from datetime import datetime, timedelta

from models import *
from crawlers.common.events import common_saved, common_failed
from crawlers.common.stash import *

header = {
    'Host':' www.modnique.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Ubuntu/12.10 Chromium/22.0.1229.94 Chrome/22.0.1229.94 Safari/537.4',
}
req = requests.Session(prefetch=True, timeout=30, config=config, headers=header)

def fetch_event(url):
    try:
        ret = req.get(url)
    except:
        # page not exist or timeout
        ret = req.get(url)

    if ret.ok: return ret.content
    else: return ret.status_code

def fetch_product(url):
    """.. :py:method::

    :rtype: -1 redirect to homepage
    """
    try:
        ret = req.get(url)
    except:
        # page not exist or timeout
        ret = req.get(url)

    if ret.ok:
        if 'bzJApp/SalesEventsHome' in ret.url or 'bzJApp/SalesEventDisplay' in ret.url:
            return -302, ret.url
        return ret.content, ret.url
    else:
        return ret.status_code, ret.url


class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.modnique.com'
        self.eventurl = 'http://www.modnique.com/all-sale-events'
        self.extract_slug_id = re.compile('.*/saleevent/(.+)/(\w+)/seeac/gseeac')
        self.extract_slug_product = re.compile('.*/product/.+/\w+/(.+)/(\w+)/color/.*size/seeac/gseeac')
        self.pt = pytz.timezone('US/Pacific')

    def crawl_category(self, ctx='modnique.crawl_category.xxxxx', **kwargs):
        """.. :py:method::
            categories should be ['apparel', 'jewelry-watches', 'handbags-accessories', 'shoes', 'beauty', 'men']
        """
        content = fetch_event(self.eventurl)
        if content is None or isinstance(content, int):
            content = fetch_event(self.eventurl)
        tree = lxml.html.fromstring(content)
        self.upcoming_proc(tree, ctx)

        events = tree.cssselect('div.bgDark > div.mbm > div > div.page > ul#nav > li.fCalc:first-of-type')[0]
        dept_link = {} # get department, link
        for e in events.cssselect('ul.subnav > li.eventsMenuWidth > ul.pbm > li.unit > a.pvn'):
            link = e.get('href')
            dept_link[ link.rsplit('/', 1)[-1] ] = link
        
        # get all events under all the departments
        for e in events.cssselect('ul.subnav > li.eventsMenuWidth > ul.pbm > li.unit > div[title]'):
            sale_title = e.get('title')
            link = e.cssselect('a')[0].get('href')
            slug, event_id = self.extract_slug_id.match(link).groups()
            link = link if link.startswith('http') else self.siteurl + link
            for ii in e.itersiblings(tag='a', preceding=True):
                dept = ii.get('href').rsplit('/', 1)[-1]
                break

            event, is_new, is_updated = self.get_event_from_db(event_id, link, slug, sale_title)
            if dept not in event.dept: event.dept.append(dept)
            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=link, is_new=is_new, is_updated=is_updated)

        # get 'the-shops' category
        link = tree.cssselect('div.bgDark > div.mbm > div > div.page > ul#nav > li.fCalc:nth-of-type(2) > a.phl')[0].get('href')
        self.crawl_shops(link.rsplit('/', 1)[-1], link, ctx)

        # http://www.modnique.com/saleevent/Daily-Deal/2000/seeac/gseeac
        sale = tree.cssselect('div.bgDark > div.mbm > div > div.page > ul#nav > li.fCalc:nth-of-type(3) > a.phl')[0].get('href')
        self.parse_sale(sale, ctx)

        for dept, link in dept_link.iteritems():
            self.crawl_dept(dept, link, ctx)

    def crawl_shops(self, dept, url, ctx):
        """.. :py:method::
            dept can't not add to event here, because all the dept page have all the events.
            Other depts' event is not displayed through js

        :param str dept: department
        :param str url: department url
        """
        content = fetch_event(url)
        if content is None or isinstance(content, int):
            content = fetch_event(url)
        tree = lxml.html.fromstring(content)
        nodes = tree.cssselect('div.bgShops > div#content > div#sales > div.pbm > div.page > ul.bannerfix > li > div.shop_thumb > div.media')
        _utcnow = datetime.utcnow()
        event_id_db = [e for e in Event.objects(events_end__exists=False, dept=['the-shops'])]
        event_id_page = []

        for node in nodes:
            link = node.cssselect('a.sImage')[0].get('href')
            slug, event_id = self.extract_slug_id.match(link).groups()
            link = link if link.startswith('http') else self.siteurl + link
            img = node.cssselect('a.sImage > img')[0].get('data-original')
            if img is None: img = node.cssselect('a.sImage > img')[0].get('src')
            image_urls = [img]
            sale_title = node.cssselect('div.sDefault > div > a > span')[0].text_content().strip()

            event, is_new, is_updated = self.get_event_from_db(event_id, link, slug, sale_title)
            if dept not in event.dept: event.dept.append(dept)
            [event.image_urls.append(img) for img in image_urls if img not in event.image_urls]
            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=link, is_new=is_new, is_updated=is_updated)
            event_id_page.append(event_id)

        if len(event_id_page) > 1: # no download or parse error condition
            for e in event_id_db:
                if e.event_id not in event_id_page:
                    e.events_end = datetime.utcnow()
                    e.update_history.update({ 'events_end': datetime.utcnow() })
                    e.save()
                    common_saved.send(sender=ctx, obj_type='Event', key=e.event_id, url=e.combine_url, is_new=False, is_updated=True)


    def crawl_dept(self, dept, url, ctx):
        """.. :py:method::
            dept can't not add to event here, because all the dept page have all the events.
            Other depts' event is not displayed through js

        :param str dept: department
        :param str url: department url
        """
        content = fetch_event(url)
        if content is None or isinstance(content, int):
            content = fetch_event(url)
        tree = lxml.html.fromstring(content)
        nodes = tree.cssselect('div.bgDark > div#content > div.sales > div.pbm > div.page > ul.bannerfix > li#saleEventContainer > div.sale_thumb > div.media')
        _utcnow = datetime.utcnow()
        for node in nodes:
            link = node.cssselect('a.sImage')[0].get('href')
            slug, event_id = self.extract_slug_id.match(link).groups()
            link = link if link.startswith('http') else self.siteurl + link
            img = node.cssselect('a.sImage > img')[0].get('data-original')
            if img is None: img = node.cssselect('a.sImage > img')[0].get('src')
            image_urls = [img.replace('B.jpg', 'A.jpg'), img]
            sale_title = node.cssselect('div.sDefault > div > a > span')[0].text_content().strip()

            time_text = node.cssselect('div.sRollover > div > a > span.title_time_banner')[0].text_content()
            day, hour, minute = time_text.split('Ends')[-1].strip().split()
            ends = timedelta(days=int(day[:-1]), hours=int(hour[:-1]), minutes=int(minute[:-1])) + _utcnow
            hour = ends.hour + 1 if ends.minute > 50 else ends.hour
            events_end = datetime(ends.year, ends.month, ends.day, hour)

            event, is_new, is_updated = self.get_event_from_db(event_id, link, slug, sale_title)
            [event.image_urls.append(img) for img in image_urls if img not in event.image_urls]
            if event.events_end != events_end:
                event.update_history.update({ 'events_end': datetime.utcnow() })
                event.events_end = events_end
            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=link, is_new=is_new, is_updated=is_updated)

    def upcoming_proc(self, tree, ctx):
        """.. :py:method::
        """
        _utcnow = datetime.utcnow()
        nodes = tree.cssselect('div#content > div#upcoming_sales li#upcoming_sales_container > div.sale_thumb > div.media')
        for node in nodes:
            link = node.cssselect('div.sRollover > div.mbs > a')[0].get('href')
            slug, event_id = self.extract_slug_id.match(link).groups()
            link = link if link.startswith('http') else self.siteurl + link
            img = node.cssselect('a.sImage > img')[0].get('data-original')
            if img is None:
                img = node.cssselect('a.sImage > img')[0].get('src')
            image_urls = [img.replace('M.jpg', 'A.jpg'), img.replace('M.jpg', 'B.jpg')]
            sale_title = node.cssselect('a.sImage')[0].get('title')

            day, hour, minute = node.cssselect('div#sDefault_{0} > div'.format(event_id))[0].text_content().split('in')[-1].strip().split()
            begins = timedelta(days=int(day[:-1]), hours=int(hour[:-1]), minutes=int(minute[:-1])) + _utcnow
            hour = (begins.hour+1) % 24 if begins.minute > 50 else begins.hour
            events_begin = datetime(begins.year, begins.month, begins.day, hour)

            event, is_new, is_updated = self.get_event_from_db(event_id, link, slug, sale_title)
            [event.image_urls.append(img) for img in image_urls if img not in event.image_urls]
            if event.events_begin != events_begin:
                event.update_history.update({ 'events_begin': datetime.utcnow() })
                event.events_begin = events_begin
            if event.events_end != None:
                event.events_end = None
                event.update_history.update({ 'events_end': datetime.utcnow() })
            if event.product_ids != []: 
                event.product_ids = []
                event.update_history.update({ 'product_ids': datetime.utcnow() })

            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=link, is_new=is_new, is_updated=is_updated)


    def get_event_from_db(self, event_id, link, slug, sale_title):
        """.. :py:method::
            get a event object from database
        :param str event_id:
        :param str link: event link
        :param str slug: slug in link
        :param str sale_title: event sale title
        :rtype: list of `event, is_new, is_updated`
        """
        is_new, is_updated = False, False
        event = Event.objects(event_id=event_id).first()
        if not event:
            is_new = True
            event = Event(event_id=event_id)
            event.urgent = True
            event.combine_url = link
            event.slug = slug
            event.sale_title = sale_title
        event.update_time = datetime.utcnow()
        return event, is_new, is_updated


    def crawl_listing(self, url, ctx='modnique.crawl_listing.xxxxx', **kwargs):
        """.. :py:method::
        """
        slug, event_id = self.extract_slug_id.match(url).groups()
        content = fetch_event(url)
        if content is None or isinstance(content, int):
            content = fetch_event(url)
            if content is None or isinstance(content, int):
                common_failed.send(sender=ctx, key=event_id, url=url,
                    reason='download listing url error, {0}'.format(content))
                return

        product_ids = []
        tree = lxml.html.fromstring(content)
        nodes = tree.cssselect('div.line > div.page > div#items > ul#products > li.product')
        for node in nodes:
            js = json.loads(node.get('data-json'))
            color = js['color'] if 'color' in js else ''
#            try:
#                abandon, color = node.get('id').rsplit('_', 1) # item_57185525_gunmetal
#                if color.isdigit(): color = ''
#            except AttributeError:
#                pass
            title = node.cssselect('div.item_thumb2 > div.itemTitle > h6.neutral')[0].text_content().strip()
            link = node.cssselect('div.item_thumb2 > div.hd > a.item_link')[0].get('href').strip() # link have '\r\n'
            link = link if link.startswith('http') else self.siteurl + link
            slug, key = self.extract_slug_product.match(link).groups()

            price = node.cssselect('div.item_thumb2 > div > div.media > div.bd > p > span.price')[0].text_content().replace('modnique', '').strip()
            listprice = node.cssselect('div.item_thumb2 > div > div.media > div.bd > p > span.bare')
            listprice = listprice[0].text_content().replace('retail', '').strip() if listprice else ''
            soldout = True if node.cssselect('div.item_thumb2 > div.soldSticker') else False

            is_new, is_updated = False, False
            product = Product.objects(key=key).first()
            if not product:
                is_new = True
                product = Product(key=key)
                product.updated = False
                product.combine_url = link
                product.color = color
                product.title = title
                product.slug = slug
                product.listprice = listprice
                product.price = price
                product.soldout = soldout
            else:
                if soldout and product.soldout != True:
                    product.soldout = True
                    is_updated = True
                    product.update_history.update({ 'soldout': datetime.utcnow() })
                if product.combine_url != link:
                    product.combine_url = link
                    product.update_history.update({ 'combine_url': datetime.utcnow() })
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
        else: ready = False
        event.product_ids = product_ids
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event_id, is_new=False, is_updated=False, ready=ready)


    def crawl_product(self, url, ctx='', **kwargs):
        """.. :py:method::
        """
        slug, key = self.extract_slug_product.match(url).groups()
        content = fetch_product(url)
        if content is None or isinstance(content[0], int):
            content = fetch_product(url)
            if content is None or isinstance(content[0], int):
                common_failed.send(sender=ctx, key=key, url=url,
                        reason='download product url error, {0}'.format(content))
                return
        tree = lxml.html.fromstring(content[0])

        image_urls, shipping, list_info, brand, returned = self.parse_product(tree)

        is_new, is_updated = False, False
        product = Product.objects(key=key).first()
        if not product:
            is_new = True
            product = Product(key=key)
        [product.image_urls.append(img) for img in image_urls if img not in product.image_urls]
        product.shipping = shipping
        product.list_info = list_info
        product.returned = returned
        product.full_update_time = datetime.utcnow()
        if product.updated == False:
            product.updated = True
            ready = True
        else: ready = False
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=key, url=url, is_new=is_new, is_updated=is_updated, ready=ready)


    def parse_product(self, tree):
        nav = tree.cssselect('div > div.ptl > div.page > div.line')[0] # bgDark or bgShops
        images = nav.cssselect('div > div#product_gallery > div.line > div#product_imagelist > a')
        image_urls = []
        for img in images:
            img_url = img.get('href') 
            # lots of page don't have super image, or only have several super, then get the medium
            if img_url == 'http://llthumb.bids.com/mod$image.getSuperImgsSrc()':
                img_url = img.cssselect('img')[0].get('src')
            image_urls.append( img_url )
        shipping = nav.cssselect('div.lastUnit > div.line form div#item_content_wrapper > div#item_wrapper > div#product_delivery')[0].text_content().strip()
        info = nav.cssselect('div.lastUnit > div.line div#showcase > div.container')[0]
        list_info = []
        nodes = info.cssselect('div.tab_container > div#tab1 p')
        for node in nodes:
            text = node.text_content().strip()
            if text.isdigit(): continue
            if text: list_info.append(text)

        brand = info.cssselect('div#tab4')[0].text_content().strip()
        returned = info.cssselect('div#tab5')[0].text_content().strip()
        return image_urls, shipping, list_info, brand, returned


    def parse_sale(self, url, ctx):
        content = fetch_product(url)
        if content is None or isinstance(content[0], int):
            common_failed.send(sender=ctx, key='', url=url,
                    reason='download product url error, {0}'.format(content))
            return
        tree = lxml.html.fromstring(content[0])
        key = re.compile('.*itemid=([^&]+).*').match(content[1]).group(1)

        image_urls, shipping, list_info, brand, returned = self.parse_product(tree)
        nav = tree.cssselect('div > div.ptl > div.page > div.line')[0] # bgDark or bgShops
        pprice = nav.cssselect('div.lastUnit > div.line form > div.mod > div.hd > div.media > div.bd')[0]
        price = pprice.cssselect('span.price')[0].text_content()
        listprice = pprice.cssselect('span.bare')
        listprice = listprice[0].text_content().replace('retail', '').strip() if listprice else ''
        title = nav.cssselect('div.lastUnit > div.line > h4.pbs')[0].text_content().strip()

        is_new, is_updated = False, False
        product = Product.objects(key=key).first()
        if not product:
            is_new = True
            product = Product(key=key)
        product.combine_url = content[1]
        [product.image_urls.append(img) for img in image_urls if img not in product.image_urls]
        product.shipping = shipping
        product.list_info = list_info
        product.returned = returned
        product.price = price
        product.listprice = listprice
        product.title = title
        product.event_type = False
        product.products_begin = datetime.now(tz=self.pt).replace(hour=0, minute=0, second=0, microsecond=0).astimezone(pytz.utc)
        product.products_end = product.products_begin + timedelta(days=1)
        product.full_update_time = datetime.utcnow()
        if is_new:
            product.updated = True
            ready = True
        else: ready = False
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=key, url=url, is_new=is_new, is_updated=is_updated, ready=ready)


if __name__ == '__main__':
    import zerorpc
    from settings import CRAWLER_PEERS
    server = zerorpc.Server(Server(), heartbeat=None)
    server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PEERS[0]['port']))
    server.run()
