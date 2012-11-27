# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
from settings import POWER_PORT

import zerorpc
from gevent.coros import Semaphore

from tools import ImageTool
from brandAPI import APIClient
from powers.events import image_crawled, image_crawled_failed
from powers.binds import image_crawled, image_crawled_failed

#process_image_lock = Semaphore(1)

class PowerServer(object):
    def process_image(self, args=(), kwargs={}):
        print 'accept', args, kwargs
        return self._process_image(*args, **kwargs)
    
    def _process_image(self, site, image_urls, ctx, doctype,  **kwargs):
        """ doctype is either ``event`` or ``product`` """
        key = kwargs.get('event_id', kwargs.get('key'))
        m = __import__("crawlers."+site+'.models', fromlist=['Event', 'Product'])
        image_tool = ImageTool()
        image_path = image_tool.crawl(image_urls, site, key)
        if len(image_path):

            if doctype == 'event':
                m.Event.objects(event_id=key).update(set__image_path=image_path)
            elif doctype == 'product':
                m.Product.objects(key=key).update(set__image_path=image_path)
            image_crawled.send(sender=ctx, site=site, key=key, model=doctype.capitalize(), num=len(image_path))
        else:
            # TODO image_crawled_failed or need try except
            pass

    def extract_brand(self, args=(), kwargs={}):
        site = kwargs.get('site', '')
        doctype = kwargs.get('doctype', '').capitalize()
        key = kwargs.get('key', '')
        brand = kwargs.get('brand') or ''
        title = kwargs.get('title', '')

        # TO REMOVE
        import time
        print site,'  ' + doctype + '  ',  key + '<'+brand+'>  ',  '<'+ title +'>'+ ':'

        brand = APIClient.brand.match(brand, title)
        if brand:
            m = __import__('crawlers.'+site+'.models', fromlist=[doctype])
            if doctype == 'Event'
                m.Event.objects(event_id=key).update(set__favbuy_brand=brand, set__complete_status=1)
            elif doctype == 'Product'
                m.Product.objects(key=key).update(set__favbuy_brand=brand, set__complete_status=1)

            # TODO send a signal to inform the success of brand extract

        # TODO set the brand back to the data object in db for cleaning.

def test():
    from crawlers.gilt.models import Event
    event = Event.objects().first()
    image_urls = event.image_urls
    site='gilt'
    ctx = site+event.event_id
    doctype = 'event'
    APIServer().process_image(site, image_urls, ctx, doctype, event_id=event.event_id)

if __name__ == '__main__':
    zs = zerorpc.Server(PowerServer()) 
    zs.bind("tcp://0.0.0.0:{0}".format(POWER_PORT))
    zs.run()
