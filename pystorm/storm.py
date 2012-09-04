#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import socket
import random
import logging
import inspect
import requests 
import threading
import lxml.html
import lxml.etree

from settings import PEERS

from rpcserver.settings import SHUFFLE_GROUPING, FIELD_GROUPING
from rpcserver.settings import TYPE_SPOUT, TYPE_BOLT, TYPE_OUTLET, TYPE_MINT
from rpcserver.settings import ROOT_PORT

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
            "import settings\n",
            "import logging\n",
            "\n",
            "worker_type = settings.TYPE_{0}\n".format(self.typename),
            "\n",
            "configs = {0}\n".format(repr(self.configs)),
            "\n",
        ]

        self.codes.append("\n")
        for line in inspect.getsourcelines(worker_class.execute)[0]:
            # unindent 4 bytes
            self.codes.append(line[4:])

        self.codes.append("\n")
        for line in inspect.getsourcelines(worker_class.setup)[0]:
            # unindent 4 bytes
            self.codes.append(line[4:])

        self.check_type() 

        self.code = "".join(self.codes)


        self.parent = None
        self.children = []

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

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    def chain(self, node):
        self.add_child(node)
        return node

class Controller(object):
    """ controls deploys and others """
    def __init__(self):
        self.logger = logging.getLogger("storm.Controller")
        
    def add_worker(self, host_string, name, code, addresses):
        """ add worker to remote host, return bind_address """
        self.logger.warning("add worker {0} to {1}".format(name, host_string))
        from fabric.api import settings, run, put

        tmpfile = "/tmp/{0}.py".format(name)
        open(tmpfile, "w").write(code)

        with settings(host_string=host_string):
            run("mkdir -p /opt/pystorm/rpcserver/workers")
            put(tmpfile, "/opt/pystorm/rpcserver/workers/{0}.py".format(name))
            
        resp = self._request(host_string, {"op":"add_worker","worker_name":name,"backends":addresses})
        if resp and resp.get("worker_status"):
            return resp.get("worker_status").get("bind_address")
        else:
            raise ValueError("resp should be a dict with a key equals `worker_status`")

    def request(self, host_string, request):
        threading.Thread(target=self._request, args=(host_string, request)).start()

    def _request(self, host_string, request):
        """ send request to rpcserver """
        host = host_string[host_string.find('@')+1:] if '@' in host_string else host_string
        port = ROOT_PORT
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((host, port))
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
        finally:
            s.close()

class Topology(object):
    """ a tree of nodes """
    def __init__(self, node=None):
        self.logger = logging.getLogger("storm.Topology")
        self.root = node
        self.root_workers = []
        self.ctrl = Controller()

    def set_root(self, node):
        self.root = node
        return node

    def create(self, node=None):
        """ create topology from bottom up 

        return address of the node worker
        """
        if node is None:
            node = self.root

        addresses = []
        for n in node.children:
            child_address = self.create(n)
            addresses.extend(child_address)

        ret = self.spawn(node, addresses)
        return ret

    def spawn(self, node, addresses):
        """ spawn a worker for a node, add addresses to its backend """
        backends = []
        first_run_peers = list(PEERS)

        for _ in range(node.num_workers):
            if first_run_peers:
                host_string = random.choice(first_run_peers)
                first_run_peers.remove(host_string)
            else:
                host_string = random.choice(PEERS)

            addr = self.ctrl.add_worker(host_string, node.worker_name, node.code, addresses) 

            if addr:
                backends.append(addr)
                
        return backends

    #def shutdown(self):
    #    self.ctrl.shutdown()


class SimpleFetcher(Bolt):
    """ A general-purpose web page fetcher """
    def setup(self):
        import requests

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
        import lxml.html
        from zlib import compress, decompress

        self.logger.debug("get url {0}".format(url))
        content = self.session.get(url).text
        if selector:
            tree = lxml.html.fromstring(content)
            for t in tree.xpath(selector):
                ret = {"content":compress(lxml.etree.tostring(t))}
                yield ret
        else:
            ret = {"content":compress(content)}
            yield ret

if __name__ == '__main__':
    pass
