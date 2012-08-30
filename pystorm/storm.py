#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import zmq
import time
import random
import logging
import threading
import multiprocessing
import cPickle as pickle

SERVERS = ['127.0.0.1']

SHUFFLE_GROUPING, FIELD_GROUPING = 1001, 1002
TYPE_SPOUT, TYPE_BOLT, TYPE_OUTLET = 2001, 2002, 2003

class Controller(object):
    """ controlling workers """
    def __init__(self):
        self.context = None
        self.backend = None
        self.running = True
        self.bind_address = None
        self.workers_by_pid = {}
        threading.Thread(target=self.receiver).start()

    def shutdown(self):
        for pid in self.workers_by_pid.keys():
            print "killing", pid
            os.kill(int(pid), 9)
        self.running = False
    
    def get_backend_addresses(self, worker_class):
        addresses = []
        for w in self.workers_by_pid.values():
            if w['worker_class'] == type(worker_class).__name__:
                addresses.append(w['bind_address'])
        return addresses

    def receiver(self):
        self.context         = zmq.Context()
        self.controller      = self.context.socket(zmq.PULL)
        self.bind_address    = "tcp://{0}".format(random.choice(SERVERS))
        port                 = self.controller.bind_to_random_port(self.bind_address)
        self.bind_address   += ":{0}".format(port)

        print type(self).__name__, "binded", self.bind_address
        poller = zmq.Poller()
        poller.register(self.controller, zmq.POLLIN)

        while self.running:
            socks = dict(poller.poll(100))
            if socks.get(self.controller) == zmq.POLLIN:
                message_pickled = self.controller.recv(zmq.NOBLOCK)
                d = pickle.loads(message_pickled)
                d["time"] = time.time()
                self.workers_by_pid[d['pid']] = d

class Worker(multiprocessing.Process):
    """ A general zeromq worker

    bind on a random port  
    able to connect to other workers
    """
    def __init__(self, type=TYPE_BOLT, *args, **kwargs):
        super(Worker, self).__init__(*args, **kwargs)

        # zmq related settings
        self.context         = None
        self.frontend        = None
        self.bind_address    = None
        self.backends        = []
        self.addresses       = []
        self.grouping_fields = []
        self.grouping_policy = SHUFFLE_GROUPING

        # controller related settings
        self.create_time     = time.time()
        self.loop_count      = 0
        self.controller      = None
        self.controller_address = None

        self.type            = type
        if self.type not in [TYPE_SPOUT, TYPE_BOLT, TYPE_OUTLET]:
            raise NotImplementedError()

    def bind(self):
        """ bind address & notify controller """
        self.context = zmq.Context()
        if self.type in [TYPE_BOLT, TYPE_OUTLET]:
            self.frontend        = self.context.socket(zmq.PULL)
            self.bind_address    = "tcp://{0}".format(random.choice(SERVERS))
            port                 = self.frontend.bind_to_random_port(self.bind_address)
            self.bind_address   += ":{0}".format(port)
            print type(self).__name__, "binded", self.bind_address

        self.controller = self.context.socket(zmq.PUSH)
        self.controller.connect(self.controller_address)
        self.ping_controller()
        
    def ping_controller(self):
        data = {
            "pid":              os.getpid(),
            "worker_class":     type(self).__name__,
            "bind_address":     self.bind_address,
            "loop_count":       self.loop_count,
            "cpu_percent":      time.clock()/(time.time()-self.create_time),
        }
        self.controller.send(pickle.dumps(data))

    def execute(self, **kwargs):
        """ accepts fields, yield results, must implement by subclasses """
        raise NotImplementedError("should be implemented by subclass")

    def run(self):
        self.bind()
        self.connect(self.addresses)

        poller = zmq.Poller()
        poller.register(self.controller, zmq.POLLIN)

        while True:
            try:
                if self.type == TYPE_SPOUT:
                    self.results = self.execute()
                else:
                    self.pickled_dict = self.frontend.recv()
                    kwargs            = pickle.loads(self.pickled_dict)
                    self.results      = self.execute(**kwargs)

                if self.type == TYPE_OUTLET:
                    # for outlets, we don't need to push our messages further
                    # so we simply do nothing
                    pass
                else:
                    # pick a backend according to "grouping_policy", push result to it
                    for r in self.results:
                        backend = self.choose_backend(r)
                        backend.send(pickle.dumps(r))
                self.loop_count += 1
            except Exception, e:
                logging.exception(e.message)
                
    def connect(self, addresses):
        for address in addresses:
            print type(self).__name__, "connecting", address
            backend = self.context.socket(zmq.PUSH)
            backend.connect(address)
            self.backends.append(backend)

    def set_grouping(self, policy=SHUFFLE_GROUPING, fields=None):
        self.grouping_policy = policy
        self.grouping_fields = fields

    def choose_backend(self, result_dict):
        if self.grouping_policy == SHUFFLE_GROUPING:
            return random.choice(self.backends)
        elif self.grouping_policy == FIELD_GROUPING:
            mod = len(self.backends)
            values = [ result_dict.get(field) for field in self.grouping_fields ]
            return self.backends[hash(tuple(values)) % mod]
        else:
            raise NotImplementedError()

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

class Node(object):
    """ a node in topology """
    def __init__(self, worker_class, num_of_workers, grouping_policy=SHUFFLE_GROUPING, fields=None):
        self.worker_class = worker_class
        self.num_of_workers = num_of_workers
        self.grouping_policy = grouping_policy
        self.fields = fields
        self.parent = None
        self.children = []

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

class Topology(object):
    """ a tree of nodes """
    def __init__(self, node=None):
        self.root = node
        self.root_workers = []
        self.ctrl = Controller()
        time.sleep(0.1)

    def set_root(self, node):
        self.root = node

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

        return self.spawn(node, addresses)

    def spawn(self, node, addresses):
        """ spawn a worker for a node, add addresses to its backend """
        backends = []
        for _ in range(node.num_of_workers):
            w = node.worker_class()
            w.addresses = addresses
            w.controller_address = self.ctrl.bind_address
            w.set_grouping(node.grouping_policy, node.fields)
        
            if node == self.root:
                self.root_workers.append( w )
            else:
                w.start()
                
        time.sleep(0.1)
        backends.extend( self.ctrl.get_backend_addresses(w) )
                
        return backends

    def start(self):
        """ run the root worker """
        for w in self.root_workers:
            w.start()

    def shutdown(self):
        self.ctrl.shutdown()

if __name__ == '__main__':
    pass
