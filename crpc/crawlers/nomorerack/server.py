# -*- coding: utf-8 -*-
"""
crawlers.nomorerack.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""

import lxml.html
from datetime import datetime

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *

def fetch_page(url):
    try:
        ret = request.get(url)
    except:
        # page not exist or timeout
        return

    # nomorerack will redirect to homepage automatically when this product is not exists.
    if ret.url == u'http://nomorerack.com/' and ret.url[:-1] != url:
        return 0

    if ret.ok: return ret.content
    else: return ret.status_code

class Server(object):
    """.. :py:class:: Server
        This is zeroRPC server class for ec2 instance to crawl pages.
    """
    def __init__(self):
        self.siteurl = 'http://nomorerack.com'
        self.east_tz = pytz.timezone('US/Eastern')

    def crawl_category(self, ctx=''):
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
            event.events_end = datetime.utcfromtimestamp(float(events_end[:10]))
            event.update_time = datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, key=event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)

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
        common_saved.send(sender=ctx, key='#', url=self.siteurl, is_new=is_new, is_updated=is_updated)

        # categories' deals, with no products_begin time
        categories = ['women', 'men', 'home', 'electronics', 'kids', 'lifestyle']
        for categroy_key in categories:
            is_new, is_updated = False, False
            category = Category.objects(key=category_key).first()
            if not category:
                is_new = True
                category = Category(key=category_key)
                category.is_leaf = True
                category.combine_url = 'http://nomorerack.com/daily_deals/category/{0}'.format(category_key)
            category.update_time = datetime.utcnow()
            category.save()
            common_saved.send(sender=ctx, key=category_key, url=category.combine_url, is_new=is_new, is_updated=is_updated)
    

    def crawl_listing(self, url, ctx=''):
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
        if isinstance(content, int) or content is None:
            common_failed.send(sender=ctx, key=event_id, url=url,
                    reason='download events listing error or {0} return'.format(content))
            return
        tree = lxml.html.fromstring(content)
        primary = tree.cssselect('div#wrapper > div#content > div#front > div#primary')
        sale_description = primary.cssselect('div.events_page_heading > div.text > p.description')[0].text_content().strip()
        nodes = primary.cssselect('div.raw_grid > div.deal')
        for node in nodes:
            soldout = True if node.cssselect('div.image > div.sold_out') else False
            product, is_new, is_updated = self.from_listing_get_info(node, soldout)

            if event_id not in product.event_id: product.event_id.append(event_id)
            product.save()
            common_saved.send(sender=ctx, key=product.key, url=product.combine_url, is_new=is_new, is_updated=is_updated)

        # After this event's products have been saved into DB,
        # send ready signal about this event to image processor
        event = Event.objects(event_id=event_id).first()
        if not event: event = Event(event_id=event_id)
        if not event.sale_description: event.sale_description = sale_description
        if event.urgent == True:
            event.urgent=False,
            ready = 'Event'
        else: ready = None
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, key=event_id, url=event.combine_url, is_new=False, is_updated=False, ready=ready)


    def get_sales_listing(self, url, ctx):
        """.. :py:method::
            Got all the product basic information from sales listing
        """
        if url == self.siteurl:
            _get_today_sales_listing(url, ctx)
        else:
            _get_category_sales_listing(url, ctx)

    def _get_today_sales_listing(self, url, ctx):
        """.. :py:method::
            Got all the product from today's sales listing, products_begin and products_end can be gotten
        """
        content = fetch_page(url)
        if isinstance(content, int) or content is None:
            common_failed.send(sender=ctx, key='#', url=url,
                    reason='download sales listing homepage error or {0} return'.format(content))
            return
        tree = lxml.html.fromstring(content)
        ends = tree.cssselect('div#wrapper > div#content > div#front > div.top > div.ribbon-center > p')[0].text_content()
        ends = ends.split('until')[-1].strip().replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')
        time_str, time_zone = ends.rsplit(' ', 1)
        products_end = time_convert(time_str, '%B %d %I:%M %p%Y', time_zone)
        _eastnow = datetime.now(tz=self.east_tz)
        east_today_begin_in_utc = self.east_tz.localize( datetime(_eastnow.year, _eastnow.month, _eastnow.day) ).astimezone(pytz.utc)

        nodes = tree.cssselect('div#wrapper > div#content > div#front > div#primary > div.deals > div.deal')
        for node in nodes:
            soldout = True if node.cssselect('div.info > h4.sold_out') else False
            product, is_new, is_updated = self.from_listing_get_info(node, soldout)

            if is_new: product.event_type = False # different from events' product
            product.products_begin = east_today_begin_in_utc
            product.products_end = products_end
            product.save()
            common_saved.send(sender=ctx, key=product.key, url=product.combine_url, is_new=is_new, is_updated=is_updated)

    def _get_category_sales_listing(self, url, ctx):
        """.. :py:method::
            Got all the product from categories' sales listing
        """
        category_key = url.rsplit('/', 1)[-1]
        content = fetch_page(url)
        if isinstance(content, int) or content is None:
            common_failed.send(sender=ctx, key=category_key, url=url,
                    reason='download sales listing error or {0} return'.format(content))
            return
        tree = lxml.html.fromstring(content)
        nodes = tree.cssselect('div#wrapper > div#content > div.deals > div.deal')
        for node in nodes:
            soldout = True if node.cssselect('div.info > h4.sold_out') else False
            cats_path = node.cssselect('div.info > h4')[0].text_content() if not soldout else ''
            cats_path = category_key + ' > ' + cats_path if cats_path else ''

            product, is_new, is_updated = self.from_listing_get_info(node, soldout)

            if is_new: product.event_type = False # different from events' product
            if category_key not in product.category_key: product.category_key.append(category_key)
            if cats_path and cats_path not in product.cats: product.cats.append(cats_path)
            product.save()
            common_saved.send(sender=ctx, key=product.key, url=product.combine_url, is_new=is_new, is_updated=is_updated)
        self._get_js_load_products(category_key)


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
        img = node.cssselect('div.image > a.image_tag > img')[0].get('src')
        title = node.cssselect('div.info > div.display > p')[0].text_content()
        price = node.cssselect('div.info > div.display > div.pricing > ins')[0].text_content()
        listprice = node.cssselect('div.info > div.display > div.pricing > del')
        listprice = listprice[0].text_content() if listprice else ''
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
            product.image_urls = [img]
            product.price = price
            product.listprice = listprice
            product.scarcity = scarcity
            product.soldout = soldout
        else:
            if scarcity and product.scarcity != scarcity:
                product.scarcity = scarcity
                is_updated = True
            if soldout and product.soldout != soldout:
                product.soldout = True
                is_updated = True
        product.list_update_time = datetime.utcnow()
        return product, is_new, is_updated


    def _get_js_load_products(self, category_key):
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
                cats_path = node.cssselect('div.info > h4')[0].text_content() if not soldout else ''
                cats_path = category_key + ' > ' + cats_path if cats_path else ''

                product, is_new, is_updated = self.from_listing_get_info(node, soldout)

                if is_new: product.event_type = False # different from events' product
                if category_key not in product.category_key: product.category_key.append(category_key)
                if cats_path and cats_path not in product.cats: product.cats.append(cats_path)
                product.save()
                common_saved.send(sender=ctx, key=product.key, url=product.combine_url, is_new=is_new, is_updated=is_updated)


    def crawl_product(self, url, ctx=''):
        """.. :py:method::
            Got all the product information and save into the database
        """
        product_id = url.rsplit('/', 1)[-1]
        content = fetch_page(url)
        if isinstance(content, int) or content is None:
            common_failed.send(sender=ctx, key=product_id, url=url,
                    reason='download product detail page error or {0} return'.format(content))
            return
        tree = lxml.html.fromstring(content)
        nodes = tree.cssselect('div.deal')


            


    def crawl_product(self, url, ctx=''):
        """.. :py:method::
            Got all the product information and save into the database
        """
        key = url.rsplit('/', 1)[-1]
        key = self.url2product_id(url)
        product,is_new = Product.objects.get_or_create(key=key)
        self.browser.get(url)
        try:
            node = self.browser.find_element_by_css_selector('div#products_view.standard')
        except NoSuchElementException:
            return False

        cat = node.find_element_by_css_selector('div.right h5').text
        title = node.find_element_by_css_selector('div.right h2').text
        summary = node.find_element_by_css_selector('p.description').text
        thumbs = node.find_element_by_css_selector('div.thumbs')
        image_count = len(thumbs.find_elements_by_css_selector('img'))
        try:
            image_url = thumbs.find_element_by_css_selector('img').get_attribute('src')
        except NoSuchElementException:
            image_urls = product.image_urls
        else:
            image_urls = self.make_image_urls(image_url,image_count)
        attributes = node.find_elements_by_css_selector('div.select-cascade select')
        sizes = []
        colors = []
        for attr in attributes:
            ops = attr.find_elements_by_css_selector('option')
            m  = ops[0].get_attribute('value')
            if m == 'Select a size':
                for op in  ops:
                    size = op.get_attribute('value')
                    sizes.append({'size':size})
            elif m == 'Select a color':
                for op in  ops:
                    colors.append(op.text)

        date_str = ''
        try:
            date_str = self.browser.find_element_by_css_selector('div.ribbon-center h4').text
        except NoSuchElementException:
            date_str = self.browser.find_element_by_css_selector('div.ribbon-center p').text
        date_obj = self.format_date_str(date_str)
        price = node.find_element_by_css_selector('div.standard h3 span').text
        listprice = node.find_element_by_css_selector('div.standard p del').text
        product.summary = summary
        product.title = title
        product.cats= [cat]
        product.image_urls = image_urls
        product.products_end = date_obj
        product.price = price
        product.listprice = listprice
        product.pagesize    =   sizes
        product.updated = True

#        for i in locals().items():
#            print 'i',i
        product.save()
        common_saved.send(sender=ctx, site=DB, key=product.key, is_new=is_new, is_updated=not is_new)
        print 'product.cats',product.cats
        return

    def format_date_str(self,date_str):
        """ translate the string to datetime object """

        # date_str = 'This deal is only live until November 2nd 11:59 AM EST'
        #        or  'This event is only live until November 2nd 11:59 AM EST'
        print 're.date str:',date_str
        m = re.compile(r'This (.*)deal is only live until (.*)$').findall(date_str)
        print 're.m',m
        str = m[0][-1]
        return dt_parser.parse(str)

    def make_image_urls(self,url,count):
        urls = []
        m = re.compile(r'^http://nmr.allcdn.net/images/products/(\d+)-').findall(url)
        img_id = m[0]
        for i in range(0,count):
            url = 'http://nmr.allcdn.net/images/products/%s-%d-lg.jpg' %(img_id,i)
            urls.append(url)
        return urls

if __name__ == '__main__':
    server = Server()
    server.crawl_product('http://nomorerack.com/daily_deals/view/128407-product')
