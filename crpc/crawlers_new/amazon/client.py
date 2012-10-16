import gevent
from gevent import monkey
monkey.patch_all()

from settings import *

import time
import random
import redisco
import zerorpc
import requests

from models import *
from gevent.pool import Pool
from crawlers.common.utils import crawl

def progress(msg):
    import sys
    sys.stdout.write(msg)
    sys.stdout.flush()

def crawl_listing(addrs):
    pool = Pool(10*len(addrs))
    clients = [zerorpc.Client(addr, timeout=300) for addr in addrs]
    num_cats = Category.objects().count()
    it = 0
    for c in Category.objects(is_leaf=True).order_by('-update_time'):
        it += 1
        print c.catstr(), '{0} of {1}'.format(it, num_cats)
        if c.spout_time and  c.spout_time > datetime.utcnow()-timedelta(hours=12):
            print '...skipped'
            continue
        pages = (c.num-1)/c.pagesize+10
        for p in range(1, min(pages+1,401)):
            url = c.url()+'&page={0}'.format(p)
            progress(str(p)+' ')
            pool.spawn(crawl, random.choice(clients), 'crawl_listing', url)
        print
        c.spout_time = datetime.utcnow()
        c.save()
    pool.join()

def crawl_product(addrs):
    pool = Pool(20*len(addrs))
    clients = [zerorpc.Client(addr, timeout=300) for addr in addrs]
    t = time.time()
    count = 0
    for p in Product.objects.filter(updated=False):
        count += 1
        pool.spawn(crawl, random.choice(clients), 'crawl_product', p.url())
        progress(".")
        if count % 100 == 0:
            print 'current qps:', count/(time.time()-t)
    pool.join()

if __name__ == '__main__':
    crawl_product(['tcp://127.0.0.1:1234'])
    from server import Server
    ss = Server()
    for p in Product.objects.filter(updated=False):
        print p.url()
        ss.crawl_product(p.url())
