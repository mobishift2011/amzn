# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
from gevent.coros import Semaphore
import zerorpc

from boto.s3.connection import S3Connection
from settings import POWER_PORT
from configs import *

from tools import ImageTool
from powers.events import *

from helpers.log import getlogger
logger = getlogger('powerserver', filename='/tmp/powerserver.log')

#process_image_lock = Semaphore(1)

class PowerServer(object):
    def __init__(self):
        self.__s3conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)

    def process_image(self, args=(), kwargs={}):
        logger.info('Image Server Accept -> {0} {1}'.format(args, kwargs))
        return self._process_image(*args, **kwargs)
    
    def _process_image(self, site, doctype, image_urls,  **kwargs):
        """ doctype is either ``event`` or ``product`` """
        key = kwargs.get('event_id', kwargs.get('key'))
        m = __import__("crawlers."+site+'.models', fromlist=['Event', 'Product'])

        instance = None
        if doctype.capitalize() == 'Event':
            instance = m.Event.objects(event_id=key).first()
        elif doctype.capitalize() == 'Product':
            instance = m.Product.objects(key=key).first()

        if instance and instance.image_complete == False:
            logger.info('crawling image of {0}.{1}.{2}'.format(site, doctype, key))
            image_tool = ImageTool(connection=self.__s3conn)
            image_tool.crawl(image_urls, site, doctype, key, thumb=True)
            image_path = image_tool.image_path  

            if image_tool.image_complete:
                instance.update(set__image_path=image_path, set__image_complete=True)
            else:
                logger.error('crawling image of {0}.{1}.{2} failed'.format(site, doctype, key))
               # TODO image_crawled_failed or need try except
                pass


if __name__ == '__main__':
    import os, sys
    port = POWER_PORT if len(sys.argv) != 2 else int(sys.argv[1])
    zs = zerorpc.Server(PowerServer(), pool_size=50, heartbeat=None) 
    zs.bind("tcp://0.0.0.0:{0}".format(port))
    zs.run()
