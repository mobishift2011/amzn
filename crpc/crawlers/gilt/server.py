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
        self.crawl_sales(ctx)
    
    def crawl_listing(self, url, ctx):
        """.. :py:method::
            from url get listing page.
            from listing page get Eventi's description, endtime, number of products.
            Get all product's image, url, title, price, soldout

        :param url: listing page url
        """
        pass
    
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
        is_new = not product.updated
        product.product_key = product_key
        if is_new:
            print(DB+ ' crawling new product %s' % product.product_key)
        else:
            print(DB+ ' crawling old product %s' % product.product_key)
        product.title = res.get('name')
        product.brand = res.get('brand')
        product.image_urls = [urls[0].get('url') for urls in res.get('image_urls').values()]
        content = res.get('content')
        if content:
            product.list_info = content.get('description').strip().split('  ')
            product.list_info.append('material: ' + (content.get('material') or ''))
            product.list_info.append('origin: ' + (content.get('origin') or ''))
        product.dept = res.get('categories')
        
        is_updated = False
        soldout = True
        product.soldout = True
        for sku in res.get('skus'):
            product.skus.append(sku.get('id'))
            price = sku.get('msrp_price')
            is_updated = True if not (product.price == price) else is_updated
            product.price == price
            
            listprice = sku.get('sale_price')
            is_updated = True if not (product.listprice == listprice) else is_updated
            product.listprice = listprice
            
            if sku.get('inventory_status') == "for sale":
                soldout = False
                is_updated = True if not (product.soldout == soldout) else is_updated
                product.soldout = soldout
            else:
                if sku.get('attributes'):
                    product.sizes_scarcity.append(sku.get('attributes')[0].get('value'))
        product.updated = True
        product.full_update_time = datetime.datetime.utcnow()
        product.save()
        
        print(DB+'.product.{0}.end'.format(url))
        common_saved.send(sender=ctx, key=product.product_key, url=url, is_new=is_new, is_updated=is_updated)
    
    def crawl_sales(self, ctx, store=None):
        if store:
            print(DB+'.store.{0}.begin'.format(store))
            time.sleep(3)
            
            sales_active = giltClient.sales_active(store)
            map(lambda x: self.process_sale(ctx, x), sales_active.get('sales'))
            sales_upcoming = giltClient.sales_upcoming(store)
            map(lambda x: self.process_sale(ctx, x), sales_active.get('sales'))
            
            print(DB+'.store.{0}.end'.format(store))
        else:
            map(lambda x: self.crawl_sales(ctx, x), giltClient.stores())
    
    def process_sale(self, ctx, sale):
        print(DB+'.event.{0}.start'.format(sale.get('name').encode('utf-8')))
        
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
        event.is_leaf = bool(sale.get('products'))
        event.sale_description = sale.get('description')
        event.save()
        
        is_updated = False
        if event.is_leaf:
            for url in sale.get('products'):
                product_id = (url.split('/products/')[1]).split('/')[0] ###TODO 取得product_id
                product, prod_new = Product.objects.get_or_create(key=str(product_id))
                if prod_new:
                    print(DB+ ' new product %s from category %s' % (product.key, event.sale_title))
                else:
                    print(DB+ ' old product %s from category %s' % (product.key, event.sale_title))
                product.product_key = product_id
                product.event_id.append(event.event_id)
                product.store = event.store
                product.list_update_time = datetime.datetime.utcnow()
                product.updated = not prod_new if prod_new else product.updated
                product.save()
                
                is_updated = prod_new
        
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
    
    products = Product.objects.filter(updated=False)
    for product in products:
        s.crawl_product(product.url(), 'gilt')
    print 'total cost(s): %s' % (time.time()-timer)