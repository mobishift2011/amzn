# -*- coding: utf-8 -*-
'''
crawlers.venteprivee.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

Created on 2012-11-16

@author: ethan
'''

import time
import pytz
import random
import lxml.html
import zerorpc
from datetime import datetime

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *

req = requests.Session(prefetch=True, timeout=30, config=config, headers=headers)

class VClient(object):
    __base_call_url = 'http://us.venteprivee.com/v1/api'
    
    def __init__(self):
        self.__is_auth = False
    
    def request(self, url):
        r = requests.get(url)
        r.raise_for_status()
        return r.json
    
    def sales(self):
        url = "%s/shop/default" % self.__base_call_url
        return self.request(url).get('sales')
    
    def catalog(self, event_id):
        url = "%s/catalog/content/%s" % (self.__base_call_url, event_id)
        return self.request(url) 
    
    def product_detail(self, pfid):
        url = "%s/productdetail/content/%s" % (self.__base_call_url, pfid)
        return self.request(url)

class ventepriveeLogin(object):
    """.. :py:class:: ventepriveeLogin
        login, check whether login, fetch page.
    """
    def __init__(self):
        """.. :py:method::
            variables need to be used
        """
        self.login_url = 'https://us.venteprivee.com/main/'
        self.data = {
            'email': login_email[DB],
            'password': login_passwd,
            'rememberMe': False,
        }
        self.current_email = 'piipaa@yeah.net'#login_email[DB]
        self._signin = {}

    def login_account(self):
        """.. :py:method::
            use post method to login
        """
        self.data['email'] = self.current_email
        req.get(self.login_url)
        url = 'https://us.venteprivee.com/api/membership/signin'
        req.post(url, data=self.data)
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

        if ret.status_code == 401:
            self.login_account()
            ret = req.get(url)
        if ret.ok: return ret
        return ret.status_code



class Server(object):
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    def __init__(self):
        self.vclient = VClient()
        self.net = ventepriveeLogin()


    def crawl_category(self, ctx='', **kwargs):
        """.. :py:method::
            from self.event_url get all the events
        """
        sales = self.vclient.sales()
        for sale in sales:
            debug_info.send(sender=DB+'.event.{0}.start'.format(sale.get('name').encode('utf-8')))
            events_begin = pytz.timezone('US/Eastern').localize(datetime.strptime(sale.get('startDate'), '%Y-%m-%dT%H:%M:%S')).astimezone(pytz.utc)
            events_end = pytz.timezone('US/Eastern').localize(datetime.strptime(sale.get('endDate'), '%Y-%m-%dT%H:%M:%S')).astimezone(pytz.utc)
            events_begin = datetime(events_begin.year, events_begin.month, events_begin.day, events_begin.hour, events_begin.minute)
            events_end = datetime(events_end.year, events_end.month, events_end.day, events_end.hour, events_end.minute)
            event, is_new = Event.objects.get_or_create(event_id = str(sale.get('operationId'))) 
            if event.events_begin != events_begin:
                event.update_history.update({ 'events_begin': datetime.utcnow() })
                event.events_begin = events_begin
            if event.events_end != events_end:
                event.update_history.update({ 'events_end': datetime.utcnow() })
                event.events_end = events_end
            
            is_updated = False
            event.combine_url = 'https://us.venteprivee.com/main/#/catalog/%s' % event.event_id
            event.sale_title = sale.get('name')
            for media in ['home', 'icon', 'preview']:
                image_url = "http://pr-media04.venteprivee.com/is/image/VPUSA/{0}".format(sale.get('media').get(media))
                if image_url not in event.image_urls:
                    event.image_urls.append(image_url)
            event.sale_description = sale.get('brandDescription')
            event.type = sale.get('type')
            event.dept = [] # TODO cannot get the info
            event.urgent = is_new or event.urgent
            event.update_time = datetime.utcnow()
            event.save()
            
            debug_info.send(sender=DB+'.event.{0}.end'.format(sale.get('name').encode('utf-8')))
            common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)

    def crawl_listing(self, url, ctx='', **kwargs):
        """.. :py:method::
            not useful
        :param url: event url with event_id 
        """
        debug_info.send(sender=DB+'.listing.{0}.start'.format(url))
        if kwargs.get('login_email'): self.net.check_signin( kwargs.get('login_email') )
        else: self.net.check_signin()
        
        response = self.net.fetch_page(url)
        if response is None or isinstance(response, int):
            response = self.net.fetch_page(url)
            if response is None or isinstance(response, int):
                common_failed.send(sender=ctx, key=url.rsplit('/', 1)[-1],
                        url='https://us.venteprivee.com/main/#/catalog/{0}'.format(url.rsplit('/', 1)[-1]),
                        reason="download listing error: %s" % response)
                return
        res = response.json
        
        product_ids = []
        event_id = str(res.get('operationId'))
        products = res.get('productFamilies')
        for prodNode in products:
            is_updated = False
            key = str(prodNode['productFamilyId'])
            soldout =  prodNode.get('isSoldOut')
            product, is_new = Product.objects.get_or_create(key=key)
            if is_new:
                product.title =  prodNode.get('name')
                product.price = prodNode.get('formattedPrice')
                product.listprice = prodNode.get('formattedMsrp')
                product.soldout = soldout
                product.combine_url = 'https://us.venteprivee.com/main/#/product/%s/%s' % (event_id, product.key)
                product.updated = False
            else:
                # is_updated = (product.price != prodNode.get('formattedPrice')) or is_updated
                if soldout and product.soldout != True:
                    product.soldout = True
                    is_updated = True
                    product.update_history.update({ 'soldout': datetime.utcnow() })
            if event_id not in product.event_id: product.event_id.append(event_id)
            product.list_update_time = datetime.utcnow()
            product.save()
            
            debug_info.send(sender=DB+'.listing.product.{0}.crawled'.format(product.key))
            common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=url, is_new=is_new, is_updated=is_updated)
            product_ids.append(key)
        
        event = Event.objects.get(event_id=event_id)
        if not event: event = Event(event_id=event_id)
        if event.urgent == True:
            event.urgent = False
            ready = True
        else: ready = False
        event.product_ids = product_ids
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=False, is_updated=False, ready=ready)
        
        debug_info.send(sender=DB+'.listing.{0}.end'.format(url))

    def crawl_product(self, url, ctx='', **kwargs):
        """.. :py:method::
            Got all the product information and save into the database
        :param url: product url, with product id
        """
        debug_info.send(sender=DB+'.product.{0}.start'.format(url))
        if kwargs.get('login_email'): self.net.check_signin( kwargs.get('login_email') )
        else: self.net.check_signin()
        
        is_updated = False
        ready = False
        response = self.net.fetch_page(url)
        if response is None or isinstance(response, int):
            response = self.net.fetch_page(url)
            if response is None or isinstance(response, int):
                common_failed.send(sender=ctx, key=url.rsplit('/', 1)[-1],
                                   url=url,
                                   reason="download product error: %s" % response)
                return

        res = response.json
        key = str(res.get('productFamilyId'))
        
        product, is_new = Product.objects.get_or_create(key=key)

        product.title = res.get('name')
        product.brand = res.get('operationName')
        product.listprice = res.get('formattedMsrp')
        product.price = res.get('formattedPrice')
        for det in res.get('media').get('det'):
            image_url = 'http://pr-media01.venteprivee.com/is/image/VPUSA/%s' % det.get('fileName')
            if image_url not in product.image_urls:
                product.image_urls.append(image_url)
        product.soldout = res.get('isSoldOut')
        breadCrumb = res.get('breadCrumb').get('name')
        if breadCrumb not in product.dept:
            product.dept.append(breadCrumb)
        product.returned = res.get('returnPolicy')
        product.shipping = '; '.join( res.get('estimatedDeliveryDates') )
        list_info_tree = lxml.html.fromstring( res.get('description') )
        list_info = list_info_tree.xpath('.//div[@class="FTCopierColler_RDV"]/dl[@class="ftBloc"]/dt[contains(text(), "Description")]')
        if not list_info:
            list_info = list_info_tree.xpath('.//div[@class="FTCopierColler_RDV"]/dl[@class="ftBloc"]/dt[contains(text(), "Features")]')
            list_info = list_info[0].getnext() if list_info else []
        else:
            list_info = list_info[0].getnext()
        if not list_info: # After Description, it is </dl>
            list_info = []
            for ii in list_info_tree.xpath('.//div[@class="FTCopierColler_RDV"]/dl[@class="ftBloc"]'):
                list_info.extend(ii.xpath('.//text()'))
            product.list_info = list_info
        else:
            product.list_info = list_info.xpath('.//text()')

#        product.sizes = []#res.get('sizes')    # TODO
#        product.sizes_scarcity = [] # TODO
        temp_updated = product.updated
        product.updated = False if is_new else True
        if product.updated:
            product.full_update_time = datetime.utcnow()
            if not temp_updated and product.updated:
                ready = True
        product.save()
        
        common_saved.send(sender=ctx, obj_type='Product', key=product.key, url=url, is_new=is_new, is_updated=(not is_new) and is_updated, ready=ready)
        debug_info.send(sender=DB+'.product.{0}.end'.format(url))

if __name__ == '__main__':
#    server = zerorpc.Server(Server())
#    server.bind("tcp://0.0.0.0:{0}".format(CRAWLER_PORT))
#    server.run()

    start = time.time()
    
    s = Server()
    s.crawl_category('venteprivee')
    events = Event.objects(urgent=True)
    for event in events:
        s.crawl_listing(event.url(), 'venteprivee')
    products = Product.objects.filter(updated=False)
    for product in products:
        s.crawl_product(product.url(), 'ventiprivee')
    
    print 'total costs: %s (s)' % (time.time() - start)
