# -*- coding: utf-8 -*-
from tools import ImageTool
from powers.events import image_crawled, image_crawled_failed
from powers.binds import image_crawled, image_crawled_failed
    
def crawl_images(site, image_urls, ctx, doctype,  **kwargs):
    """ doctype is either ``event`` or ``product`` """
    key = kwargs.get('event_id', kwargs.get('key'))
    m = __import__("crawlers."+site+'.models', fromlist=['Event', 'Product'])
    if doctype == 'event':
        instance = m.Event.objects(event_id=key).first()
    elif doctype == 'product':
        instance = m.Product.objects(key=key).first()

    if instance:
        it = ImageTool()
        instance.update(set__image_path=it.crawl(image_urls, site, key))
            
        image_crawled.send(sender=ctx, site=site, key=key, model=doctype.capitalize(), num=len(instance.image_path))
    else:
        # TODO image_crawled_failed
        pass
