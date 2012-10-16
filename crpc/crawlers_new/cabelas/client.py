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

from gevent.pool import Pool
from datetime import datetime, timedelta


def progress(msg='.'):
    import sys
    sys.stdout.write(msg)
    sys.stdout.flush()


def crawl_category():
    from server import Server
    ss = Server()
    ss.crawl_category()


def crawl_listing(addrs):
    pool = Pool(30*len(addrs))
    clients = [zerorpc.Client(addr) for addr in addrs]
    it = 0 
    num_cats = Category.objects().count()
    for c in Category.objects(leaf=True):
        it += 1
        print c.catname, it, 'of', num_cats
        if c.spout_time and  c.spout_time > datetime.utcnow()-timedelta(hours=8):
            print '...skipped'
            continue
        if c.num:
            num_page = (c.num - 1) // ITEM_PER_PAGE + 1
            for page in xrange(1, num_page+1):
                page_item_NO = (page-1)*ITEM_PER_PAGE
                url = c.url( page_item_NO )
                if page == num_page:
                    pool.spawn(random.choice(clients).crawl_listing, url, c.catstr(), page, c.num % ITEM_PER_PAGE)
#                    ss.crawl_listing( url, c.catstr(), page, c.num % ITEM_PER_PAGE)
                else:
                    pool.spawn(random.choice(clients).crawl_listing, url, c.catstr(), page)
#                    ss.crawl_listing( url, c.catstr(), page)
                progress(str(page)+' ')
            print
        c.spout_time = datetime.utcnow()
        c.save()
    pool.join()


def crawl_product(addrs):
    pool = Pool(30*len(addrs))
    clients = [zerorpc.Client(addr, timeout=300) for addr in addrs]
    count = 0
    t = time.time()
    for p in Product.objects(updated=False).timeout(False):
#        ss.crawl_product(p.url(), p.itemID)
        pool.spawn(random.choice(clients).crawl_product, p.url(), p.itemID)
        progress('.')
        count += 1
        if count % 100 == 0:
            print 'qps', count/(time.time()-t)
    pool.join()


if __name__ == '__main__':
    pass
