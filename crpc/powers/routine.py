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
from configs import SITES
from events import *

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

def call_rpc(rpc, method, *args, **kwargs):
    try:
        from crawlers.common.rpcserver import RPCServer
#        RPCServer().image(method, args, kwargs)
        m = __import__("powers.server", fromlist=['Image'])
        service = m.Image()
        if service:
            return getattr(service, method)(*args, **kwargs)
        else:
            raise ValueError("{crawler} does not seems to a valid crawler".format(**locals()))
#        rpc.image(method, args, kwargs)
    except Exception:
        print traceback.format_exc()
        image_crawled_failed.send(sender=kwargs['ctx'],
                            site = kwargs['ctx'],
                            key = kwargs.get('key') or kwargs.get('event_id'),
                            url = kwargs.get('url'),
                            reason = traceback.format_exc()
                            )

def get_site_module(site):
    return __import__("crawlers."+site+'.models', fromlist=['Event', 'Product'])

def spout_event_images(site):
    m = get_site_module(site)
    events = m.Event.objects(urgent=False, image_complete=False)
    for event in events:
        yield {
            'site': site,
            'event_id': event.event_id,
            'image_urls': event.image_urls,
        }

def spout_product_images(site):
    m = get_site_module(site)
    products = m.Product.objects(updated=True, image_complete=False)
    for product in products:
        yield {
            'site': site,
            'key': product.key,
            'image_urls': product.image_urls
        }

class UpdateContext(object):
    """ the context manager for monitoring 
        
    wraps tedious signals passing inside the context manager
    
    Usage:

    >>> with MonitorContext(site='amazon', method='update_category'):
    ...     pass # do something related to site and method

    """
    def __init__(self, site, method):
        self.site = site
        self.method = method
        self.sender = "{0}.{1}.{2}".format(self.site, self.method, uuid.uuid4().hex)
    
    def __enter__(self):
        pre_image_crawl.send(sender = self.sender,
                                    site = self.site,
                                    method = self.method)
        return self.sender

    def __exit__(self, exc_type, exc_value, exc_traceback):
        complete = True
        reason = ''
        if exc_type:
            complete = False
            reason = ''.join(traceback.format_tb(exc_traceback))+'{0!r}'.format(exc_value)
        
        post_image_crawl.send(sender = self.sender,
                                    site = self.site,
                                    method = self.method,
                                    complete = complete,
                                    reason = reason)

def scan_event_images(site, rpc, concurrency=3):
    with UpdateContext(site, 'crawl_event_images') as ctx:
        rpcs = [rpc] if not isinstance(rpc, list) else rpc
        pool = Pool(len(rpcs)*concurrency)
        for kwargs in spout_event_images(site):
            kwargs['ctx'] = ctx
            rpc = random.choice(rpcs)
            pool.spawn(call_rpc, rpc, 'crawl_event_images', **kwargs)
        pool.join()

def scan_product_images(site, rpc, concurrency=3):
    with UpdateContext(site, 'crawl_product_images') as ctx:
        rpcs = [rpc] if not isinstance(rpc, list) else rpc
        pool = Pool(len(rpcs)*concurrency)
        for kwargs in spout_product_images(site):
            kwargs['ctx'] = ctx
            rpc = random.choice(rpcs)
            pool.spawn(call_rpc, rpc, 'crawl_product_images', **kwargs)
        pool.join()

def crawl_images(site, model, key, rpc=None, concurrency=3):
    if rpc is None:
        rpc = get_rpcs()
    
    kwargs = {}
    method = 'crawl_%s_images' % model.lower() if model else None
    with UpdateContext(site, method) as ctx:
        m = __import__("crawlers."+site+'.models', fromlist=['Event', 'Product'])
        if model == 'Event':
            event = m.Event.objects.get(event_id=key)
            if event and not event.image_complete:
                kwargs.__setitem__('site', site)
                kwargs.__setitem__('event_id', event.event_id)
                kwargs.__setitem__('image_urls', event.image_urls)
                kwargs.__setitem__('ctx', ctx)
        elif model == 'Product':
            product = m.Product.objects.get(key=key)
            if product and not product.image_complete:
                kwargs.__setitem__('site', site)
                kwargs.__setitem__('key', product.key)
                kwargs.__setitem__('image_urls', product.image_urls)
                kwargs.__setitem__('ctx', ctx)
        
        if kwargs and method:
            rpcs = [rpc] if not isinstance(rpc, list) else rpc
            rpc = random.choice(rpcs)
            call_rpc(rpc, method, **kwargs)
