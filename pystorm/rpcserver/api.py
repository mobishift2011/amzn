#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" A pluggable API server runs any amount of worker, powered by gevent 

Worker     : execute some Code Blocks based on configs
Controller : schedules and monitors Workers
Code Block : should lives in seperate .py files under `workers` directory,
             each contains an `execute` method and  a `configs` dict
"""
import settings
import logging

import os
import zmq
import uuid
import gevent
import zerorpc

import multiprocessing
from msgpack import packb as pack, unpackb as unpack

logger = logging.getLogger("api")

class Worker(multiprocess.Process):
    """ Worker class to execute some code 
    
    * do some basic statistics
    * respond to controller's ping request
    * throttled subject to configs
    """
    default_configs = {
        'num_coroutines' : 1,   # num of concurrently running greenlets
        'qps_limit'      : 0,   # 0 -> not limiting, not implemented yet
    }
    def __init__(self, type=TYPE_BOLT, execute=lambda:None, configs={}):
        super(Worker, self).__init__(*args, **kwargs)

        self.uuid = uuid.uuid4()
        self.execute = execute
        self.configs = default_configs

        self.configs.update(configs)
        self.logger = logging.getLogger("api.Worker")

        self.context = None  # zeromq context

        # zmq related settings
        self.context         = None
        self.rpc             = None   # zerorpc server
        self.frontend        = None   # receives messages
        self.bind_address    = None   
        self.backends        = []     # pass messages to
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

        
    def execute(self, *args, **kwargs):
        if self._not_throttled():
            try:
                self.execute(*args, **kwargs)
            except Exception, e:
                self.logger.exception(e.message)
            else:
                self._executed()

    def bind(self):
        """ bind address & notify controller """
        self.context = zmq.Context()
        if self.type in [TYPE_BOLT, TYPE_OUTLET]:
            self.frontend        = self.context.socket(zmq.PULL)
            self.bind_address    = "tcp://{0}".format(random.choice(SERVERS))
            port                 = self.frontend.bind_to_random_port(self.bind_address)
            self.bind_address   += ":{0}".format(port)
            self.logger.debug(type(self).__name__ + " binded at " + self.bind_address)

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
        self.controller.send(pack(data))

    def run(self):
        """ runs the worker """
        # start a zerorpc server so that we can controll worker across process
        self.server = zerorpc.Server(worker_instance)
        self.server.bind()
        gevent.spawn(self.server.run)

        # bind itself to some port for listening and then tell the controller about this info
        self.bind()
        self.connect(self.addresses)

        while True:
            try:
                if self.type == TYPE_SPOUT:
                    self.results = self.execute()
                else:
                    self.packed_dict  = self.frontend.recv()
                    kwargs            = unpack(self.packed_dict)
                    self.results      = self.execute(**kwargs)

                if self.type == TYPE_OUTLET:
                    # for outlets, we don't need to push our messages further
                    # so we simply do nothing
                    pass
                else:
                    # pick a backend according to "grouping_policy", push result to it
                    for r in self.results:
                        backend = self.choose_backend(r)
                        backend.send(pack(r))
                self.loop_count += 1
            except Exception, e:
                logging.exception(e.message)

    def stop(self):
        if self.server:
            self.server.stop()

    def connect(self, addresses):
        for address in addresses:
            self.logger.debug(type(self).__name__ + " connecting " + address)
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

    def _not_throttled(self):
        # TODO implement throttling
        return True

    def _executed(self):
        # TODO implement statistics
        pass

class Scheduler(object):
    """ Schedules worker creates/stops/executes
    
    * schedule workers
    * monitor workers
    """
    workers = {}        # uuid -> Controller
    def __init__(self):
        self.logger = logging.getLogger("api.Controller")
        self.context = None
        self.ping_backend = None
        self.ping_address = None
        
    def start_workers(self):
        self.reload_workers()

    def get_all_stats(self):
        # TODO implement get stats info
        pass

    def request(self, request):
        """ processing request
    
        {"op":"all_stats"} -> a dict of stats
        """
        response = {}
        try:
            req = unpack(request)
        except Exception, e:
            response.update({"status":"error","message":e.message})
        else:
            if req.get("op") == "all_stats":
                response.update({"status":"ok"})
                response.update({"data":self.get_all_stats()})
            else:
                response.update({"status":"error","message":"op code error/not found"})
            
        return pack(response)

    def stop_workers(self):
        workers = Controller.workers
        for w in workers.itervalues():
            w.stop()

    def reload_workers(self):
        """ reload all workers from workers subdir
    
        * each worker lives in a .py file
        * each worker has a `execute` method and a `configs` dict
        """
        if not os.path.exists("workers"):
            self.logger.warning("workers directory does not exist")
            return

        self.stop_workers() 
        workers = Controller.workers = {}

        for path in os.listdir("workers"):
            if path.endswith(".py"): 
                code = open(path).read()
                try:
                    exec(code)
                except Exception, e:
                    self.logger.error("worker {0} cannot exec {1}".format(path, e.message))
                else:
                    f = locals().get("execute")
                    c = locals().get("configs")
                    multiprocessing.Process(Target=Worker, args=(f, c)).start()

    def ping_receiver(self):
        """ recieves ping from workers, record ping info """
        self.context         = zmq.Context()
        self.ping_backend    = self.context.socket(zmq.PULL)
        self.ping_address    = "tcp://0.0.0.0"
        port                 = self.ping_backend.bind_to_random_port(self.bind_address)
        self.ping_address   += ":{0}".format(port)

        self.logger.debug(type(self).__name__ + " binded at " + self.ping_address)

        poller = zmq.Poller()
        poller.register(self.ping_backend, zmq.POLLIN)

        while self.running:
            socks = dict(poller.poll(100))
            if socks.get(self.ping_backend) == zmq.POLLIN:
                message_packed = self.ping_backend.recv(zmq.NOBLOCK)
                d = unpack(message_packed)
                d["time"] = time.time()
                self.workers[d['uuid']] = d

if __name__ == "__main__":
    #c = Controller()
    #c.start_workers()
    s = zerorpc.Server(Sandbox())
    s.bind("tcp://0.0.0.0:4242")
    s.run()
