# -*- coding: utf-8 -*-
from powers.events import *
from powers.routine import get_rpcs, scan_event_images, scan_product_images
from powers.models import EventProgress, ProductProgress

from datetime import datetime

from gevent import monkey; monkey.patch_all()
import gevent

from helpers.log import getlogger
logger = getlogger("crawlerImageLog")

@run_image_crawl.bind
def image_crawl(sender, **kwargs):
    site = kwargs.get('site')
    method = kwargs.get('method')
    
    if site and method:
        logger.info('start to get rpc resource for %s.%s' % (site, method))
        gevent.spawn(globals()[method], site, get_rpcs(), 10) #.rawlink(partial(task_completed, site=site, method=method))

@pre_image_crawl.bind
def stat_pre_general_update(sender, **kwargs):
    pass

@post_image_crawl.bind
def stat_post_general_update(sender, **kwargs):
    pass

@image_crawled_failed.bind
def stat_failed(sender, **kwargs):
    pass

@image_crawled.bind
def stat_save(sender, **kwargs):
    logger.debug('{0} -> {1}'.format(sender,kwargs.items()))
    site = kwargs.get('site', '')
    key = kwargs.get('key', '')
    model = kwargs.get('model', '')
    num = kwargs.get('num', '')
    
    print '{0}.{1}.{2}.crawled_image_num:{3}'.format(site, key, model, num)
    try:
        m = __import__("crawlers."+site+'.models', fromlist=['Event', 'Product'])
        entity = None
        if model == 'Event':
            progress = EventProgress.objects(site=site, key=key)
            if not progress: progress = EventProgress(site=site, key=key)
            entity = m.Event.objects.get(event_id=key)
            
        elif model == 'Product':
            progress = ProductProgress.objects(site=site, key=key)
            if not progress: progress = EventProgress(site=site, key=key)
            entity = m.Product.objects.get(key=key)
        
        if progress:
            progress.image_complete = True
            progress.num_image = num
            progress.updated_at = datetime.utcnow()
            progress.save()
            
            # to ensure the event or product flag is indicated after the progress has been done.
            if entity:
                entity.image_complete = True
                entity.save()
    
    except Exception as e:
        logger.exception(e.message)
