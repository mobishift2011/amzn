# -*- coding: utf-8 -*-
from tools import ImageTool

class Image(object):
    def crawl_event_images(self, site, event_id, image_urls):
        m = __import__("crawlers."+site+'.models', fromlist=['Event'])
        event = m.Event.objects.get(event_id=event_id)
        if event:
            it = ImageTool()
            s3_urls = it.crawl(image_urls, site, event_id)
            event.image_path = s3_urls
            event.save()
            print '\n%s.%s.s3urls: %s' % (site, event_id, s3_urls)
        else:
            # TODO
            pass
    
    def crawl_product_images(self, site, key, image_urls):
        m = __import__("crawlers."+site+'.models', fromlist=['Product'])
        product = m.Product.objects.get(key=key)
        if product:
            it = ImageTool()
            s3_urls = it.crawl(image_urls, site, key)
            product.image_path = s3_urls
            product.save()
            print '\n%s.%s.s3urls: %s' % (site, key, s3_urls)
        else:
            # TODO
            pass