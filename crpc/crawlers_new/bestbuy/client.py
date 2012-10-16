import gevent
from gevent import monkey
monkey.patch_all()

from settings import *

import time
import random
import zerorpc
import requests
import pymongo

from gevent.pool import Pool

conn = pymongo.Connection(DB_HOST)
col_cats = conn[DB]['category']
col_product = conn[DB]['product']

def progress(msg='.'):
    import sys
    sys.stdout.write(msg)
    sys.stdout.flush()

def crawl_category():
    from server import Server
    ss = Server()
    ss.crawl_category()


#def crawl_listing(ss):
#    pool = Pool(30)
#    for item in col_cats.find({'leaf': 1, 'num': {'$exists': True}}, fields=['url', 'catstr']):
#        pool.spawn(ss.crawl_listing, item['url'], item['catstr'])
#        progress() 
#    pool.join()

def crawl_listing(addrs):
    pool = Pool(30*len(addrs))
    clients = [zerorpc.Client(addr) for addr in addrs]
    for item in col_cats.find({'leaf': 1, 'num': {'$exists': True}}, fields=['url', 'catstr']):
        pool.spawn(random.choice(clients).crawl_listing, item['url'], item['catstr'])
        progress() 
    pool.join()

#def crawl_product(ss):
#    pool = Pool(30)
#    # sku for find, url for download
#    for item in col_product.find({'detail_parse': {'$ne': True}}, fields=['sku', 'url'], timeout=False):
#        pool.spawn(ss.crawl_product, item['sku'], 'http://www.bestbuy.com' + item['url'])
#        progress() 
#    pool.join()

def crawl_product(addrs):
    pool = Pool(30*len(addrs))
    clients = [zerorpc.Client(addr) for addr in addrs]
    count = 0
    begin = time.time()
    # sku for find, url for download
    for item in col_product.find({'detail_parse': {'$ne': True}}, fields=['sku', 'url'], timeout=False):
        pool.spawn(random.choice(clients).crawl_product, item['sku'], 'http://www.bestbuy.com' + item['url'])
        progress() 
        count += 1
        if count % 100 == 0:
            print 'qps ', count / (time.time() - begin)
    pool.join()


if __name__ == '__main__':
    pass
