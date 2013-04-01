# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import gevent
import zerorpc

from settings import TEXT_PORT, CRPC_ROOT
from backends.matching.extractor import Extractor
from brandapi import Extracter
from pipelines import EventPipeline, ProductPipeline
from deals.pipelines import ProductPipeline as DealProductPipeline
from backends.monitor.models import Stat

from powers.events import brand_refresh
from crawlers.common.stash import picked_crawlers
from datetime import datetime
from os import listdir
from os.path import join, isdir

from helpers.log import getlogger
logger = getlogger('textserver', filename='/tmp/textserver.log')

_extracter =  Extracter() 

class TextServer(object):
    def __init__(self):
        # brand extracter
        if not hasattr(ProductPipeline, 'extracter'):
            setattr(ProductPipeline, 'extracter', _extracter)

        # tag extractor
        if not hasattr(ProductPipeline, 'extractor'):
            setattr(ProductPipeline, 'extractor', Extractor())         

        self.__m = {}
        
        # for name in listdir(join(CRPC_ROOT, "crawlers")):
        #     path = join(CRPC_ROOT, "crawlers", name)
        #     if name not in exclude_crawlers and isdir(path):
        #         self.__m[name] = __import__("crawlers."+name+'.models', fromlist=['Event', 'Product'])

        for name in picked_crawlers:
            self.__m[name] = __import__("crawlers."+name+'.models', fromlist=['Event', 'Product'])
    
    def process_product(self, args=(), kwargs=()):
        site = kwargs.get('site')
        key = kwargs.get('key')

        if not site:
            return

        product = self.__m[site].Product.objects(key=key).first()
        if not product:
            logger.warning('process product not exists -> {0}'.format(kwargs))

        pp = DealProductPipeline(site, product) if kwargs.get('product_type') == 'deal' else ProductPipeline(site, product)
        if pp.clean():
            product.save()

    def propagate(self, args=(), kwargs={}):
        site = kwargs.get('site')
        event_id = kwargs.get('event_id')

        if not site:
            return

        event = self.__m[site].Event.objects(event_id=event_id).first()
        if not event:
            logger.warning('propagate event not exists -> {0}'.format(kwargs))

        p = EventPipeline(site, event)

        # For uppcoming events, do nothing with propagation but something with text processing.
        if event.events_begin and event.events_begin > datetime.utcnow():
            if p.extract_text():
                event.save()
            return

        products = self.__m[site].Product.objects(event_id=event.event_id)
        
        if event.propagation_complete:
            if p.propagate(products):
                logger.info('event propagation updated -> {0}'.format(kwargs))
        else:
            if p.propagate(products):
                logger.info('event propagated -> {0}'.format(kwargs))
                interval = datetime.utcnow().replace(second=0, microsecond=0)
                Stat.objects(site=site, doctype='event', interval=interval).update(inc__prop_num=1, upsert=True)             
            else:
                logger.error('event propagation failed -> {0}'.format(kwargs))


@brand_refresh.bind
def rebulid_brand_index(sender, **kwargs):
    _extracter.rebuild_index()


if __name__ == '__main__':
    import os, sys
    port = TEXT_PORT if len(sys.argv) != 2 else int(sys.argv[1])
    zs = zerorpc.Server(TextServer(), pool_size=50, heartbeat=None) 
    zs.bind("tcp://0.0.0.0:{0}".format(port))
    zs.run()
