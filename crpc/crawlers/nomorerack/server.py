# -*- coding: utf-8 -*-
"""
crawlers.nomorerack.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""

import re
import time
import lxml.html
from datetime import datetime

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *

header = { 
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,en-US;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Host': 'nomorerack.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/17.0 Firefox/17.0',
}
req = requests.Session(prefetch=True, timeout=30, config=config, headers=header)

def fetch_page(url):
    try:
        ret = req.get(url)
    except:
        # page not exist or timeout
        ret = req.get(url)

    if ret.ok: return ret.content
    else: return ret.status_code

def fetch_product_page(url):
    try:
        ret = req.get(url)
    except:
        # page not exist or timeout
        ret = req.get(url)

    # nomorerack will redirect to homepage automatically when this product is not exists.
    if ret.url == u'http://nomorerack.com/' and ret.url[:-1] != url:
        return -302
    if ret.url == u'http://www.nomorerack.com/' and ret.url[:-1] != url:
        return -302
    elif ret.url.startswith(u'http://nomorerack.com/events/view/'):
        return -302

    if ret.ok: return ret.content
    else: return ret.status_code


class Server(object):
    """.. :py:class:: Server
        This is zeroRPC server class for ec2 instance to crawl pages.
    """
    def __init__(self):
        self.siteurl = 'http://nomorerack.com'
        self.east_tz = pytz.timezone('US/Eastern')

    def crawl_category(self, ctx='', **kwargs):
        """.. :py:method::
            1. Get exclusive event
            2. From top depts, get all the category
        """
        self.get_exclusive_events(ctx)
        self.get_deals_categroy(ctx)

    def get_exclusive_events(self, ctx=''):
        """.. :py:method::
            homepage's events
        """
        content = fetch_page(self.siteurl + '/#events')
        if isinstance(content, int) or content is None:
            content = fetch_page(self.siteurl + '/#events')
            if isinstance(content, int) or content is None:
                common_failed.send(sender=ctx, key='', url=self.siteurl,
                        reason='download homepage events error or {0} return'.format(content))
                return
        tree = lxml.html.fromstring(content)
        nodes = tree.cssselect('div#wrapper > div#content > div#front > div#primary > div[style] > div.events > div.event')
        for node in nodes:
            events_end = node.xpath('./div[@class="countdown"]/@expires_on')[0]
            sale_title = node.cssselect('div.info > a[href] > h3')[0].text_content().strip()
            link = node.cssselect('div.info > a[href]')[0].get('href')
            event_id = link.rsplit('/', 1)[-1]
            img = node.cssselect('div.image > a > img')[0].get('src')

            is_new, is_updated = False, False
            event = Event.objects(event_id=event_id).first()
            if not event:
                is_new = True
                event = Event(event_id=event_id)
                event.urgent = True
                event.combine_url = link if link.startswith('http') else self.siteurl + link
                event.sale_title = sale_title
                if 'large' in img:
                    event.image_urls.append( img.replace('large', 'medium') )
                    event.image_urls.append( img.replace('large', 'thumb') )
                elif 'medium' in img:
                    event.image_urls.append( img.replace('medium', 'large') )
                    event.image_urls.append( img.replace('medium', 'thumb') )
                event.image_urls.append(img)
            events_end = datetime.utcfromtimestamp(float(events_end[:10]))
            if event.events_end != events_end:
                event.update_history.update({ 'events_end': datetime.utcnow() })
                event.events_end = events_end
            event.update_time = datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)

    def get_deals_categroy(self, ctx=''):
        """.. :py:method::
            get deals' categories, can spout them to crawl listing later
        """
        # homepage's deals, we can calculate products_begin time
        is_new, is_updated = False, False
        category = Category.objects(key='#').first()
        if not category:
            is_new = True
            category = Category(key='#')
            category.is_leaf = True
            category.combine_url = self.siteurl
        category.update_time = datetime.utcnow()
        category.save()
        common_saved.send(sender=ctx, obj_type='Category', key='#', url=self.siteurl, is_new=is_new, is_updated=is_updated)

        # categories' deals, with no products_begin time
        categories = ['women', 'men', 'home', 'electronics', 'kids', 'lifestyle']
        for category_key in categories:
            is_new, is_updated = False, False
            category = Category.objects(key=category_key).first()
            if not category:
                is_new = True
                category = Category(key=category_key)
                category.is_leaf = True
                category.combine_url = 'http://nomorerack.com/daily_deals/category/{0}'.format(category_key)
            category.update_time = datetime.utcnow()
            category.save()
            common_saved.send(sender=ctx, obj_type='Category', key=category_key, url=category.combine_url, is_new=is_new, is_updated=is_updated)
    

    def crawl_listing(self, url, ctx='', **kwargs):
        """.. :py:method::
            1. Get events listing page's products
            2. Get deals from different categories
        """
        if 'events' in url:
            self.get_events_listing(url, ctx)
        else:
            self.get_sales_listing(url, ctx)

    def get_events_listing(self, url, ctx):
        """.. :py:method::
            Got all the product basic information from events listing
        """
        event_id = url.rsplit('/', 1)[-1]
        content = fetch_page(url)
        if content is None: content = fetch_page(url)
        if isinstance(content, int) or content is None:
            common_failed.send(sender=ctx, key=event_id, url=url,
                    reason='download events listing error: {0}'.format(content))
            return
        tree = lxml.html.fromstring(content)
        primary = tree.cssselect('div#wrapper > div#content > div#front > div#primary')[0]
        sale_description = primary.cssselect('div.events_page_heading > div.text > p.description')[0].text_content().strip()
        nodes = primary.cssselect('div.raw_grid > div.deal')
        product_ids = []
        for node in nodes:
            soldout = True if node.cssselect('div.image > div.sold_out') else False
            product, is_new, is_updated = self.from_listing_get_info(node, soldout)

            if event_id not in product.event_id: product.event_id.append(event_id)
            product.save()
            common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, is_new=is_new, is_updated=is_updated)
            product_ids.append(product.key)

        # After this event's products have been saved into DB,
        # send ready signal about this event to image processor
        event = Event.objects(event_id=event_id).first()
        if not event: event = Event(event_id=event_id)
        if not event.sale_description: event.sale_description = sale_description
        if event.urgent == True:
            event.urgent = False
            ready = True
        else: ready = False
        event.product_ids = product_ids
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=event.combine_url, is_new=False, is_updated=False, ready=ready)


    def get_sales_listing(self, url, ctx):
        """.. :py:method::
            Got all the product basic information from sales listing
        """
        if url == self.siteurl:
            self._get_today_sales_listing(url, ctx)
        else:
            self._get_category_sales_listing(url, ctx)

    def _get_today_sales_listing(self, url, ctx):
        """.. :py:method::
            Got all the product from today's sales listing, products_begin and products_end can be gotten
        """
        content = fetch_page(url)
        if content is None: content = fetch_page(url)
        if isinstance(content, int) or content is None:
            common_failed.send(sender=ctx, key='#', url=url,
                    reason='download sales listing homepage error or {0} return'.format(content))
            return
        tree = lxml.html.fromstring(content)
        ends = tree.cssselect('div#wrapper > div#content > div#front > div.top > div.ribbon-center > p')[0].text_content()
        ends = ends.split('until')[-1].strip().replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')
        time_str, time_zone = ends.rsplit(' ', 1)
        products_end = time_convert(time_str, '%B %d %I:%M %p%Y', time_zone)
        products_end = datetime(products_end.year, products_end.month, products_end.day, products_end.hour, products_end.minute)
        _eastnow = datetime.now(tz=self.east_tz)
        east_today_begin_in_utc = self.east_tz.localize( datetime(_eastnow.year, _eastnow.month, _eastnow.day) ).astimezone(pytz.utc)
        east_today_begin_in_utc = datetime(east_today_begin_in_utc.year, east_today_begin_in_utc.month, east_today_begin_in_utc.day, east_today_begin_in_utc.hour, east_today_begin_in_utc.minute)

        nodes = tree.cssselect('div#wrapper > div#content > div#front > div#primary > div.deals > div.deal')
        for node in nodes:
            soldout = True if node.cssselect('div.info > h4.sold_out') else False
            product, is_new, is_updated = self.from_listing_get_info(node, soldout)

            product.event_type = False # different from events' product
            if product.products_begin != east_today_begin_in_utc:
                product.update_history.update({ 'products_begin': datetime.utcnow() })
                product.products_begin = east_today_begin_in_utc
            if product.products_end != products_end:
                product.update_history.update({ 'products_end': datetime.utcnow() })
                product.products_end = products_end
            product.save()
            common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, is_new=is_new, is_updated=is_updated)

    def _get_category_sales_listing(self, url, ctx):
        """.. :py:method::
            Got all the product from categories' sales listing
        """
        category_key = url.rsplit('/', 1)[-1]
        content = fetch_page(url)
        if content is None: content = fetch_page(url)
        if isinstance(content, int) or content is None:
            common_failed.send(sender=ctx, key=category_key, url=url,
                    reason='download sales listing error or {0} return'.format(content))
            return
        tree = lxml.html.fromstring(content)
        nodes = tree.cssselect('div#wrapper > div#content > div.deals > div.deal')
        for node in nodes:
            soldout = True if node.cssselect('div.info > h4.sold_out') else False
            tag = node.cssselect('div.info > h4')[0].text_content() if not soldout else ''
            cats_path = category_key + ' > ' + tag if tag else ''

            product, is_new, is_updated = self.from_listing_get_info(node, soldout)

            if is_new: product.event_type = False # different from events' product
            if category_key not in product.category_key: product.category_key.append(category_key)
            if cats_path and cats_path not in product.cats: product.cats.append(cats_path)
            if tag and tag not in product.tagline: product.tagline.append(tag)
            product.save()
            common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, is_new=is_new, is_updated=is_updated)
        self._get_js_load_products(category_key, ctx)


    def from_listing_get_info(self, node, soldout):
        """.. :py:method::
            Both events listing page and deals listing have the same cssselect about one product,
            so collect the same information and return
        :param node: node for cssselect
        :param soldout: true of false
        :rtype: product object, is_new, is_updated
        """
        link = node.cssselect('div.image > a.image_tag')[0].get('href')
        product_id = link.rsplit('/', 1)[-1]
        # img = node.cssselect('div.image > a.image_tag > img')[0].get('src')
        title = node.cssselect('div.info > div.display > p')[0].text_content().encode('utf-8')
        price = node.cssselect('div.info > div.display > div.pricing > ins')[0].text_content().replace('$', '').replace(',', '').strip()
        listprice = node.cssselect('div.info > div.display > div.pricing > del')
        listprice = listprice[0].text_content().replace('$', '').replace(',', '').replace('Retail', '').strip() if listprice else ''
        scarcity = node.cssselect('div.qty > span')
        scarcity = scarcity[0].text_content() if scarcity else ''

        is_new, is_updated = False, False
        product = Product.objects(key=product_id).first()
        if not product:
            is_new = True
            product = Product(key=product_id)
            product.updated = False
            product.combine_url = 'http://nomorerack.com/daily_deals/view/{0}'.format(product_id)
            product.title = title
            # product.image_urls = [img]
            product.price = price
            product.listprice = listprice
            product.scarcity = scarcity
            product.soldout = soldout
        else:
            if scarcity and product.scarcity != scarcity:
                product.scarcity = scarcity
            if soldout and product.soldout != soldout:
                product.soldout = soldout
                is_updated = True
                product.update_history.update({ 'soldout': datetime.utcnow() })
            if product.price != price:
                product.price = price
                product.update_history.update({ 'price': datetime.utcnow() })
            if product.listprice != listprice:
                product.listprice = listprice
                product.update_history.update({ 'listprice': datetime.utcnow() })
        product.list_update_time = datetime.utcnow()
        return product, is_new, is_updated


    def _get_js_load_products(self, category_key, ctx):
        """.. :py:method::
            In listing page of every category, they need js to load more products.
            12 products each times.

        :param category_key: category name of these products
        """
        number = 12
        while True:
            url = 'http://nomorerack.com/daily_deals/category_jxhrq/{0}?offset={1}&sort=best_selling'.format(category_key, number)
            number += 12
            content = fetch_page(url)
            if content is None: content = fetch_page(url)
            if isinstance(content, int) or content is None:
                common_failed.send(sender=ctx, key=category_key, url=url,
                        reason='download sales listing js products error or {0} return'.format(content))
                return
            tree = lxml.html.fromstring(content)
            nodes = tree.cssselect('div.deal')
            if nodes == []: #this is the stop condition
                return
            for node in nodes:
                soldout = True if node.cssselect('div.info > h4.sold_out') else False
                tag = node.cssselect('div.info > h4')[0].text_content() if not soldout else ''
                cats_path = category_key + ' > ' + tag if tag else ''

                product, is_new, is_updated = self.from_listing_get_info(node, soldout)

                if is_new: product.event_type = False # different from events' product
                if category_key not in product.category_key: product.category_key.append(category_key)
                if cats_path and cats_path not in product.cats: product.cats.append(cats_path)
                if tag and tag not in product.tagline: product.tagline.append(tag)
                product.save()
                common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=product.combine_url, is_new=is_new, is_updated=is_updated)


    def crawl_product(self, url, ctx='', **kwargs):
        """.. :py:method::
            Got all the product information and save into the database
        """
        product_id = url.rsplit('/', 1)[-1]
        content = fetch_product_page(url)
        if content is None or isinstance(content, int):
            time.sleep(0.5)
            content = fetch_product_page(url)
            if isinstance(content, int) or content is None:
                common_failed.send(sender=ctx, key=product_id, url=url,
                        reason='download product detail page error: {0}'.format(content))
                return
        tree = lxml.html.fromstring(content)
        node = tree.cssselect('div#wrapper > div#content > div#front > div#primary > div#products_view')[0]
        summary = node.cssselect('div.right > p.description')
        if summary:
            summary = summary[0].text_content().split('Want to know more?')
            if len(summary) == 2:
                summary, list_info = summary[0].strip(), summary[1].strip().split('\n')
            else:
                summary, list_info = summary[0].strip(), []
        image_urls = []
        for img in node.cssselect('div.left > div.images > div.thumbs > img'):
            # image_urls.append( img.get('src') )
            # image_urls.append( img.get('src').replace('tn.', 'rg.') )
            image_urls.append( img.get('src').replace('tn.', 'lg.') ) # we just need one large image

        ends = tree.cssselect('div#wrapper > div#content > div#front > div.ribbon > div.ribbon-center h4')
        if not ends:
            ends = tree.cssselect('div#wrapper > div#content > div#front > div.top > div.ribbon-center > p')
            end = ends[0].text_content()
            if not end:
                end = ends[-1].text_content()
            ends = end 
        else:
            ends = ends[0].text_content()
        ends = ends.split('until')[-1].strip().replace('st', '').replace('nd', '').replace('rd', '').replace('th', '') 
        if ends == '': 
            y, m, d, h, mm, s = re.compile('until: new \$\.countdown\.UTCDate\(.+, (\d+), (.+), (\d+), (\d+), (\d+), (\d+)\),').search(content).groups()
            products_end = datetime(int(y), int(m.split('-')[0]), int(d), int(h), int(mm), int(s))
        else:
            time_str, time_zone = ends.rsplit(' ', 1)

            if len(time_str.split(' ')) == 3:
                time_format = '%B %d %I:%M%p%Y'
            elif len(time_str.split(' ')) == 4:
                time_format = '%B %d %I:%M %p%Y'

            try:
                if 'Augu ' in time_str: time_str = time_str.replace('Augu ', 'August ')
                products_end = time_convert(time_str, time_format, time_zone)
            except ValueError:
                if len(time_str.split(' ')) == 3:
                    a, b, c = time_str.split(' ')
                    if c[:2] == '00' and c[5] == 'A':
                        products_end = time_convert(time_str.replace('AM', ' '), '%B %d %H:%M %Y', time_zone)
                    elif int(c[:2]) >=13 and c[5] == 'P':
                        products_end = time_convert(time_str.replace('PM', ' '), '%B %d %H:%M %Y', time_zone)
                elif len(time_str.split(' ')) == 4:
                    a, b, c, d = time_str.split(' ')
                    if c[:2] == '00' and d[0] == 'A':
                        products_end = time_convert(time_str.replace('AM', ''), '%B %d %H:%M %Y', time_zone)
                    elif int(c[:2]) >=13 and d[0] == 'P':
                        products_end = time_convert(time_str.replace('PM', ''), '%B %d %H:%M %Y', time_zone)

        is_new, is_updated = False, False
        product = Product.objects(key=product_id).first()
        if not product:
            is_new = True
            product = Product(key=product_id)
        product.summary = summary if summary else ''
        product.list_info = list_info if summary else []
        for img in image_urls:
            if img not in product.image_urls: product.image_urls.append(img)
        product.products_end = products_end
        product.full_update_time = datetime.utcnow()

        if product.updated == False:
            product.updated = True
            ready = True
        else: ready = False
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=url, is_new=is_new, is_updated=is_updated, ready=ready)


if __name__ == '__main__':
    url = 'http://nomorerack.com/daily_deals/view/543345-stuhrling_mens_gen_y_sport_chronograph_watch___orange'
    Server().crawl_product(url)
    exit()
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(CRAWLER_PORT))
    server.run()
