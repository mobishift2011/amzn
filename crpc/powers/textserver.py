# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import zerorpc

from settings import TEXT_PORT, CRPC_ROOT
from backends.matching.extractor import Extractor
from backends.matching.classifier import SklearnClassifier

from brandapi import Extracter
from tools import Propagator
from powers.events import *

from crawlers.common.stash import exclude_crawlers
from os import listdir
from os.path import join, isdir

from helpers.log import getlogger
logger = getlogger('textserver', filename='/tmp/textserver.log')

#process_image_lock = Semaphore(1)

class TextServer(object):
    def __init__(self):
        self.__extracter = Extracter()  # brand extracter
        self.__extractor = Extractor()  # tag extractor
        self.__classifier = SklearnClassifier()
        self.__classifier.load_from_database()
        self.__m = {}
        
        for name in listdir(join(CRPC_ROOT, "crawlers")):
            path = join(CRPC_ROOT, "crawlers", name)
            if name not in exclude_crawlers and isdir(path):
                self.__m[name] = __import__("crawlers."+name+'.models', fromlist=['Event', 'Product'])

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
        }  

        if not brand_complete:
            crawled_brand = product.brand
            brand = self.__extracter.extract(crawled_brand) or \
                        self.__extracter.extract(title)
            if brand:
                product.update(set__favbuy_brand=brand, set__brand_complete=True)
                flags['favbuy_brand'] = True
                logger.info('{0}.product.{1} extract brand {2} -> {3} OK'.format(site, key, crawled_brand, brand))
                # TODO send scuccess signal
            else:
                product.update(set__brand_complete=False)
                logger.warning('{0}.product.{1} extract brand {2} failed'.format(site, key, crawled_brand))
                # TODO send fail signal

        text_list = []
        if not tag_complete:
            text_list.append(product.title or '')
            text_list.extend(product.list_info or [])
            text_list.append(product.summary or '')
            text_list.append(product.short_desc or '')
            text_list.extend(product.tagline or [])
            favbuy_tag = self.extractor.extract( '\n'.join(text_list).encode('utf-8') )
            product.update(set__favbuy_tag = favbuy_tag, set__tag_complete=bool(favbuy_tag))

            if product.tag_complete:
                flags['favbuy_tag'] = True
            else:
                logger.info('{0}.product.{1} extract tag failed'.format(site, key))
        
        if not dept_complete:
            text_list.extend(product.dept)
            favbuy_dept = list(self.classifier.classify( '\n'.join(text_list) ))
            product.update(set__favbuy_dept = favbuy_dept, set__dept_complete=bool(favbuy_dept))

            if product.dept_complete:
                flags['favbuy_dept'] = True
            else:
                logger.info('{0}.product.{1} extract dept failed'.format(site, key))

        # for updating product publish
        res = {}
        fields = [key for key in flags if flags[key]]
        if fields:
            common_saved.send(sender=None, obj_type='Product', key=product.key, url=product.combine_url, \
                is_new=false, is_updated=True, fields=fields)

            res['event_id'] = product.event_id or []
            res['fields'] = {}
            for field in fields:
                res['fields'][field] = getattr(product, field)

        # for updating event propagation
        return res

    def propagate(self, args=(), kwargs={}):
        site = kwargs.get('site')
        event_id = kwargs.get('event_id')
        p = Propagator(site, event_id, self.__extractor, self.__classifier)
        if p.propagate():
            logger.info('{0}.{1} propagation OK'.format(site, event_id))
            # TODO send scuccess signal
        else:
            logger.error('{0}.{1} propagation failed'.format(site, event_id))
            # TODO send fail signal


if __name__ == '__main__':
    import os, sys
    port = TEXT_PORT if len(sys.argv) != 2 else int(sys.argv[1])
    zs = zerorpc.Server(TextServer(), pool_size=50, heartbeat=None) 
    zs.bind("tcp://0.0.0.0:{0}".format(port))
    zs.run()

