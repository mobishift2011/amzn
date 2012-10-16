#encoding=utf-8
import gevent
from gevent import monkey
monkey.patch_all()

from settings import *
from models import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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


def crawl_listing(addrs):
    """
        Output:
            num_new_crawl - newly crawled
            num_new_update - newly updated
            num_not_exist - page not exist or timeout or 404
            num_parse_error - page parse error
    """
#    from server import Server
#    ss = Server()
    pool = Pool(20*len(addrs)+1)
    clients = [zerorpc.Client(addr, timeout=300) for addr in addrs]
    it = 0 
    num_cats = Category.objects().count()
    for c in Category.objects(leaf=True).timeout(False):
        it += 1
        print c.catname, it, 'of', num_cats
        if c.spout_time and  c.spout_time > datetime.utcnow()-timedelta(hours=8):
            print '...skipped'
            continue
#        ss.crawl_listing( c.url(), c.catstr() )
        pool.spawn(random.choice(clients).crawl_listing, c.url(), c.catstr())
        c.spout_time = datetime.utcnow()
        c.save()
    pool.join()


def crawl_product(addrs):
    pool = Pool(50*len(addrs)+1)
    clients = [zerorpc.Client(addr, timeout=300) for addr in addrs]
    count = 0
    t = time.time()
    for p in Product.objects(updated=False).timeout(False):
#        ss.crawl_product(p.url())
        pool.spawn(random.choice(clients).crawl_product, p.url())
        progress('.')
        count += 1
        if count % 100 == 0:
            print 'qps', count/(time.time()-t)
    pool.join()


def update_product(*targs):
    """ Parameter *targs for updating:
            price, available, shipping, rating, reviews, ...
    """
    from server import Server
    ss = Server()
#    pool = Pool(50*len(addrs)+1)
#    clients = [zerorpc.Client(addr, timeout=300) for addr in addrs]
    count = 0
    for p in Product.objects().timeout(False):
        ss.update_product(p, *targs)
#        pool.spawn(random.choice(clients).update_product, p, *targs)
        count += 1
        if count % 100 == 0:
            print 'qps', count / (time.time() - t)
#    pool.join()
        


if __name__ == '__main__':
    pass
