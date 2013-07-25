#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>
import os
import time
import random
import traceback
from datetime import datetime, timedelta
from gevent.pool import Pool
from mongoengine import Q

from crawlers.common.stash import picked_crawlers
from helpers.rpc import get_rpcs

from crawlers.common.events import *
from backends.monitor.models import Fail

common_saved.bind('sync')
def do_nothing(*args, **kwargs):
    pass

common_failed.bind('sync')
def do_nothing(*args, **kwargs):
    pass

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


def spout_obj(site, method, full=False):
    """ if full, spout full, else elimite which have been recently updated in list updating"""
    m = get_site_module(site)
    if method == 'check_onsale_product':
        if not full:
            obj = m.Product.objects( (Q(products_end__gt=datetime.utcnow()) | Q(products_end__exists=False)) \
                        & Q(list_update_time__lt=datetime.utcnow()-timedelta(hours=1)) & Q(soldout=False)).timeout(False)
        else:
            obj = m.Product.objects(Q(products_end__gt=datetime.utcnow()) | Q(products_end__exists=False)).timeout(False)
        print '{0} have {1} on sale event/category products.'.format(site, obj.count())
        for o in obj:
            print o.url()
            yield {'id': o.key, 'url': o.url()}

#        if hasattr(m, 'Category'):
#            obj = m.Product.objects(products_end__exists=False).timeout(False)
#            print '{0} have {1} on sale category products.'.format(site, obj.count())
#            for o in obj:
#                yield {'id': o.key, 'url': o.url()}

    elif method == 'check_offsale_product':
        obj = m.Product.objects(products_end__lt=datetime.utcnow()).timeout(False)

        print '{0} have {1} off sale event products.'.format(site, obj.count())
        for o in obj:
            yield {'id': o.key, 'url': o.url()}

        if hasattr(m, 'Category'):
            obj = m.Product.objects(products_end__exists=False).timeout(False)
            print '{0} have {1} off sale category products.'.format(site, obj.count())
            for o in obj:
                yield {'id': o.key, 'url': o.url()}

    elif method == 'check_onsale_event':
        if not hasattr(m, 'Event'):
            return
        obj = m.Event.objects(Q(events_end__gt=datetime.utcnow()) | Q(events_end__exists=False)).timeout(False)
        print '{0} have {1} on sale events.'.format(site, obj.count())

        for o in obj:
            yield {'id': o.event_id, 'url': o.url()}

    elif method == 'check_offsale_event':
        if not hasattr(m, 'Event'):
            return
        obj = m.Event.objects(events_end__lt=datetime.utcnow()).timeout(False)
        print '{0} have {1} off sale events.'.format(site, obj.count())

        for o in obj:
            yield {'id': o.event_id, 'url': o.url()}


def call_rpc(rpc, site, method, *args, **kwargs):
    try:
        rpc.run_cmd(site, method, args, kwargs)
    except Exception as e:
        print 'RPC call error: {0}'.format(traceback.format_exc())
        key = kwargs.get('id')
        url = kwargs.get('url')
        f = Fail()
        f.site = site
        f.method = method
        f.key = key
        f.url = url
        f.message = traceback.format_exc()
        f.save()


def checkout(site, method, rpc, concurrency=30, full=False):
    """ """
    rpcs = rpc if isinstance(rpc, list) else [rpc]
    pool = Pool(len(rpcs) * concurrency)
    ret = spout_obj(site, method, full=full)
    if ret is False:
        return
    for kwargs in ret:
        rpc = random.choice(rpcs)
        pool.spawn(call_rpc, rpc, site, method, **kwargs)
    pool.join()


def offsale_schedule(full=False):
    """  do checking

    if full is False, spout products whose list_update_time is old(so we should update them manually)
    if full is True, spout products no matter what value list_update_time is
    """
    from checkserver import CheckServer
    rpc = CheckServer()
    # rpc = get_rpcs([{'host_string':'root@127.0.0.1', 'port':8899}])
    # rpc = get_rpcs()

    # call will change the crpc/mastiff database
    checkout('ruelala', 'check_onsale_product', rpc, full=full)
    checkout('onekingslane', 'check_onsale_event', rpc, full=full)
    checkout('onekingslane', 'check_onsale_product', rpc, full=full)
    checkout('lot18', 'check_onsale_product', rpc, full=full)
    checkout('gilt', 'check_onsale_product', rpc, full=full)
    checkout('nomorerack', 'check_onsale_product', rpc, full=full)
    checkout('belleandclive', 'check_onsale_product', rpc, full=full)
    checkout('venteprivee', 'check_onsale_product', rpc, full=full)
    checkout('ideeli', 'check_onsale_product', rpc, full=full)
    checkout('modnique', 'check_onsale_product', rpc, full=full)
    checkout('totsy', 'check_onsale_product', rpc, full=full)

    # many on/off sale problem
    checkout('6pm', 'check_onsale_product', rpc, full=full)
    if full:
        # add endtime to nomorerack offstore products
        checkout('bluefly', 'check_onsale_product', rpc, full=full)
        checkout('nordstrom', 'check_onsale_product', rpc, full=full)
        checkout('ashford', 'check_onsale_product', rpc, full=full)
        checkout('saksfifthavenue', 'check_onsale_product', rpc, full=full)
        checkout('nomorerack', 'check_offsale_product', rpc, full=full)


def onsale_schedule(full=False):
    """  do checking

    """
    from checkserver import CheckServer
    rpc = CheckServer()
    # rpc = get_rpcs([{'host_string':'root@127.0.0.1', 'port':8899}])
    # rpc = get_rpcs()

    checkout('belleandclive', 'check_offsale_product', rpc, full=full)
    checkout('beyondtherack', 'check_offsale_product', rpc, full=full)
    checkout('gilt', 'check_offsale_product', rpc, full=full)
    checkout('lot18', 'check_offsale_product', rpc, full=full)
    checkout('modnique', 'check_offsale_product', rpc, full=full)
    checkout('onekingslane', 'check_offsale_product', rpc, full=full)
    checkout('ruelala', 'check_offsale_product', rpc, full=full)

def control():
    log_file = '/tmp/onoff_sale.log'
    pool = Pool(2)

    if os.path.isfile(log_file):
        # when log file exists, we do full=False update ( every 600 seconds )
        try:
            offsale_schedule(full=False)
        except:
            traceback.print_exc()

        if time.time() - os.path.getctime(log_file) > 86400:
            os.unlink(log_file)
        else:
            return
    else:
        # else, we create one, and do full=True update (every one day)
        with open(log_file, 'w') as fd:
            try:
                offsale_schedule()
                pool.spawn(onsale_schedule)

                from powers.script import secondhand_filter
                secondhand_filter.filter()
            except:
                fd.write(traceback.format_exc())

if __name__ == '__main__':
    while True:
        control()
        time.sleep(600)

