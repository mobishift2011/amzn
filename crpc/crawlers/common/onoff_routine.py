#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import random
from datetime import datetime
from gevent.pool import Pool

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
        for site in picked_crawlers:
            get_site_module.mod[site] = __import__("crawlers.{0}.models".format(site), fromlist=['Event', 'Category', 'Product'])

    return get_site_module.mod[site]


def spout_obj(site, method):
    """ """
    m = get_site_module(site)
    if method == 'check_onsale_product':
        obj = m.Product.objects(products_end__gt=datetime.utcnow()).timeout(False)
        print '{0} have {1} on sale products.'.format(site, obj.count())

    elif method == 'check_offsale_product':
        obj = m.Product.objects(products_end__lt=datetime.utcnow()).timeout(False)
        print '{0} have {1} off sale products.'.format(site, obj.count())

    elif method == 'check_offsale_event':
        if not hasattr(m, 'Event'):
            return
        obj = m.Event.objects(events_end__lt=datetime.utcnow()).timeout(False)
        print '{0} have {1} events end.'.format(site, obj.count())

    for o in obj:
        yield o

def call_rpc(rpc, site, method, obj):
    try:
        rpc.run_cmd(site, method, obj)
    except Exception as e:
        print 'RPC call error: {0}'.format(e.message)


def checkout(site, method, concurrency=10):
    """ """
    rpcs = get_rpcs()
    pool = Pool(len(rpcs) * concurrency)
    ret = spout_obj(site, method)
    if ret is False:
        return
    for obj in ret:
        rpc = random.choice(rpcs)
        pool.spawn(call_rpc, rpc, site, method, obj)
    pool.join()


if __name__ == '__main__':
    checkout('onekingslane', 'check_onsale_product')
#    checkout('onekingslane', 'check_offsale_product')
#    checkout('onekingslane', 'check_offsale_event')
