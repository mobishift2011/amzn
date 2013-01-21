# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
from gevent.coros import Semaphore
import zerorpc

from boto.s3.connection import S3Connection
from settings import POWER_PORT, CRPC_ROOT
from configs import *
from tools import ImageTool
from powers.events import *
from imglib import trim, scale
from models import Stat

from crawlers.common.stash import exclude_crawlers
from os import listdir
from os.path import join, isdir
from datetime import datetime

from helpers.log import getlogger
logger = getlogger('powerserver', filename='/tmp/powerserver.log')

#process_image_lock = Semaphore(1)

class PowerServer(object):
    def __init__(self):
        self.__s3conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
        self.__m = {}

        for name in listdir(join(CRPC_ROOT, "crawlers")):
            path = join(CRPC_ROOT, "crawlers", name)
            if name not in exclude_crawlers and isdir(path):
                self.__m[name] = __import__("crawlers."+name+'.models', fromlist=['Event', 'Product'])

    def process_image(self, args=(), kwargs={}):
        logger.debug('Image Server Accept -> {0} {1}'.format(args, kwargs))
        return self._process_image(*args, **kwargs)
    
    def _process_image(self, site, doctype, image_urls,  **kwargs):
        """ doctype is either ``event`` or ``product`` """
        key = kwargs.get('event_id', kwargs.get('key'))
        model = doctype.capitalize()
        sender = '{0}.{1}.{2}'.format(site, model, key)
        instance = None

        if model == 'Event':
            instance = self.__m[site].Event.objects(event_id=key).first()
        elif model == 'Product':
            instance = self.__m[site].Product.objects(key=key).first()

        if instance and instance.image_complete == False:
            logger.info('To crawl image of {0}'.format(sender))
            it = ImageTool(connection=self.__s3conn)
            try:
                it.crawl(image_urls, site, model, key, thumb=True)
            except Exception, e:
                logger.error('crawling image of {0} exception: {1}'.format(sender, str(e)))
                return

            if it.image_complete:
                instance.reload()
                if instance.image_complete:
                    return
                instance.image_path = it.image_path
                instance.image_complete = True
                instance.update_history.update({'image_path': datetime.utcnow()})
                instance.save()
                image_crawled.send(sender=sender, model=model, key=key)
                interval = datetime.utcnow().replace(second=0, microsecond=0)
                Stat.objects(site=site, doctype=doctype.lower(), interval=interval).update(inc__image_num=1, upsert=True)
            else:
                logger.error('crawling image of {0} failed'.format(sender))


if __name__ == '__main__':
    import os, sys
    port = POWER_PORT if len(sys.argv) != 2 else int(sys.argv[1])
    zs = zerorpc.Server(PowerServer(), pool_size=50, heartbeat=None) 
    zs.bind("tcp://0.0.0.0:{0}".format(port))
    zs.run()
    