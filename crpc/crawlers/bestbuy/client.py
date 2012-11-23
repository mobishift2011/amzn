import gevent
from gevent import monkey
monkey.patch_all()

from settings import *

import time
import random
#import redisco
import zerorpc
import requests
import pymongo

from gevent.pool import Pool

conn = pymongo.Connection(DB_HOST)
col_cats = conn[DB]['category']
col_product = conn[DB]['product']

def progress():
    import sys
    sys.stdout.write('.')
    sys.stdout.flush()

def crawl_category(addrs):
    clients = [zerorpc.Client(addr) for addr in addrs]
    threads = []
    for i in xrange(30*len(addrs)):
        threads.append( gevent.spawn(random.choice(clients).crawl_category) )
        progress()
    gevent.joinall(threads)

def crawl_category():
    from server import Server
    ss = Server()
    ss.crawl_category()

def crawl_listing(addrs):
    pool = Pool(30*len(addrs))
    clients = [zerorpc.Client(addr) for addr in addrs]
    for item in col_cats.find({'leaf': 1, 'num': {'$exists': True}}, fields=['url', 'catstr']):
        pool.spawn(random.choice(clients).crawl_listing, item['url'], item['catstr'])
        progress() 
    pool.join()

def crawl_product(addrs):
    pool = Pool(30*len(addrs))
    clients = [zerorpc.Client(addr) for addr in addrs]
    # sku for find, url for download
    for item in col_product.find({'detail_parse': False}, fields=['sku', 'url']):
        pool.spawn(random.choice(clients).crawl_product, item['sku'], item['url'])
        progress() 
    pool.join()


def crawl_listing(ss):
    pool = Pool(30)
    for item in col_cats.find({'leaf': 1, 'num': {'$exists': True}}, fields=['url', 'catstr']):
        pool.spawn(ss.crawl_listing, item['url'], item['catstr'])
        progress() 
    pool.join()

def crawl_product(ss):
    pool = Pool(30)
    # clients = [zerorpc.Client(addr) for addr in addrs]
    # sku for find, url for download
    for item in col_product.find({'detail_parse': {'$ne': True}}, fields=['sku', 'url'], timeout=False):
        pool.spawn(ss.crawl_product, item['sku'], 'http://www.bestbuy.com' + item['url'])
        progress() 
    pool.join()

if __name__ == '__main__':
#    for p in Product.objects.filter(updated=False):
#        print p.url()
#        ss.crawl_product(p.url())
    from server import Server
    ss = Server()
#    crawl_listing(ss)
    crawl_product(ss)
#    add = ['tcp://127.0.0.1:{0}'.format(CRAWLER_PORT)]
