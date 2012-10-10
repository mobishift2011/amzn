import gevent
from gevent import monkey
monkey.patch_all()

from settings import *

import sys
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


def crawl_category(ss):
    ss.crawl_category()

def crawl_listing(ss):
    for item in col_cats.find({'leaf': 1, 'num': {'$exists': True}}, fields=['url', 'catstr'], timeout=False):
        ss.crawl_listing(item['url'], item['catstr'])
        progress()

def crawl_product(ss):
    # bah for find, url for download
    for item in col_product.find({'detail_parse': False}, fields=['bah', 'url'], timeout=False):
        ss.crawl_product(item['bah'], item['url'])
        progress()


if __name__ == '__main__':
#    from server import Server
#    ss = Server()
#    for p in Product.objects.filter(updated=False):
#        print p.url()
#        ss.crawl_product(p.url())
    from server import Server
    ss = Server()
#    crawl_category(ss)
    print len(sys.argv)
    if len(sys.argv) >= 2:
        crawl_product(ss)
    else:
        crawl_listing(ss)
