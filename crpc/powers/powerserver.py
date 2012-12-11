# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
from gevent.coros import Semaphore
import zerorpc

from boto.s3.connection import S3Connection
from settings import POWER_PORT
from configs import *

from tools import ImageTool, Propagator
from brandapi import Extracter
from powers.events import *

#process_image_lock = Semaphore(1)

class PowerServer(object):
    def __init__(self):
        self.__s3conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)

    def process_image(self, args=(), kwargs={}):
        print 'Image Server Accept', args, kwargs
        return self._process_image(*args, **kwargs)
    
    def _process_image(self, site, image_urls, ctx, doctype,  **kwargs):
        """ doctype is either ``event`` or ``product`` """
        key = kwargs.get('event_id', kwargs.get('key'))
        m = __import__("crawlers."+site+'.models', fromlist=['Event', 'Product'])

        image_tool = ImageTool(connection=self.__s3conn)
        image_tool.crawl(image_urls, site, doctype, key, thumb=True)
        image_path = image_tool.image_path

        if image_tool.image_complete:
            if doctype.capitalize() == 'Event':
                m.Event.objects(event_id=key).update(set__image_path=image_path, set__image_complete=True)
            elif doctype.capitalize() == 'Product':
                m.Product.objects(key=key).update(set__image_path=image_path, set__image_complete=True)
            image_crawled.send(sender=ctx, site=site, key=key, model=doctype.capitalize(), num=len(image_path))
        else:
            # TODO image_crawled_failed or need try except
            pass

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

        #TO REMOVE
        print 'brand extracting ---> ', site,' ' + doctype + ' ',  key # + ' ', 'brand-<'+crawled_brand+'>  ',  'title-<'+ kwargs.get('title', ' ') +'>'+ ':'
        
        print 'import  ', 'crawlers.'+site+'.models', 'doctype:', doctype.capitalize()
        m = __import__('crawlers.'+site+'.models', fromlist=[doctype.capitalize()])
        extracter = Extracter()
        brand = extracter.extract(crawled_brand)

        if brand:
            if doctype == 'Product':
                m.Product.objects(key=key).update(set__favbuy_brand=brand, set__brand_complete=True)
                kwargs['favbuy_brand'] = brand
                # brand_extracted.send('%s_%s_%s_brand' % (site, doctype, key), **kwargs)
        else:
            if doctype == 'Product':
                m.Product.objects(key=key).update(set__brand_complete=False)
                # brand_extracted_failed.send('%s_%s_%s_brand' % (site, doctype, key), **kwargs)

    def propagate(self, args=(), kwargs={}):
        site = kwargs.get('site')
        event_id = kwargs.get('event_id')
        p = Propagator(site, event_id)
        if p.propagate():
            pass
            # TODO send scuccess signal
        else:
            pass
            # TODO send fail signal


def test():
    pass

if __name__ == '__main__':
    import os, sys
    port = POWER_PORT if len(sys.argv) != 2 else int(sys.argv[1])
    zs = zerorpc.Server(PowerServer(), pool_size=50, heartbeat=None) 
    zs.bind("tcp://0.0.0.0:{0}".format(port))
    zs.run()

