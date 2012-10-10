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

def progress(msg):
    import sys
    sys.stdout.write(msg)
    sys.stdout.flush()

def crawl_listing(addrs):
    pool = Pool(10*len(addrs))
    clients = [zerorpc.Client(addr, timeout=300) for addr in addrs]
    num_cats = Category.objects().count()
    it = 0
    for c in Category.objects().order_by('-update_time'):
        it += 1
        if c.spout_time and  c.spout_time > datetime.utcnow()-timedelta(hours=8):
            print '...skipped'
            continue
        pages = (c.num-1)/c.pagesize+1
        for p in range(1, min(pages+1,401)):
            url = c.url()+'&page={0}'.format(p)
            progress(str(p)+' ')
            pool.spawn(random.choice(clients).crawl_listing, url)
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
        pool.spawn(random.choice(clients).crawl_product, p.url())
        progress(".")
        if count % 100 == 0:
            print 'current qps:', count/(time.time()-t)
    pool.join()


def crawl_listing():
    from server import Server
    from gevent.queue import Queue
    ss = Server()
    pool = Pool(50)
    it = 0
    num_cats = Category.objects().count()
    for c in Category.objects():
        it += 1
        print c.catid, c.catname, it, 'of', num_cats
        if c.spout_time and  c.spout_time > datetime.utcnow()-timedelta(hours=8):
            print '...skipped'
            continue
        if c.num:
            for page in range(1, min((c.num-1)/100+2,101)):
                url = c.url(page)
                pool.spawn(ss.crawl_listing, url)
                progress(str(page)+' ')
            print
        c.spout_time = datetime.utcnow()
        c.save()
    pool.join()

def crawl_product(addrs):
    from server import Server
    from zerorpc import Client
    pool = Pool(50*len(addrs)+1)
    clients = [zerorpc.Client(addr, timeout=300) for addr in addrs]
    ss = Server()
    count = 0
    t = time.time()
    for p in Product.objects(updated=False):
        url = p.url()
        #print url
        #ss.crawl_product(url)
        #pool.spawn(ss.crawl_product, url)
        pool.spawn(random.choice(clients).crawl_product, url)
        progress('.') 
        count += 1
        if count % 100 == 0:
            print 'qps', count/(time.time()-t)
    pool.join()

if __name__ == '__main__':
    pass
    #crawl_listing()
    crawl_product([])
