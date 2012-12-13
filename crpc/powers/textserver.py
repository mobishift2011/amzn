# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import zerorpc

from settings import TEXT_PORT
from backends.matching.extractor import Extractor
from backends.matching.classifier import SklearnClassifier

from brandapi import Extracter
from tools import Propagator
from powers.events import *

from helpers.log import getlogger
logger = getlogger('textserver', filename='/tmp/textserver.log')

#process_image_lock = Semaphore(1)

class TextServer(object):
    def __init__(self):
        self.__extracter = Extracter()  # brand extracter
        self.__extractor = Extractor()  # tag extractor
        self.__classifier = SklearnClassifier()
        self.__classifier.load_from_database()

    def extract_brand(self, args=(), kwargs={}):
        """
        @param: kwargs contains several keys as followed:
        * site
        * key
        * title
        * brand
        * doctype
        * combine_url
        """
        site = kwargs.get('site', '')
        doctype = kwargs.get('doctype', '')
        key = kwargs.get('key', '')
        crawled_brand = kwargs.get('brand') or ''

        brand = self.__extracter.extract(crawled_brand)
        m = __import__('crawlers.'+site+'.models', fromlist=[doctype.capitalize()])
        if brand:
            if doctype == 'Product':
                m.Product.objects(key=key).update(set__favbuy_brand=brand, set__brand_complete=True)
                logger.info('{0} {1} {2} extract brand {3} OK---> {4}'.format(site, doctype, key, crawled_brand, brand))
                # TODO send scuccess signal
        else:
            if doctype == 'Product':
                m.Product.objects(key=key).update(set__brand_complete=False)
                logger.warning('{0} {1} {2} extract brand {3} failed'.format(site, doctype, key, crawled_brand))
                # TODO send fail signal

    def propagate(self, args=(), kwargs={}):
        site = kwargs.get('site')
        event_id = kwargs.get('event_id')
        p = Propagator(site, event_id, self.__extractor, self.__classifier)
        if p.propagate():
            logger.info('{0} {1} {2} extract brand {3} OK---> {4}'.format(site, doctype, key, crawled_brand, brand))
            # TODO send scuccess signal
        else:
            logger.warning('{0} {1} {2} extract brand {3} failed'.format(site, doctype, key, crawled_brand))
            # TODO send fail signal


if __name__ == '__main__':
    import os, sys
    port = TEXT_PORT if len(sys.argv) != 2 else int(sys.argv[1])
    zs = zerorpc.Server(TextServer(), pool_size=50, heartbeat=None) 
    zs.bind("tcp://0.0.0.0:{0}".format(port))
    zs.run()

