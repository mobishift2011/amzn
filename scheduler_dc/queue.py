import marshal
from scrapy.utils.reqser import request_to_dict, request_from_dict

class SpiderQueue(object):
    """Per-spider queue abstraction on top of redis using sorted set"""

    def __init__(self, server, spider, key):
        """Initialize per-spider redis queue

        Parameters:
            server -- redis connection
            spider -- spider instance
            key -- key for this queue (e.g. "%(spider)s:queue")

        """
        self.server = server
        self.spider = spider
        self.key = key % {'spider': spider.name}

    def __len__(self):
        return self.server.llen(self.key)

    def push(self, request, encoded=False):
        if not encoded:
            data = marshal.dumps(request_to_dict(request, self.spider))
        else:
            data = request
        self.server.rpush(self.key, data)

    def pop(self):
        # use atomic range/remove using multi/exec
        result = self.server.lpop(self.key)
        if result:
            return request_from_dict(marshal.loads(result), self.spider)

    def clear(self):
        self.server.delete(self.key)

