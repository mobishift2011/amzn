# -*- coding: utf-8 -*-
from powers.events import *
from powers.routine import get_rpcs, update_event_images, update_product_images

from gevent import monkey; monkey.patch_all()
import gevent

@run_image_crawl.bind
def image_crawl(sender, **kwargs):
    site = kwargs.get('site')
    method = kwargs.get('method')
    
    print 'get rpc resource to %s.%s' % (site, method)
    if site and method:
        gevent.spawn(globals()[method], site, get_rpcs(), 10) #.rawlink(partial(task_completed, site=site, method=method))