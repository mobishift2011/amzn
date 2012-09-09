#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import pickle
import socket
import random
import logging
import inspect
import requests 
import threading
import lxml.html
import lxml.etree

from settings import PEERS

from rpcserver.configs import SHUFFLE_GROUPING, FIELD_GROUPING
from rpcserver.configs import TYPE_SPOUT, TYPE_BOLT, TYPE_OUTLET, TYPE_MINT
from rpcserver.configs import ROOT_PORT

from msgpack import packb as pack, unpackb as unpack

class Worker(object):
    """ Raw Worker """
    def setup(self):
        pass

    def execute(self, **kwargs):
        raise NotImplementedError("This method should be overrided by sub class")

class Spout(Worker):
    """ source of the task chain
    
    a special worker which do not serve on any port, i.e. content generator
    """
    def __init__(self, *args, **kwargs):
        super(Spout, self).__init__(type=TYPE_SPOUT, *args, **kwargs)

class Bolt(Worker):
    """ consumer and redispatcher """
    def __init__(self, *args, **kwargs):
        super(Bolt, self).__init__(type=TYPE_BOLT, *args, **kwargs)

class Outlet(Worker):
    """ finishes a task chain """
    def __init__(self, *args, **kwargs):
        super(Outlet, self).__init__(type=TYPE_OUTLET, *args, **kwargs)

class Mint(Worker):
    """ independent workers: no `input`/`output` """
    def __init__(self, *args, **kwargs):
        super(Mint, self).__init__(type=TYPE_MINT, *args, **kwargs)

class Node(object):
    """ a node in topology """
    def __init__(self, worker_class, num_workers, grouping_policy=SHUFFLE_GROUPING, fields=None, configs={}):
        if not issubclass(worker_class, Worker):
            raise TypeError("worker class should be a sub class of Worker")

        self.worker_class = worker_class
        self.worker_name = worker_class.__name__
        self.configs = configs              # temporily unused
        self.num_workers = num_workers
        self.grouping_policy = grouping_policy
        self.fields = fields
        self.varnames = worker_class.execute.func_code.co_varnames

        self.typename = worker_class.__base__.__name__.upper()
        if self.typename not in ["SPOUT","BOLT","OUTLET","MINT"]:
            self.typename = worker_class.__base__.__base__.__name__.upper()
            
        self.codes = [
            "#!/usr/bin/env python\n",
            "# -*- coding: utf-8 -*-\n",
            "import os\n",
            "import sys\n",
            "sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))\n",
            "\n"
            "import configs\n",
            "import logging\n",
            "import pickle\n",
            "\n",
            "worker_type = configs.TYPE_{0}\n".format(self.typename),
            "\n",
            "configs = {0}\n".format(repr(self.configs)),
            "\n",
            "policy = {0}\n".format(self.grouping_policy),
            "\n"
            "fields = {0}\n".format(repr(self.fields)),
            "\n"
        ]

        for line in inspect.getsourcelines(worker_class.execute)[0]:
            # unindent 4 bytes
            self.codes.append(line[4:])
        self.codes.append("\n")

        for line in inspect.getsourcelines(worker_class.setup)[0]:
            # unindent 4 bytes
            self.codes.append(line[4:])
        self.codes.append("\n")

        self.check_type() 

        self.code = "".join(self.codes)


        self.parent = None
        self.children = []
        self.worker_status_list = []
        self.created = False
        self.backends = []

    def check_type(self):
        """ type checking """
        typename = type(self.worker_class).__name__

        # check argument list
        if typename in ["Spout", "Mint"]:
            assert len(self.varnames) == 1, "worker type and execute args does not match"
        else:
            assert len(self.varnames) > 1, "worker type and execute args does not match"

        # check return type
        if typename in ["Spout", "Bolt"]:
            lastline = self.codes[-1]
            if "yield" not in lastline:
                raise ValueError("Spouts/Bolts should yield a dict as kwargs to the next worker")

    def add_worker_status(self, worker_status):
        self.worker_status_list.append(worker_status)

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    def chain(self, node):
        self.add_child(node)
        return node

class Controller(object):
    """ controls deploys and others """
    def __init__(self, path):
        self.path = path
        self.name = path.rsplit('/',1)[-1]
        self.host_added = []
        self.ss = {}

    @property
    def logger(self):
        return logging.getLogger("storm.Topology")

    def add_common(self, host_string):
        from fabric.api import settings, put, run
        with settings(host_string=host_string, warn_only=True):
            run("mkdir -p /opt/pystorm/rpcserver/common/")
            put(self.path, "/opt/pystorm/rpcserver/common/")

    def add_worker(self, host_string, name, code, addresses, num=1):
        """ add worker to remote host, return bind_address """
        if host_string not in self.host_added:
            self.add_common(host_string)

        self.logger.info("add worker {0} to {1}".format(name, host_string))
        from fabric.api import settings, run, put

        tmpfile = "/tmp/{0}.py".format(name)
        open(tmpfile, "w").write(code)

        with settings(host_string=host_string):
            run("mkdir -p /opt/pystorm/rpcserver/workers")
            put(tmpfile, "/opt/pystorm/rpcserver/workers/{0}.py".format(name))
            
        resp = self._request(host_string, {"op":"add_worker","worker_name":name,"backends":addresses,"num":num})
            
        if resp:
            return resp.get("worker_status")
        else:
            raise ValueError("resp should be a dict with a key equals `worker_status`")

    def stop_worker(self, host_string, uuid):
        """ stop worker @ remote host """
        self.logger.info("stop worker {0} @ {1}".format(uuid, host_string))
        resp = self._request(host_string, {"op":"stop_worker","uuid":uuid})

    def destroy(self, node):
        """ stop all workers of this node """
        for worker_status in node.worker_status_list:
            uuid = worker_status.get('uuid')
            host_string = worker_status.get('host_string')
            self.stop_worker(host_string, uuid)

    def get_status(self, host_string, uuid):
        resp = self._request(host_string, {"op":"get_status","uuid":uuid})
        return resp

    #def request(self, host_string, request):
    #    threading.Thread(target=self._request, args=(host_string, request)).start()

    def _request(self, host_string, request):
        """ send request to rpcserver """
        host = host_string[host_string.find('@')+1:] if '@' in host_string else host_string
        port = ROOT_PORT
        if host_string not in self.ss:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            self.ss[host_string] = s
        else:
            s = self.ss[host_string]

        try:
            s.sendall( pack(request)+'\n' ) 
            resp = unpack(s.recv(8192))
        except socket.timeout:
            self.logger.warning("request timed out: <request: {0}>".format(request))
        except Exception, e:
            self.logger.exception("unexpected exception: {0}".format(e.message))
        else:
            if not isinstance(resp, dict):
                raise ValueError("rpcserver should return a packed dict")

            if resp.get("status") != "ok":
                self.logger.exception("request has unexpected return: <request: {0}>, <response: {1}>".format(repr(request), repr(resp)))

            return resp.get("data")

class Topology(object):
    """ a tree of nodes """
    def __init__(self, path):
        self.roots = []
        self.ctrl = Controller(path)

    @property
    def logger(self):
        return logging.getLogger("storm.Topology")

    def add_root(self, node):
        self.roots.append(node)
        return node

    def create(self, node=None):
        """ create topology from bottom up 

        return address of the node worker
        """
        if node is None:
            for node in self.roots:
                self.create(node)
            # clear ctrl's socket so that we can pickle it
            self.ctrl.ss = {}

        if node.created:
            return node.backends  

        addresses = []
        for n in node.children:
            child_address = self.create(n)
            addresses.extend(child_address)

        ret = self.spawn(node, addresses)
        return ret

    def spawn(self, node, addresses):
        """ spawn a worker for a node, add addresses to its backend """
        backends = []
        round_robin_peers = list(PEERS)
        average, bonus = divmod(node.num_workers, len(PEERS))

        for _ in range(len(PEERS)):
            if bonus > 0:
                num = average+1
                bonus -= 1
            else:
                num = average

            host_string = random.choice(round_robin_peers)
            round_robin_peers.remove(host_string)

            statuses = self.ctrl.add_worker(host_string, node.worker_name, node.code, addresses, num) 
            addrs = []
            for status in statuses:
                addrs.append( status.get("bind_address") )
                status.update({'host_string':host_string})
                node.add_worker_status(status)

            for addr in addrs:
                if addr:
                    host = host_string[host_string.find('@')+1:] if '@' in host_string else host_string
                    backends.append(addr.replace('0.0.0.0',host))
                
        node.created = True
        node.backends = backends
        return backends

    def destroy(self, node=None):
        if not node:
            for node in self.roots:
                self.destroy(node)
            self.ctrl.ss = {}
        
        self.ctrl.destroy(node)

        for n in node.children:
            self.destroy(n)

    def all_status(self, node=None):
        statuses = []
        if not node:
            for node in self.roots:
                statuses.extend(self.all_status(node))
            self.ctrl.ss = {}
            return statuses
    
        for status in node.worker_status_list:
            statuses.append(self.ctrl.get_status(status.get('host_string'), status.get('uuid')))

        for n in node.children:
            statuses.extend(self.all_status(n))
    
        return statuses


class SimpleFetcher(Bolt):
    """ A general-purpose web page fetcher """
    def setup(self):
        import requests

        self.cache_timeout = 3600*24
        self.cache = {}    # caches url and its visit time

        self.session = requests.Session(
            prefetch = True,
            timeout = 15,
            headers = {
                'User-Agent': 'Mozilla 5.0/Firefox 15.0.1 FavBuyBot',
            },
            config = {
                'max_retries': 3,
                'pool_connections': 10,
                'pool_maxsize': 10,
            }
        ) 

    def execute(self, url, selector=None):
        """ given url, fetch page, return content (filtered by selector if present)

        @param: `url` is the web url to fetch
        @param: `selector` is a xpath string to extract blocks of info from the page
                the main page main contain too many unuseful infos that we want to filter
        
        @yield: a list/tuple of zlib compressed 
        """
        import time
        import lxml.html
        from zlib import compress, decompress

        self.logger.debug("get url {0}".format(url))

        # if cache not expired, don't fetch
        if url in self.cache and time.time() - self.cache.get(url) < self.cache_timeout:
            return
        else:
            self.cache[ url ] = time.time()
                
        content = self.session.get(url).content
        if selector:
            tree = lxml.html.fromstring(content)
            for t in tree.xpath(selector):
                ret = {"url":url,"content":compress(lxml.etree.tostring(t))}
                yield ret
        else:
            ret = {"url":url,"content":compress(content)}
            yield ret

if __name__ == '__main__':
    pass
