# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()
from gevent.pool import Pool
import gevent
from mongoengine import Q

from settings import TEXT_PEERS
from helpers.rpc import get_rpcs
from crawlers.common.routine import get_site_module

import traceback
from datetime import datetime
import random

from helpers.log import getlogger
logger = getlogger('dealroutine', filename='/tmp/deals.log')


def call_rpc(rpc, method, *args, **kwargs):
    try:
        return getattr(rpc, method)(args, kwargs)
    except Exception as e:
        logger.error('call rpc error: {0}'.format(traceback.format_exc()))
        print traceback.format_exc()


def spout_products(site):
    now = datetime.utcnow()
    products = get_site_module(site).Product.objects(Q(products_end__gt=now) | Q(products_end__exists=False) | Q(products_end=None))
    for product in products:
        yield {
            'site': site,
            'key': product.key
        }


def clean_product(site, concurrency=3):
    rpcs = get_rpcs(TEXT_PEERS)
    pool = Pool(len(rpcs)*concurrency)
    products = spout_products(site)

    for product in products:
        rpc = random.choice(rpcs)
        product['product_type'] = 'deal'
        pool.spawn(call_rpc, rpc, 'process_product', **product)
    pool.join()

if __name__ == '__main__':
    import sys
    clean_product(sys.argv[1]) 
