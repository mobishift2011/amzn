from gevent import monkey
monkey.patch_all()

import time
import gevent
import gevent.pool
import requests
from lxml.html import fromstring

ROOT    = 'http://www.amazon.com/s/?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A541966'
PRODUCT = 'http://www.amazon.com/product_name/dp/{0}/'

headers = {
    'User-Agent': 'Mozilla 5.0/Firefox 15.0.1',
}

config = {
    'max_retries': 3,
    'pool_connections': 10,
    'pool_maxsize': 10,
}

s = requests.session(prefetch=True, timeout=15, config=config, headers=headers)
ip = s.get("http://httpbin.org/ip").text
print "which ip am i using?", ip
dps = set()

t1 = time.time()
def getindex(page=1):
    t1 = time.time()
    print 'page', page
    r = s.get(ROOT+"&page={0}".format(page))
    print 'page', page, 'fetched'
    text = r.text
    t = fromstring(text)
    result = t.xpath(".//div[@id='rightResultsATF']")[0]
    for a in result.findall(".//a"):
        slices = a.get('href').split('/')
        if len(slices)>4 and slices[4] == 'dp':
            dps.add(slices[5])

pool = gevent.pool.Pool(50)

for page in range(1, 11):
    pool.spawn(getindex, page)

pool.join()

print 'indexing time', time.time() - t1

urls = [ PRODUCT.format(dp) for dp in dps ]
print 'total products', len(urls)
finished = 0
def getpage(url):
    r = s.get(url)
    global finished
    finished += 1

t = time.time()
print 'starting fetches'
for url in urls:
    pool.spawn(getpage, url)

pool.join()
time_taken = time.time() - t
print 'qps', len(urls)/time_taken
print 'finished/total: {0}/{1}'.format(finished, len(urls))
