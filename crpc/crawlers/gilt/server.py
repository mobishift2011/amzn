# -*- coding: utf-8 -*-
"""
crawlers.gilt.server
~~~~~~~~~~~~~~~~~~~~~~

Implements Product and Category crawling for Gilt

Created on 2012-10-26

@author: ethan

"""

from settings import RPC_PORT
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
        map(lambda x: self.process_sale(x, ctx), sales_active.get('sales'))
    
    def crawl_listing(self, url, ctx):
        """.. :py:method::
            from url get listing page.
            from listing page get Eventi's description, endtime, number of products.
            Get all product's image, url, title, price, soldout

        :param url: listing page url
        """
        print(DB+'.listing.{0}.begin'.format(url))
        sale = giltClient.request(url)
        
        if sale.get('products'):
            map(lambda x: self.crawl_product(x, ctx), sale.get('products'))
        
        event = Event.objects(event_id = sale.get('sale_key')).first()
        if event:
            event.urgent = False
            event.save()
        
        print(DB+'.listing.{0}.end'.format(url))
                
    
    def crawl_product(self, url, ctx):
        """.. :py:method::
            Got all the product information and save into the database

        :param url: product url
        """
        print(DB+'.product.{0}.begin'.format(url))
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
        product_url_split = res.get('url').split('/product/')   ######eg."http://www.gilt.com/sale/women/jack-rogers-6838/product/165556423-jack-rogers-jill-classic-moccasin?
        product_key = product_url_split[1].split('?')[0]
        
        # product, is_new = Product.objects.get_or_create(pk=str(res.get('id')))
        product = Product.objects.filter(pk=str(res.get('id'))).first()
        if not product:
            product = Product(pk=str(res.get('id')))
            product.updated = False
            product.save()
            is_new = True
        else:
            is_new = False
        
        if product.updated:
            print(DB+ ' crawling old product %s' % product_key)
            is_updated = False
        else:
            print(DB+ ' crawling new product %s' % product_key)
            is_updated = True
        
        product.product_key = product_key
        product.title = res.get('name')
        product.brand = res.get('brand')
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
            price = sku.get('msrp_price')
            is_updated = True if (product.price != price and not is_new) else is_updated
            product.price = price
            
            listprice = sku.get('sale_price')
            is_updated = True if (product.listprice != listprice and not is_new) else is_updated
            product.listprice = listprice
            
            if sku.get('inventory_status') == "for sale":
                soldout = False
                is_updated = True if (product.soldout != soldout and not is_new) else is_updated
            else:
                if sku.get('attributes'):
                    product.sizes_scarcity.append(sku.get('attributes')[0].get('value'))
        product.soldout = soldout
        product.updated = False if is_new else True
        product.full_update_time = datetime.datetime.utcnow()
        product.save()
        
        print(DB+'.product.{0}.end'.format(url))
        common_saved.send(sender=ctx, key=product.product_key, url=url, is_new=is_new, is_updated=(not is_new) and is_updated)
    
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
    
    def process_sale(self, sale, ctx):
        print(DB+'.event.{0}.start'.format(sale.get('name').encode('utf-8')))
        
        is_updated = False
        event, is_new = Event.objects.get_or_create(event_id = sale.get('sale_key'))
        event.sale_title = sale.get('name')
        event.event_id = sale.get('sale_key')
        event.store = sale.get('store')
        if event.store not in event.dept:
            event.dept.append(event.store)
        event.type = 'sale'
        event.image_urls = [urls[0].get('url') for urls in sale.get('image_urls').values()]
        event.events_begin = datetime.datetime.strptime(sale.get('begins'), '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
        event.events_end = datetime.datetime.strptime(sale.get('ends'), '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
        #        upcoming = sale.get('begins') > datetime.datetime.now()
        
        is_updated = (event.is_leaf != bool(sale.get('products'))) and not is_new
        event.is_leaf = bool(sale.get('products'))
        event.sale_description = sale.get('description')
        if is_new or is_updated:
            event.urgent = True
        event.save()
        
        common_saved.send(sender=ctx, key=event.event_id, url=sale.get('sale_url'), is_new=is_new, is_updated=(not is_new) and is_updated)
#        map(lambda url: self.process_product(url, sale), sale.get('products') or [])
#        print(DB+'.event.{{0}}.end'.format(sale.get('name')))


if __name__ == '__main__':
#    server = zerorpc.Server(Server())
#    server.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
#    server.run()
    timer=time.time()
    s = Server()
#    s.crawl_category('gilt')
    events = Event.objects(urgent=True, is_leaf=True).order_by('-update_time').timeout(False)
    for event in events:
        s.crawl_listing(event.url(), 'gilt')
        break
#    products = Product.objects.filter(updated=False)
#    for product in products:
#        s.crawl_product(product.url(), 'gilt')
    print 'total cost(s): %s' % (time.time()-timer)