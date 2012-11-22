# -*- coding: utf-8 -*-
from tools import ImageTool
from powers.events import image_crawled, image_crawled_failed
from powers.binds import image_crawled, image_crawled_failed

class Image(object):
    def crawl_event_images(self, site, event_id, image_urls, ctx):
        m = __import__("crawlers."+site+'.models', fromlist=['Event'])
        event = m.Event.objects(event_id=event_id)
        if event:
            it = ImageTool()
            event.image_path = it.crawl(image_urls, site, event_id)
            event.save()
            
            image_crawled.send(sender=ctx, site=site, key=event_id, model='Event', num=len(event.image_path))
        else:
            # TODO image_crawled_failed
            pass
    
    def crawl_product_images(self, site, key, image_urls, ctx):
        m = __import__("crawlers."+site+'.models', fromlist=['Product'])
        product = m.Product.objects(key=key)
        if product:
            it = ImageTool()
            product.image_path = it.crawl(image_urls, site, key)
            product.save()
                 
            image_crawled.send(sender=ctx, site=site, key=key, model='Product', num=len(product.image_path))
        else:
            # TODO image_crawled_failed
            pass
