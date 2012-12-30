# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import gevent
import zerorpc

from settings import TEXT_PORT, CRPC_ROOT
from backends.matching.extractor import Extractor
from backends.matching.classifier import FavbuyClassifier

from brandapi import Extracter
from tools import Propagator
from powers.events import *
from models import Stat

from crawlers.common.stash import exclude_crawlers
from datetime import datetime
from os import listdir
from os.path import join, isdir

from helpers.log import getlogger
logger = getlogger('textserver', filename='/tmp/textserver.log')


class TextServer(object):
    def __init__(self):
        self.__extracter = Extracter()  # brand extracter
        self.__extractor = Extractor()  # tag extractor
        self.__classifier = FavbuyClassifier()
        self.__classifier.load_from_database()
        self.__m = {}
        
        for name in listdir(join(CRPC_ROOT, "crawlers")):
            path = join(CRPC_ROOT, "crawlers", name)
            if name not in exclude_crawlers and isdir(path):
                self.__m[name] = __import__("crawlers."+name+'.models', fromlist=['Event', 'Product'])

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
            logger.info('{0}.product.{1} extract tag OK -> {2}'.format(site, product.key, product.favbuy_tag))
        else:
            logger.warning('{0}.product.{1} extract tag Failed'.format(site, product.key))

    def __extract_dept(self, dept_complete, text_list, product, flags, site):
        if dept_complete:
            return

        p = product
        depts = []
        depts.extend(p.dept)
        for eid in p.event_id:
            e = self.__m[site].Event.objects.get(event_id=eid)
            depts.extend( e.dept )
            if hasattr(e, 'short_desc'):
                depts.append( e.short_desc )

        content = u'==site==: ' + site + u'\n'
        if depts:
            content += u'==depts==: ' + u'; '.join(depts) + u'\n'
        if p.cats:
            content += u'==cats==: ' +  u'; '.join(p.cats) + u'\n'
        if p.brand:
            content += u'==brand==: ' + p.brand + u'\n'
        if p.tagline:
            content += u'==tagline==: ' + u'; '.join(p.tagline) + u'\n'
        content += u'==title==: ' +  p.title + u'\n'
        content += u'==listinfo==: ' + u'\n'.join(p.list_info)
        print content

        favbuy_dept = list(self.__classifier.classify( content ))
        product.favbuy_dept = favbuy_dept
        product.dept_complete = bool(favbuy_dept)

        if product.dept_complete:
            flags['favbuy_dept'] = True
            logger.info('{0}.product.{1} extract dept OK -> {2}'.format(site, product.key, product.favbuy_dept))
        else:
            logger.error('{0}.product.{1} extract dept Failed'.format(site, product.key))

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
            product.list_update_time = datetime.utcnow()
            product.save()

            res['event_id'] = product.event_id or []
            res['fields'] = {}
            for field in fields:
                res['fields'][field] = getattr(product, field)
        
        logger.debug('text server extract res -> {0}'.format(res))
        return res
    
    def propagate(self, args=(), kwargs={}):
        site = kwargs.get('site')
        event_id = kwargs.get('event_id')
        p = Propagator(site, event_id, self.__extractor, self.__classifier, module=self.__m[site])
        if p.propagate():
            logger.info('{0}.event.{1} propagation OK'.format(site, event_id))
            interval = datetime.utcnow().replace(second=0, microsecond=0)
            Stat.objects(site=site, doctype='event', interval=interval).update(inc__prop_num=1, upsert=True)
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


if __name__ == '__main__':
    #ts = TextServer()
    #print ts.extract_text(kwargs=dict(site='myhabit', key='B008UW2L7K'))
    #exit(0)
    import os, sys
    port = TEXT_PORT if len(sys.argv) != 2 else int(sys.argv[1])
    zs = zerorpc.Server(TextServer(), pool_size=50, heartbeat=None) 
    zs.bind("tcp://0.0.0.0:{0}".format(port))
    zs.run()

