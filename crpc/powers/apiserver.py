# -*- coding: utf-8 -*-
from settings import API_PORT

import zerorpc

from tools import ImageTool
from powers.events import image_crawled, image_crawled_failed
from powers.binds import image_crawled, image_crawled_failed

class APIServer(object):
    def process_image(self, args=(), kwargs={}):
        return self._process_image(*args, **kwargs)
    
    def _process_image(self, site, image_urls, ctx, doctype,  **kwargs):
        """ doctype is either ``event`` or ``product`` """
        key = kwargs.get('event_id', kwargs.get('key'))
        m = __import__("crawlers."+site+'.models', fromlist=['Event', 'Product'])
        if doctype == 'event':
            instance = m.Event.objects(event_id=key).first()
        elif doctype == 'product':
            instance = m.Product.objects(key=key).qfirst()

        if instance:
            it = ImageTool()
            image_path = it.crawl(image_urls, site, key)
            if len(image_path):
                instance.update(set__image_path = image_path)
                image_crawled.send(sender=ctx, site=site, key=key, model=doctype.capitalize(), num=len(instance.image_path))
        else:
            # TODO image_crawled_failed
            pass

def test():
    from crawlers.gilt.models import Event
    event = Event.objects().first()
    image_urls = event.image_urls
    site='gilt'
    ctx = site+event.event_id
    doctype = 'event'
    APIServer().process_image(site, image_urls, ctx, doctype, event_id=event.event_id)

if __name__ == '__main__':
    zs = zerorpc.Server(APIServer()) 
    zs.bind("tcp://0.0.0.0:{0}".format(API_PORT))
    zs.run()
