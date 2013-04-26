# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import gevent
from affiliate import Affiliate
from backends.matching.mechanic_classifier import classify_product_department
from powers.configs import BRAND_EXTRACT
import re, htmlentitydefs
from titlecase import titlecase
from collections import Counter
from datetime import datetime

from helpers.log import getlogger
logger = getlogger('pipelines', filename='/tmp/textserver.log')


def parse_price(price):
    if not price:
        return 0.

    amount = 0.
    pattern = re.compile(r'^[^\d]*(\d+(,\d{3})*(\.\d+)?)')
    match = pattern.search(price)
    if match:
        amount = (match.groups()[0]).replace(',', '')
    return float(amount)


# Removes HTML or XML character references and entities from a text string.
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


class ProductPipeline(object):
    def __init__(self, site, product):
        self.site = site
        self.product = product
        self.__extracter = ProductPipeline.extracter if hasattr(ProductPipeline, 'extracter') else None
        self.__extractor = ProductPipeline.extractor if hasattr(ProductPipeline, 'extractor') else None

    def extract_text(self):
        """
        Do some text data cleaning and standardized processing on the product,
        such as titlecase, html tag remove and so on.
        """
        product = self.product

        # This filter changes all title words to Title Caps,
        # and attempts to be clever about uncapitalizing SMALL words like a/an/the in the input.
        if product.title:
            product.title = titlecase(re.sub("&#?\w+;", " ", product.title))

        # Clean the html tag.
        pattern = r'<[^>]*>'

        if product.list_info:
            str_info = '\n\n\n'.join(product.list_info)
            product.list_info = re.sub(pattern, ' ', str_info).split('\n\n\n')

        if product.shipping:
            product.shipping = re.sub(pattern, ' ',  product.shipping)

        if product.returned:
            product.returned = re.sub(pattern, ' ', product.returned)
            product.returned = product.returned.replace('\r\n', ' ')

    def extract_brand(self):
        site = self.site
        product = self.product

        if product.brand_complete:
            return

        crawled_brand = product.brand or ''
        brand = self.__extracter.extract(crawled_brand)

        if not brand:
            brand = self.__extracter.extract(product.title)
            # For Add Brand should not be extract from the title
            if brand in BRAND_EXTRACT['not_title']:
                brand = None

        if brand:
            product.favbuy_brand = brand
            product.brand_complete=True
            product.update_history['favbuy_brand'] = datetime.utcnow()
            logger.info('product brand extracted -> {0}.{1}'.format(site, product.key))
            return product.favbuy_brand
        else:
            product.update(set__brand_complete=False)
            logger.warning('product brand extract failed -> {0}.{1} {2}'.format(site, product.key, crawled_brand.encode('utf-8')))

        return

    def extract_tag(self, text_list):
        site = self.site
        product = self.product

        if product.tag_complete:
            return

        favbuy_tag = self.__extractor.extract( '\n'.join(text_list).encode('utf-8') )
        product.favbuy_tag = favbuy_tag
        product.tag_complete = bool(favbuy_tag)

        if product.tag_complete:
            product.update_history['favbuy_tag'] = datetime.utcnow()
            logger.info('product tag extracted -> {0}.{1} {2}'.format(site, product.key, product.favbuy_tag))
            return product.favbuy_tag
        else:
            logger.warning('product tag extracted failed -> {0}.{1}'.format(site, product.key))

        return

    def extract_dept(self, text_list):
        site = self.site
        product = self.product

        if product.dept_complete:
            return

        # I don't know where to add this statement, \
        # just ensure that it'll be executed once when the product is crawled at the first time.
        try:
            self.extract_text()
        except:
            pass

        favbuy_dept = classify_product_department(site, product)
        product.favbuy_dept = favbuy_dept
        product.dept_complete = True # bool(favbuy_dept)

        if product.dept_complete:
            product.update_history['favbuy_dept'] = datetime.utcnow()
            logger.info('product dept extracted -> {0}.{1} {2}'.format(site, product.key, product.favbuy_dept))
            return product.favbuy_dept
        else:
            logger.error('product dept extract failed -> {0}.{1}'.format(site, product.key))

        return

    def extract_price(self):
        product = self.product
        is_updated = False
        favbuy_price = None
        listprice = None

        favbuy_price = parse_price(product.price)
        if favbuy_price and str(favbuy_price) != product.favbuy_price:
            product.favbuy_price = str(favbuy_price)
            product.update_history['favbuy_price'] = datetime.utcnow()
            is_updated = True


        listprice = parse_price(product.listprice) or product.favbuy_price
        if listprice and str(listprice) != product.favbuy_listprice:
            product.favbuy_listprice = str(listprice)
            product.update_history['favbuy_listprice'] = datetime.utcnow()
            is_updated = True
        
        return is_updated
    
    def extract_url(self):
        site = self.site
        product = self.product

        if not product.combine_url \
            or product.url_complete:
                return

        affiliate = Affiliate(site)
        product.favbuy_url = affiliate.get_link(product.combine_url)
        product.url_complete = bool(product.favbuy_url)

        if product.url_complete:
            product.update_history['favbuy_url'] = datetime.utcnow()
            return product.favbuy_url
        else:
            logger.warning('product extract url failed -> {0}.{1}'.format(site, product.key))

        return

    def update_events(self):
        """
        To fix the bug that the publisher will ignore the new event added to a product.
        The product should add update_history about adding event to inform the publisher.
        """
        product = self.product
        events = product.event_id

        if not events:
            return

        if not product.update_history.get('event_id'):
            product.update_history['event_id'] = {}

        for event_id in events:
            if event_id not in product.update_history['event_id']:
                product.update_history['event_id'][event_id] = datetime.utcnow()
                product.update_history['events'] = datetime.utcnow()

    def clean(self):
        product = self.product
        if product.disallow_classification:
            return

        print 'start to clean product -> %s.%s' % (self.site, product.key)

        text_list = []
        text_list.append(product.title or u'')
        text_list.extend(product.list_info or [])
        text_list.append(product.summary or u'')
        text_list.append(product.short_desc or u'')
        text_list.extend(product.tagline or [])

        # jobs = [
        #     gevent.spawn(self.extract_brand),
        #     gevent.spawn(self.extract_tag, text_list),
        #     gevent.spawn(self.extract_dept, text_list),
        #     gevent.spawn(self.extract_price),
        #     gevent.spawn(self.extract_url),
        # ]
        # gevent.joinall(jobs)

        updated = False

        if self.extract_brand():
            updated = True

        if self.extract_tag(text_list):
            updated = True

        if self.extract_dept(text_list):
            updated = True

        if self.extract_price():
            updated = True

        if self.update_events():
            updated = True

        return updated


class EventPipeline(object):
    def __init__(self, site, event):
        self.site = site
        self.event = event

    def extract_title(self):
        if not self.event.sale_title:
            return

        sale_title = titlecase(unescape(self.event.sale_title))

        if sale_title != self.event.sale_title:
            self.event.sale_title = sale_title
            self.event.update_history['sale_title'] = datetime.utcnow()
            return self.event.sale_title

        return

    def extract_text(self):
        return self.extract_title()

    def propagate_dept(self, depts, num_products):
        if self.event.disallow_classification:
            return

        dept_threshold = int(.1*num_products)
        favbuy_dept = list(self.event.favbuy_dept) \
            if self.event.favbuy_dept else []

        for k, v in depts.items():
            if v >= dept_threshold:
                favbuy_dept.extend(list(k))
        favbuy_dept = list(set(favbuy_dept))

        if favbuy_dept != self.event.favbuy_dept:
            self.event.favbuy_dept = favbuy_dept
            self.event.update_history['favbuy_dept'] = datetime.utcnow()
            return self.event.favbuy_dept

        return

    def propagate_tag(self, tags):
        favbuy_tag = list(set(tags))

        if favbuy_tag != self.event.favbuy_tag:
            self.event.favbuy_tag = favbuy_tag
            self.event.update_history['favbuy_tag'] = datetime.utcnow()
            return self.event.favbuy_tag

        return

    def propagate_brand(self, brands):
        favbuy_brand = list(set(brands))

        if favbuy_brand != self.event.favbuy_brand:
            self.event.favbuy_brand = favbuy_brand
            self.event.brand_complete = True
            self.event.update_history['favbuy_brand'] = datetime.utcnow()
            return self.event.favbuy_brand

        return

    def propagate_price_and_discount(self, price_set, discount_set):
        price_set = list(price_set)
        price_set.sort()
        discount_set = list(discount_set)
        discount_set.sort()
        lowest_price = str(price_set[0] if price_set else 0)
        highest_price = str(price_set[-1] if price_set else 0)
        lowest_discount = str(discount_set[-1] if discount_set else 1.0)
        highest_discount = str(discount_set[0] if discount_set else 1.0)

        updated = False

        if lowest_price != self.event.lowest_price:
            self.event.lowest_price = lowest_price
            self.event.update_history['lowest_price'] = datetime.utcnow()
            updated = True

        if highest_price != self.event.highest_price:
            self.event.highest_price = highest_price
            self.event.update_history['highest_price'] = datetime.utcnow()
            updated = True

        if lowest_discount != self.event.lowest_discount:
            self.event.lowest_discount = lowest_discount
            self.event.update_history['lowest_discount'] = datetime.utcnow()
            updated = True

        if highest_discount != self.event.highest_discount:
            self.event.highest_discount = highest_discount
            self.event.update_history['highest_discount'] = datetime.utcnow()
            updated = True

        return updated

    def clear_discount(self):
        updated = False

        if self.event.highest_discount:
            self.event.highest_discount = None
            self.event.update_history['highest_discount'] = datetime.utcnow()
            updated = True

        if self.event.lowest_discount:
            self.event.lowest_discount = None
            self.event.update_history['lowest_discount'] = datetime.utcnow()
            updated = True

        return updated

    def propagate(self, products=[]):
        """
        * Data structure for event title.
        * Data structure for dept, tag and brand extraction and propagation
        * Event (lowest, highest) discount, (lowest, highest) price propagation
        * Event & Product begin_date, end_date
        * Event soldout
        """
        if not self.event:
            return

        depts = Counter()
        tags = set()
        event_brands = set()
        price_set = set()
        discount_set = set()
        soldout = True

        counter = 0
        num_products = len(self.event.product_ids) if self.event.product_ids else len(products)
        if num_products == 0:
            return

        print 'start to propogate event -> %s.%s, product amount: %s' % \
            (self.site, self.event.event_id, num_products)

        for product in products:
            # It's important to verify whether the product belongs to the product_id currently.
            if self.event.product_ids and \
                product.key not in self.event.product_ids:
                    continue

            pp = ProductPipeline(self.site, product)
            pp.clean()

            try:
                print 'start to propogate from product -> %s.%s' % (self.site, product.key)

                # Product tag, dept collection
                if product.favbuy_tag:
                    tags = tags.union(product.favbuy_tag)

                if product.favbuy_dept:
                    depts[tuple(product.favbuy_dept)] += 1

                # Product brand collection
                if product.favbuy_brand:
                    event_brands.add(product.favbuy_brand)

                # (lowest, highest) discount, (lowest, highest) price propagation
                try:
                    price = float(product.favbuy_price)
                except Exception, e:
                    logger.error('{0}.product.{1} favbuy price -> {2} exception: {3}'.format(self.site, product.key, product.favbuy_price, str(e)))
                    price = 0.
                try:
                    listprice = float(product.favbuy_listprice)
                except Exception, e:
                    logger.error('{0}.product.{1} favbuy listprice -> {2} exception: {3}'.format(self.site, product.key, product.favbuy_listprice, str(e)))
                    listprice = price
                
                if price > 0:
                    price_set.add(price)
                
                discount = 1.0 * price / listprice if listprice else 1.0
                if discount < 1:
                    discount_set.add(discount)

                # products_begin, products_end
                if not self.event.events_begin:
                    self.event.events_begin = datetime.utcnow()

                if not product.products_begin or \
                    (self.event.events_begin and \
                        product.products_begin < self.event.events_begin):
                            product.products_begin = self.event.events_begin
                            product.update_history['products_begin'] = datetime.utcnow()

                if not product.products_end or \
                    (self.event.events_end and \
                        product.products_end < self.event.events_end):
                            product.products_end = self.event.events_end
                            product.update_history['products_end'] = datetime.utcnow()

                # soldout
                if soldout and ((hasattr(product, 'soldout') and not product.soldout) \
                    or (product.scarcity and int(product.scarcity))):
                        soldout = False

                product.save()
                counter += 1
            except Exception, e:
                logger.error('{0}.{1} product propagation exception'.format(self.site, product.key))

        if not counter:
            return self.event.propagation_complete

        self.extract_text()
        self.propagate_dept(depts, num_products)
        self.propagate_tag(tags)
        self.propagate_brand(event_brands)
        self.propagate_price_and_discount(price_set, discount_set)
        self.event.soldout = soldout

        self.event.propagation_complete = True
        self.event.propagation_time = datetime.utcnow()
        self.event.save()

        return self.event.propagation_complete

    def update_propagation(self, products=[]):
        if not self.event:
            return

        print 'start to update propogate %s event %s' % (self.site, self.event.event_id)

        # unknow how to do

        # update_complete = False
        # event_brands = set(self.event.favbuy_brand) if self.event.favbuy_brand else set()
        # event_tags = set(self.event.favbuy_tag) if self.event.favbuy_tag else set()
        # price_set = set()
        # discount_set = set()

        # try:
        #     price_set.add(float(self.event.lowest_price))
        # except:
        #     print('event lowest_price error')
        # try:
        #     price_set.add(float(self.event.highest_price))
        # except:
        #     print('event highest_price error')
        # try:
        #     discount_set.add(float(self.event.lowest_discount))
        # except:
        #     print('event lowest_discount error')
        # try:
        #     discount_set.add(float(self.event.highest_discount))
        # except:
        #     print('event highest_discount error')

        # if self.event.update_history:
        #     update_propagation_time = self.event.update_history.get('update_propagation') \
        #                                 or self.event.propagation_time
        # else:
        #     update_propagation_time = self.event.propagation_time

        # for product in products:
        #     update_history = product.update_history or {}

        #     # To aggregate the product updated favbuy_brand
        #     if update_history.get('favbuy_brand') \
        #         and update_history['favbuy_brand'] > update_propagation_time:
        #         event_brands.add(product.favbuy_brand)

        #     # To aggregate the product updated favbuy_tag
        #     if update_history.get('favbuy_tag') \
        #         and update_history['favbuy_tag'] > update_propagation_time:
        #         event_tags.add(product.favbuy_tag)

        #     # To update price and discount
        #     if update_history.get('favbuy_price') \
        #         and update_history['favbuy_price'] > update_propagation_time: 
        #         try:
        #             price = float(product.favbuy_price)
        #             price_set.add(price)
        #             listprice = float(product.favbuy_listprice)
        #         except:
        #             logger.error('product {0}.{1} favbuy price error -> {2}/{3}'.format( \
        #                 self.site, product.key, product.favbuy_price, product.favbuy_listprice ))
        #             continue

        #         discount = 1. * price / listprice if listprice else 1.
        #         if discount > 0 and discount < 1:
        #             discount_set.add(discount)

        # # Update the event
        # update_time = datetime.utcnow()

        # if self.propagate_brand(event_brands):
        #     update_complete = True

        # if self.propagate_tag(event_tags):
        #     update_complete = True

        # if self.propagate_price_and_discount(price_set, discount_set):
        #     update_complete = True

        # if self.propagate_price_and_discount(price_set, discount_set):
        #     update_complete = True

        # if update_complete:
        #     self.event.update_history['update_propagation'] = update_time
        #     self.event.save()

        # return update_complete


if __name__ == '__main__':
    pass
