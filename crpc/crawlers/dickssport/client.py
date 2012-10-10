import gevent
from gevent import monkey
monkey.patch_all()

from settings import *
from models import *

import sys
import time
import random
import zerorpc
import requests
import redis

from gevent.pool import Pool
from datetime import datetime, timedelta

if redis_SERVER.exists(redis_KEY): redis_SERVER.delete(redis_KEY)
redis_SERVER.hmset(redis_KEY, dict(num_new_crawl=0, num_new_update=0, num_not_exist=0, num_parse_error=0))

def progress(msg='.'):
    import sys
    sys.stdout.write(msg)
    sys.stdout.flush()


def crawl_category():
    from server import Server
    ss = Server()
    ss.crawl_category()


def crawl_listing(*targs):
    """ Parameter *targs for updating:
            price, available, shipping, rating, reviews, sell_rank ...

        Output:
            num_new_crawl - newly crawled
            num_new_update - newly updated
            num_not_exist - page not exist or timeout or 404
            num_parse_error - page parse error
    """
    from server import Server
    ss = Server()
#    pool = Pool(50)
    it = 0 
    num_cats = Category.objects().count()
    for c in Category.objects(leaf=True):
        it += 1
        print c.catname, it, 'of', num_cats
        if c.spout_time and  c.spout_time > datetime.utcnow()-timedelta(hours=8):
            print '...skipped'
            continue
        ss.crawl_listing( c.url(), c.catstr() )
#        pool.spawn(ss.crawl_listing, c.url(), c.catstr(), page, c.num % ITEM_PER_PAGE)
        c.spout_time = datetime.utcnow()
        c.save()
#    pool.join()


def crawl_product():
    from server import Server
#    pool = Pool(50*len(addrs)+1)
#    clients = [zerorpc.Client(addr, timeout=300) for addr in addrs]
    ss = Server()
    count = 0
    t = time.time()
    for p in Product.objects(updated=False).timeout(False):
        url = p.url()
        ss.crawl_product(url, p.itemID)
#        pool.spawn(random.choice(clients).crawl_product, url)
        progress('.')
        count += 1
        if count % 100 == 0:
            print 'qps', count/(time.time()-t)
#    pool.join()


if __name__ == '__main__':
#    crawl_category()
    crawl_listing()
#    if len(sys.argv) >= 2:
#        crawl_product()
#    else:
#        crawl_listing()
