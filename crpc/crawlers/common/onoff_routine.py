#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import random
import traceback
from datetime import datetime
from gevent.pool import Pool
from mongoengine import Q

from crawlers.common.stash import picked_crawlers
from helpers.rpc import get_rpcs


def get_site_module(site):
    """.. :py:method::
    :param site: the site we crawled
    :rtype: module of site
    """
    if not hasattr(get_site_module, 'mod'):
        setattr(get_site_module, 'mod', {}) 

    if site not in get_site_module.mod:
        for crawler in picked_crawlers:
            get_site_module.mod[crawler] = __import__("crawlers.{0}.models".format(crawler), fromlist=['Event', 'Category', 'Product'])

    return get_site_module.mod[site]


def spout_obj(site, method):
    """ """
    m = get_site_module(site)
    if method == 'check_onsale_product':
        obj = m.Product.objects(Q(products_end__gt=datetime.utcnow()) | Q(products_end__exists=False)).timeout(False)
        print '{0} have {1} on sale event/category products.'.format(site, obj.count())
        for o in obj:
            yield {'id': o.key, 'url': o.combine_url}

#        if hasattr(m, 'Category'):
#            obj = m.Product.objects(products_end__exists=False).timeout(False)
#            print '{0} have {1} on sale category products.'.format(site, obj.count())
#            for o in obj:
#                yield {'id': o.key, 'url': o.combine_url}

    elif method == 'check_offsale_product':
        obj = m.Product.objects(products_end__lt=datetime.utcnow()).timeout(False)
        print '{0} have {1} off sale event products.'.format(site, obj.count())
        for o in obj:
            yield {'id': o.key, 'url': o.combine_url}

        if hasattr(m, 'Category'):
            obj = m.Product.objects(products_end__exists=False).timeout(False)
            print '{0} have {1} off sale category products.'.format(site, obj.count())
            for o in obj:
                yield {'id': o.key, 'url': o.combine_url}

    elif method == 'check_onsale_event':
        if not hasattr(m, 'Event'):
            return
        obj = m.Event.objects(Q(events_end__gt=datetime.utcnow()) | Q(events_end__exists=False)).timeout(False)
        print '{0} have {1} on sale events.'.format(site, obj.count())

        for o in obj:
            yield {'id': o.event_id, 'url': o.combine_url}

    elif method == 'check_offsale_event':
        if not hasattr(m, 'Event'):
            return
        obj = m.Event.objects(events_end__lt=datetime.utcnow()).timeout(False)
        print '{0} have {1} off sale events.'.format(site, obj.count())

        for o in obj:
            yield {'id': o.event_id, 'url': o.combine_url}


def call_rpc(rpc, site, method, *args, **kwargs):
    try:
        rpc.run_cmd(site, method, args, kwargs)
    except Exception as e:
        print 'RPC call error: {0}'.format(traceback.format_exc())


def checkout(site, method, concurrency=10):
    """ """
    rpcs = get_rpcs()
#    rpcs = get_rpcs([{'host_string':'root@127.0.0.1', 'port':8899}])
    pool = Pool(len(rpcs) * concurrency)
    ret = spout_obj(site, method)
    if ret is False:
        return
    for kwargs in ret:
        rpc = random.choice(rpcs)
        pool.spawn(call_rpc, rpc, site, method, **kwargs)
    pool.join()


if __name__ == '__main__':

# call that can change the crpc/mastiff database
    checkout('onekingslane', 'check_onsale_event')
    checkout('onekingslane', 'check_onsale_product')

    checkout('ruelala', 'check_onsale_product')

    checkout('bluefly', 'check_onsale_product')

    checkout('lot18', 'check_onsale_product')
