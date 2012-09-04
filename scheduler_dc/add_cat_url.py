from queue import SpiderQueue
import redis, pymongo
from scrapy.http import Request
from scrapy.utils.reqser import request_to_dict
import marshal

class Seeder:
    def __init__(self, spider, redis_server, mongo_server):
        self.spider = spider
        self.redis_server = redis_server
        self.mongo_server = mongo_server
        #self.queue = SpiderQueue(redis_server, spider, '%(spider)s:requests')
        self.queue_key = '%s:requests' % (spider)
        
    def insert_seed(self, url, catstr):
        req = Request(url)
        req.meta['page'] = 'listing'
        req.meta['count'] = 0
        req.meta['catstr'] = catstr   # catstr
        d = request_to_dict(req)  #, self.spider)
        d['callback']= 'parse'  #'_response_downloaded'
        data = marshal.dumps(d)
        #self.queue.push(data, encoded=True)
        self.redis_server.rpush(self.queue_key, data)
        
    def seed_done(catstr):
        seed = self.mongo_server.find_one({'catstr': catstr})
        if seed:
            seed['crawled'] = 1
            self.mongo_server.update(seed)

if __name__ == "__main__":
    import redis, sys
    from optparse import OptionParser
    redis_server = redis.Redis('localhost', 6379)
    mgdb_conn = pymongo.Connection('localhost')
    cats = mgdb_conn['amazon']['cats']
    seeder = Seeder('amazon', redis_server, cats)
    
    parser = OptionParser(usage='usage: %prog [options]')
    # commands
    parser.add_option('-q', '--query', dest='query', help="query to select rows", default='')
    parser.add_option('-c', '--cat', dest='cat', help="category to select a row", default='')
    parser.add_option('--dryrun', dest='dryrun', action='store_true', help="dryrun", default=False)
    
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit()

    (options, args) = parser.parse_args(sys.argv[1:])
    if options.query:
        print 'query=', options.query
        rows = cats.find(eval(options.query), fields=['url', 'catstr'])
    elif options.cat:
        rows = cats.find({'catstr':options.cat}, fields=['url', 'catstr'])

    for r in rows:
        print r['catstr']
        if not options.dryrun:
            seeder.insert_seed(r['url'], r['catstr'])
        
