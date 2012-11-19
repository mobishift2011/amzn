# -*- coding: utf-8 -*-
"""
crawlers.common.rpcserver
~~~~~~~~~~~~~~~~~~~~~~~~~

Provides a image processed workflow for all callers

"""

from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
import zerorpc
import uuid
import random
import traceback

from settings import PEERS, RPC_PORT
from configs import SITES, AWS_ACCESS_KEY, AWS_SECRET_KEY
from Image import ImageTool

def get_rpcs():
    if not hasattr(get_rpcs, '_cached_peers'):
        setattr(get_rpcs, '_cached_peers', [])

    if get_rpcs._cached_peers != PEERS: 
        setattr(get_rpcs, '_cached_peers', PEERS)

        rpcs = []
        for peer in PEERS:
            host = peer[peer.find('@')+1:]
            c = zerorpc.Client('tcp://{0}:{1}'.format(host, RPC_PORT), timeout=None)
            if c:
                rpcs.append(c)

        setattr(get_rpcs, '_cached_rpcs', rpcs)
        
    return get_rpcs._cached_rpcs

def call_rpc(rpc, site, method, *args, **kwargs):
    try:
        rpc.call(site, method, args, kwargs)
    except Exception, e:
        print e
#        common_failed.send(sender=kwargs['ctx'],
#                            site = site,
#                            key = kwargs.get('key') or kwargs.get('event_id'),
#                            url = kwargs.get('url'),
#                            reason = traceback.format_exc()
#                            )

def get_site_module(site):
    return __import__("crawlers."+site+'.models', fromlist=['Event', 'Product'])

def spout_image_events(site):
    m = get_site_module(site)
    events = m.Event.objects()  # TODO (image_done=False)
    for event in events:
        yield {
            'site': site,
            'event_id': event.event_id,
            'image_urls': event.image_urls,
        }

def spout_image_products(site):
    m = get_site_module(site)
    products = m.Product.objects()  # TODO (image_done=False)
    for product in products:
        yield {
            'site': site,
            'key': product.key,
            'image_urls': product.image_urls
        }

def update_event_images(site, rpc, concurrency=3):
    for event in spout_image_events(site):
        print event   # TODO rpc call to crawl image
    return  # TODO poll.join()

def update_product_images(site, rpc, concurrency=3):
    for product in spout_image_products(site):
        print product   # TODO rpc call to crawl image
    return  # TODO poll.join()

def update_images(site, rpcs, concurrency=3):
    rpcs = []
#            for s in self.get_schedules():
#                if s.timematch():
#                    execute(s.site, s.method)
#    if not task_already_running(site, method):
#        gevent.spawn(globals()[method], site, get_rpcs(), 10) \
#                .rawlink(partial(task_completed, site=site, method=method))

if __name__ == '__main__':
    pass
    rpcs = get_rpcs()
    for site in SITES:
        rpc = random.choice(rpcs)
        update_event_images(site, rpc)
        update_product_images(site, rpc)