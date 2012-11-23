# -*- coding: utf-8 -*-
"""
crawlers.gilt.server
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category crawling for Gilt

Created on 2012-10-26

@author: ethan

"""

from settings import CRAWLER_PORT
from crawlers.common.events import *
from crawlers.common.crawllog import *
from crawlers.common.stash import *
from models import *
import datetime, time, pytz


class Server(object):
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    def __init__(self):
        pass


    def crawl_category(self, ctx):
        """.. :py:method::
            From top depts, get all the events(sales)
        """
        sales_active = giltClient.sales_active()
        map(lambda x: self.process_sale(x, ctx), sales_active.get('sales'))
        sales_upcoming = giltClient.sales_upcoming()
        map(lambda x: self.process_sale(x, ctx), sales_upcoming.get('sales'))
    

    def crawl_listing(self, url, ctx):
        """.. :py:method::
            from url get listing page.
            from listing page get Eventi's description, endtime, number of products.
            Get all product's image, url, title, price, soldout

        :param url: listing page url
        """
        debug_info.send(sender=DB+'.listing.{0}.begin'.format(url))

        is_updated = False
        sale = giltClient.request(url)
        try:
            event = Event.objects.get(event_id = sale.get('sale_key'))
        except Exception, e:
            common_failed.send(sender=ctx, url=url, reason='event_id does not exist in our db:{0}'.format(str(e)))
        
        ready = 'Event' if event.urgent else None
        event.urgent = False
        event.save()
        common_saved.send(sender=ctx, key=event.event_id, url=event.combine_url, is_new=False, is_updated=is_updated, ready=ready)

        if sale.get('products'):
            event.is_leaf = True
            event.save()
            map(lambda x: self.process_product(x, ctx, event.event_id), sale.get('products'))
        else:
            event.is_leaf = False
            event.save()

        debug_info.send(sender=DB+'.listing.{0}.end'.format(url))


    def crawl_product(self, url, ctx):
        """.. :py:method::
            Got all the product information and save into the database

        :param url: product url
        """
        self.process_product(url, ctx)
    

    def process_sale(self, sale, ctx):
        debug_info.send(sender=DB+'.event.{0}.start'.format(sale.get('sale_key').encode('utf-8')))

        is_updated = False
        event, is_new = Event.objects.get_or_create(event_id = sale.get('sale_key'))

        event.event_id = sale.get('sale_key')
        event.sale_title = sale.get('name')
        event.store = sale.get('store')
        if event.store and event.store not in event.dept:
            event.dept.append(event.store)
        event.combine_url = sale.get('sale_url')
        event.image_urls = [urls[0].get('url') for urls in sale.get('image_urls').values()]

        events_begin = datetime.datetime.strptime(sale.get('begins'), '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
        events_end = datetime.datetime.strptime(sale.get('ends'), '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
        is_updated = (not is_new and events_begin != pytz.UTC.localize(event.events_begin)) or is_updated
        is_updated = (not is_new and events_end != pytz.UTC.localize(event.events_end)) or is_updated
        event.events_begin = events_begin
        event.events_end = events_end

        event.sale_description = sale.get('description')
        event.urgent = is_new or event.urgent
        event.save()

        debug_info.send(sender=DB+'.event.{0}.end'.format(sale.get('sale_key').encode('utf-8')))
        common_saved.send(sender=ctx, key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=(not is_new) and is_updated, ready=ready)


    def process_product(self, url, ctx, event_id=None):
        debug_info.send(sender=DB+'.product.{0}.begin'.format(url))
        try:
            time.sleep(1.2)
            res = giltClient.request(url)
        except requests.exceptions.HTTPError, e:
            print(DB+'.product.{0}.error: {1}'.format(url, str(e)))
            common_failed.send(sender=ctx, url=url, reason=str(e))
            return
        except requests.exceptions.ConnectionError, e:
            print(DB+'.product.{0}.error: {1}'.format(url, str(e)))
            common_failed.send(sender=ctx, url=url, reason=str(e))
            return

        is_updated = False
        product, is_new = Product.objects.get_or_create(key=str(res.get('id')))
        ready = 'Product' if is_new else None

        if is_new:
            print(DB+ ' crawling new product %s' % product.key)
        else:
            print(DB+ ' crawling old product %s' % product.key)
        
        if event_id and event_id not in product.event_id:
            product.event_id.append(event_id)
        product.title = res.get('name')
        product.brand = res.get('brand')
        product.combine_url = res.get('url')
        product.image_urls = [urls[0].get('url') for urls in res.get('image_urls').values()]
        content = res.get('content')
        if content:
            product.list_info = content.get('description').strip().split('  ')
            product.list_info.append('material: ' + (content.get('material') or ''))
            product.list_info.append('origin: ' + (content.get('origin') or ''))
        product.dept = res.get('categories')
        
        soldout = True
        for sku in res.get('skus'):
            product.skus.append(sku.get('id'))
            price = sku.get('sale_price')
            is_updated = True if (product.price != price and not is_new) else is_updated
            product.price = price
            
            listprice = sku.get('msrp_price')
            is_updated = True if (product.listprice != listprice and not is_new) else is_updated
            product.listprice = listprice
            
            if sku.get('inventory_status') == "for sale":
                soldout = False
            else:
                if sku.get('attributes'):
                    product.sizes_scarcity.append(sku.get('attributes')[0].get('value'))
        is_updated = True if (product.soldout != soldout and not is_new) else is_updated
        product.soldout = soldout
        product.updated = True
        product.full_update_time = datetime.datetime.utcnow()
        product.save()
        
        debug_info.send(sender=DB+'.product.{0}.end'.format(url))
        common_saved.send(sender=ctx, key=product.key, url=product.combine_url, is_new=is_new, is_updated=(not is_new) and is_updated, ready=ready)


#    def crawl_sales(self, ctx, store=None):
#        if store:
#            print(DB+'.store.{0}.begin'.format(store))
#            time.sleep(3)
#            
#            sales_active = giltClient.sales_active(store)
#            map(lambda x: self.process_sale(ctx, x), sales_active.get('sales'))
#            sales_upcoming = giltClient.sales_upcoming(store)
#            map(lambda x: self.process_sale(ctx, x), sales_active.get('sales'))
#            
#            print(DB+'.store.{0}.end'.format(store))
#        else:
#            map(lambda x: self.crawl_sales(ctx, x), giltClient.stores())


def local_test():
    timer=time.time()
    s = Server()
    # s.crawl_category('gilt')
    events = Event.objects(urgent=False).order_by('-update_time').timeout(False)
    for event in events:
        s.crawl_listing(event.url(), 'gilt')
    # products = Product.objects.filter(updated=False)
    # for product in products:
    #     s.crawl_product(product.url(), 'gilt')
    print 'total cost(s): %s' % (time.time()-timer)

if __name__ == '__main__':
#    server = zerorpc.Server(Server())
#    server.bind("tcp://0.0.0.0:{0}".format(CRAWLER_PORT))
#    server.run()
    local_test()