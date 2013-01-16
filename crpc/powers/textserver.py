# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import gevent
import zerorpc

from settings import TEXT_PORT, CRPC_ROOT
from backends.matching.extractor import Extractor
from backends.matching.mechanic_classifier import classify_product_department

from brandapi import Extracter
from tools import Propagator
from powers.events import *
from models import Stat

from powers.events import brand_refresh
from crawlers.common.stash import exclude_crawlers
from datetime import datetime
import re
from os import listdir
from os.path import join, isdir
from titlecase import titlecase

from helpers.log import getlogger
logger = getlogger('textserver', filename='/tmp/textserver.log')

_extracter =  Extracter()

class TextServer(object):
    def __init__(self):
        self.__extracter = _extracter  # brand extracter
        self.__extractor = Extractor()  # tag extractor
        self.__m = {}
        
        for name in listdir(join(CRPC_ROOT, "crawlers")):
            path = join(CRPC_ROOT, "crawlers", name)
            if name not in exclude_crawlers and isdir(path):
                self.__m[name] = __import__("crawlers."+name+'.models', fromlist=['Event', 'Product'])

    def __extract_text(self, product):
        """
        Do some text data cleaning and standardized processing on the product,
        such as titlecase, html tag remove and so on.
        """
        # This filter changes all title words to Title Caps,
        # and attempts to be clever about uncapitalizing SMALL words like a/an/the in the input.
        if product.title:
            product.title = titlecase(product.title)

        # Clean the html tag.
        pattern = r'<[^>]*>'

        if product.list_info:
            str_info = '\n\n\n'.join(product.list_info)
            product.list_info = re.sub(pattern, ' ', str_info).split('\n\n\n')

        if product.shipping:
            product.shipping = re.sub(pattern, ' ', product.shipping)

        if product.returned:
            product.returned = re.sub(pattern, ' ', product.returned)
            product.returned = product.returned.replace('\r\n', ' ')

    def __extract_price(self, product, flags):
        if not product.favbuy_price:
            price = parse_price(product.price)
            product.favbuy_price = str(price)
            flags['favbuy_price'] = True

        if not product.favbuy_listprice:
            listprice = parse_price(product.listprice) or product.favbuy_price
            product.favbuy_listprice = str(listprice)
            flags['favbuy_listprice'] = True

    def __extract_brand(self, brand_complete, product, flags, site):
        if brand_complete:
            return

        crawled_brand = product.brand or ''
        brand = self.__extracter.extract(crawled_brand) or \
                    self.__extracter.extract(product.title)
        if brand:
            product.favbuy_brand = brand
            product.brand_complete=True
            product.update_history['favbuy_brand'] = datetime.utcnow()
            flags['favbuy_brand'] = True
            logger.info('{0}.product.{1} extract brand {2} -> {3} OK'.format(site, product.key, crawled_brand, brand))
        else:
            product.update(set__brand_complete=False)
            logger.warning('{0}.product.{1} extract brand {2} Failed'.format(site, product.key, crawled_brand))

    def __extract_tag(self, tag_complete, text_list, product, flags, site):
        if tag_complete:
            return

        favbuy_tag = self.__extractor.extract( '\n'.join(text_list).encode('utf-8') )
        product.favbuy_tag = favbuy_tag
        product.tag_complete = bool(favbuy_tag)

        if product.tag_complete:
            flags['favbuy_tag'] = True
            product.update_history['favbuy_tag'] = datetime.utcnow()
            logger.info('{0}.product.{1} extract tag OK -> {2}'.format(site, product.key, product.favbuy_tag))
        else:
            logger.warning('{0}.product.{1} extract tag Failed'.format(site, product.key))

    def __extract_dept(self, dept_complete, text_list, product, flags, site):
        if dept_complete:
            return

        favbuy_dept = classify_product_department(site, product)
        product.favbuy_dept = favbuy_dept
        product.dept_complete = True # bool(favbuy_dept)

        if product.dept_complete:
            product.update_history['favbuy_dept'] = datetime.utcnow()
            flags['favbuy_dept'] = True
            logger.info('{0}.product.{1} extract dept OK -> {2}'.format(site, product.key, product.favbuy_dept))
        else:
            logger.error('{0}.product.{1} extract dept Failed'.format(site, product.key))

        # I don't know where to add this statement, \
        # just ensure that it'll be executed once when the product is crawled at the first time.
        self.__extract_text(product)

    def extract_text(self, args=(), kwargs={}):
        """
        To extract product brand, tag, dept.
        """
        site        =   kwargs.get('site', '')
        key         =   kwargs.get('key', '')
        product     =   self.__m[site].Product.objects(key=key).first()

        if not product:
            logger.error('{0}.product extract text failed: no key {1} '.format(site, key))
            return

        title           =   product.title
        brand_complete  =   product.brand_complete
        tag_complete    =   product.tag_complete
        dept_complete   =   product.dept_complete

        flags = {
            'favbuy_brand': False,    # To indicate whether changes occur on brand extraction.
            'favbuy_tag': False,      # To indicate whether changes occur on tag extraction.
            'favbuy_dept': False,     # To indicate whether changes occur on dept classification.
            'favbuy_price': False,
            'favbuy_listprice': False,
        }  

        text_list = []
        text_list.append(product.title or u'')
        text_list.extend(product.list_info or [])
        text_list.append(product.summary or u'')
        text_list.append(product.short_desc or u'')
        text_list.extend(product.tagline or [])
        
        jobs = [
            gevent.spawn(self.__extract_brand, brand_complete, product, flags, site),
            gevent.spawn(self.__extract_tag, tag_complete, text_list, product, flags, site),
            gevent.spawn(self.__extract_dept, dept_complete, text_list, product, flags, site),
            gevent.spawn(self.__extract_price, product, flags)
        ]
        gevent.joinall(jobs)

        # For updating event propagation, we should put some info back to the rpc caller.
        res = {}
        fields = [key for key in flags if flags[key]]
        if fields:
            product.save()

            res['event_id'] = product.event_id or []
            res['fields'] = {}
            for field in fields:
                # Do this so that product's favbuy_dept won't affect event's.
                if field == 'favbuy_dept':
                    continue
                res['fields'][field] = getattr(product, field)
        
        logger.debug('text server extract res -> {0}'.format(res))
        return res
    
    def propagate(self, args=(), kwargs={}):
        site = kwargs.get('site')
        event_id = kwargs.get('event_id')
        p = Propagator(site, event_id, module=self.__m[site])
        if p.propagate():
            logger.info('{0}.event.{1} propagation OK'.format(site, event_id))
            # interval = datetime.utcnow().replace(second=0, microsecond=0)
            # Stat.objects(site=site, doctype='event', interval=interval).update(inc__prop_num=1, upsert=True)
        else:
            logger.error('{0}.event.{1} propagation failed'.format(site, event_id))

def parse_price(price):
    if not price:
        return 0.

    amount = 0.
    pattern = re.compile(r'^[^\d]*(\d+(,\d{3})*(\.\d+)?)')
    match = pattern.search(price)
    if match:
        amount = (match.groups()[0]).replace(',', '')
    return float(amount)

@brand_refresh.bind
def rebulid_brand_index(sender, **kwargs):
    _extracter.rebuild_index()

if __name__ == '__main__':
    #ts = TextServer()
    #print ts.extract_text(kwargs=dict(site='myhabit', key='B0012MIAX4'))
    #exit(0)
    import os, sys
    port = TEXT_PORT if len(sys.argv) != 2 else int(sys.argv[1])
    zs = zerorpc.Server(TextServer(), pool_size=50, heartbeat=None) 
    zs.bind("tcp://0.0.0.0:{0}".format(port))
    zs.run()

