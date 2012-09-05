#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" A pluggable API server runs any amount of worker 

Worker     : execute some Code Blocks based on configs
Controller : schedules and monitors Workers
Code Block : should lives in seperate .py files under `workers` directory,
             each contains an `execute` method and  a `configs` dict
"""
import settings
from settings import SHUFFLE_GROUPING, FIELD_GROUPING
from settings import TYPE_SPOUT, TYPE_BOLT, TYPE_OUTLET, TYPE_MINT

import os
import re
import zmq
import uuid
import time
import random
import logging
import threading

import multiprocessing
from msgpack import packb as pack, unpackb as unpack

logger = logging.getLogger("api")

class Worker(multiprocessing.Process):
    """ Worker class to execute some code 
    
    * do some basic statistics
    * respond to controller's ping request
    * throttled subject to configs
    """
    usable_ports = set(settings.CONTROLLER_PORT_RANGE)
    default_configs = {
        'num_coroutines' : 1,   # num of concurrently running greenlets
        'qps_limit'      : 0,   # 0 -> not limiting, not implemented yet
    }
    def __init__(self,  type=TYPE_BOLT, 
                        controller_address=None, 
                        backend_addresses=[], 
                        setup=None,
                        execute=None, 
                        configs={}, 
                        policy = SHUFFLE_GROUPING,
                        fields = [],
                        worker_name = "unnamed",
                        *args, **kwargs):
        super(Worker, self).__init__(*args, **kwargs)

        setup(self)

        self.worker_name = worker_name
        self.uuid = uuid.uuid4().hex
        self._execute = execute
        self.configs = Worker.default_configs
        self.configs.update(configs)
        self.logger = logging.getLogger("api.Worker.{0}".format(worker_name))

        self.__stopped = False

        # zmq related settings
        self.context         = None
        self.rpc             = None   # zerorpc server
        self.rpc_address     = ""
        self.frontend        = None   # receives messages
        self.bind_address    = None   
        self.backends        = []
        self.addresses       = backend_addresses    
        self.grouping_fields = fields
        self.grouping_policy = policy

        # controller related settings
        self.create_time     = time.time()
        self.loop_count      = 0
        self.controller      = None
        self.controller_address = controller_address

        self.type            = type
        if self.type not in [TYPE_SPOUT, TYPE_BOLT, TYPE_OUTLET, TYPE_MINT]:
            raise NotImplementedError()

        
    def bind(self):
        """ bind address & notify controller """
        self.context = zmq.Context()
        # bind a port mainly for rpc call
        self.rpc             = self.context.socket(zmq.REP)
        self.rpc_address     = "tcp://0.0.0.0"
        port                 = self.rpc.bind_to_random_port(self.rpc_address)
        self.rpc_address    += ":{0}".format(port)
        self.logger.debug(type(self).__name__ + " binded rpc at " + self.rpc_address)

        # bind itself to some port for listening and then tell the controller about this info
        if self.type in [TYPE_BOLT, TYPE_OUTLET]:
            self.frontend        = self.context.socket(zmq.PULL)
            self.bind_address    = "tcp://0.0.0.0"
            port                 = self.frontend.bind_to_random_port(self.bind_address)
            self.bind_address   += ":{0}".format(port)
            self.logger.debug(type(self).__name__ + " binded at " + self.bind_address)

        self.controller = self.context.socket(zmq.PUSH)
        self.controller.connect(self.controller_address)
        self.ping_controller()

    def ping_controller(self):
        data = self.get_status()
        self.controller.send(pack(data))

    def get_status(self):
        return {
            "pid":              os.getpid(),
            "type":             self.type,
            "uuid":             self.uuid,
            "time":             time.time(),
            "worker_name":      self.worker_name,
            "rpc_address":      self.rpc_address,
            "bind_address":     self.bind_address,
            "backend_addresses":self.addresses,
            "loop_count":       self.loop_count,
            "cpu_percent":      time.clock()/(time.time()-self.create_time),
        }

    def run(self):
        """ runs the worker """
        self.bind()
        self.connect(self.addresses)

        poller = zmq.Poller()
        if self.frontend:
            poller.register(self.frontend, zmq.POLLIN)
        if self.rpc:
            poller.register(self.rpc, zmq.POLLIN)

        def worker_only():
            while not self.__stopped:
                self._process_worker()

        if not self.frontend:
            import threading
            threading.Thread(target=worker_only).start()

        while not self.__stopped:
            socks = dict(poller.poll(50))
            if socks.get(self.frontend) == zmq.POLLIN:
                self._process_worker()
            elif socks.get(self.rpc) == zmq.POLLIN:
                self._process_rpc()

    def _process_rpc(self):
        try:
            # func, args,
            req = self.rpc.recv()

            ret = {}
            m = re.compile(r'(.*?)\((.*?)\)').search(req)            
            if m:
                func, args = m.group(1), m.group(2)
                if args:
                    raise NotImplementedError()
                else:
                    ret.update( getattr(self, func)() )
            else:
                ret = {"status":"invalid request"}
            
            resp = pack(ret)
            self.rpc.send(resp)
        except Exception, e:
            if not self.__stopped:
                self.logger.exception(e.message)

    def _process_worker(self):
        try:
            if self.type in [TYPE_SPOUT, TYPE_MINT]:
                self.results = self.execute()
            else:
                self.packed_dict  = self.frontend.recv()
                kwargs            = unpack(self.packed_dict)
                self.results      = self.execute(**kwargs)

            if self.type in [TYPE_OUTLET, TYPE_MINT]:
                # for outlets/mint, we don't need to push our messages further
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

    def execute(self, **kwargs):
        if self._not_throttled():
            ret = None
            try:
                ret = self._execute(self, **kwargs)
            except Exception, e:
                self.logger.exception("Execution Error: <{0}>".format(e.message))
            else:
                self._executed()
            return ret

    def stop(self):
        self.__stopped = True
        if self.rpc:
            self.rpc.close()
        if self.frontend:
            self.frontend.close()
        status = self.get_status()
        return {"stopped":True, "status":status}

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

class Controller(object):
    """ Schedules worker creates/stops/executes
    
    * schedule workers
    * monitor workers
    """
    def __init__(self):
        self.logger = logging.getLogger("api.Controller")
        self.context = zmq.Context()
        self.workers = {}        # uuid -> Controller

        # listens to pings
        self.ping_backend = None
        self.ping_address = None
        self._receiver_running = True
        threading.Thread(target=self.ping_receiver).start()
        
        # let ping receiver initialize first
        while not self.ping_address:
            time.sleep(0.05)

    def get_all_stats(self):
        return self._rpc_all('get_status()')

    def _rpc_all(self, cmd):
        clients = {}
        poller = zmq.Poller()

        ret = []
        for k, d in self.workers.items():
            socket = self.context.socket(zmq.REQ)
            socket.setsockopt(zmq.LINGER, 0)
            socket.connect(d['rpc_address'])
            poller.register(socket, zmq.POLLIN)
            socket.send(cmd)
            clients[socket] = k

        t = time.time()
        while time.time() - t < 1.000:
            socks = dict(poller.poll(50)) # wait 0.05s
            for socket in socks.keys():
                status = unpack(socket.recv())
                self.workers[clients[socket]] = status
                ret.append(status)
                del clients[socket]
            if not clients:
                break

        # timeouted sockets
        for k, socket in clients.items():
            status = {"status":"no response"} 
            if k in self.workers:
                status.update( self.workers[k] )
            ret.append(status)

        return ret

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
            elif req.get("op") == "stop_all":
                response.update({"status":"ok"})
                response.update({"data":self.stop_workers()})
            elif req.get("op") == "add_worker":
                response.update({"status":"ok"})
                response.update({"data":self.add_worker(req.get("worker_name"), backends=req.get("backends"))})
            else:
                response.update({"status":"error","message":"op code {0} error/not found".format(req.get("op"))})
            
        return pack(response)


    def is_added(self, initial_uuids, worker_name):
        added_workers = set(self.workers.keys()) - set(initial_uuids)
        added = False
        added_info = {}
        for w in added_workers:
            if self.workers[w].get("worker_name") == worker_name and (not self.workers[w].get("recorded", False)):
                added = True
                added_info.update(self.workers[w])
                self.workers[w]['recorded'] = True
                break
        return added, added_info

    def add_worker(self, worker_name, backends=[]):
        " add/start a worker based on its name "
        code = open(os.path.join("workers", worker_name+".py")).read()
        try:
            exec(code)
        except Exception, e:
            self.logger.error("worker {0} cannot execute: {1}".format(worker_name, e.message))
        else:
            try:
                t = locals().get("worker_type")
                f = locals().get("execute")
                c = locals().get("configs")
                s = locals().get("setup")
                p = locals().get("policy", SHUFFLE_GROUPING)
                f = locals().get("fields", [])
            except Exception, e:
                self.logger.exception(e.message)
            else:
                uuids = self.workers.keys()
                w = Worker(type=t, execute=f, configs=c, setup=s, policy=p, fields=f,
                        controller_address=self.ping_address, backend_addresses=backends, worker_name=worker_name)
                w.start()

                # wait until we got pinged
                t = time.time()

                while time.time() - t < 1.0:
                    time.sleep(0.05)
                    added, added_info = self.is_added(uuids, worker_name)
                    if added:
                        break

                return {"worker_status":added_info}

        return {"worker_status":{}}

    def check_health(self):
        """ do a health check and auto recovery

        1. check health
        2. stop "no response" workers by uuid
        3. start those workers by name
        """
        # TODO implement it
        pass

    def stop_worker_by_uuid(self):
        # TODO stop worker by uuid
        raise NotImplementedError()

    def start_workers(self, name_backends=None):
        """ basically add workers one by one """
        if name_backends:
            for name, backends in name_backends:
                self.add_worker(name, backends)
        else:
            if not os.path.exists("workers"):
                self.logger.warning("workers directory does not exist")
                return

            self.logger.warning("no backends info available, this mode should only used in debuging")
            for path in os.listdir("workers"):
                if path.endswith(".py"): 
                    worker_name = path[:-3]
                    info = self.add_worker(worker_name)

    def stop_workers(self):
        return self._rpc_all('stop()')

    def reload_workers(self):
        """ reload all workers from workers subdir
    
        * each worker lives in a .py file
        * each worker has a `execute` method and a `configs` dict
        """
        # TODO reimplement this
        pass

    def ping_receiver(self):
        """ recieves ping from workers, record ping info """
        context              = zmq.Context()
        self.ping_backend    = context.socket(zmq.PULL)
        self.ping_address    = "tcp://0.0.0.0"
        port                 = self.ping_backend.bind_to_random_port(self.ping_address)
        self.ping_address   += ":{0}".format(port)

        self.logger.debug(type(self).__name__ + " binded at " + self.ping_address)

        poller = zmq.Poller()
        poller.register(self.ping_backend, zmq.POLLIN)

        while self._receiver_running:
            socks = dict(poller.poll(100))
            if socks.get(self.ping_backend) == zmq.POLLIN:
                message_packed = self.ping_backend.recv(zmq.NOBLOCK)
                d = unpack(message_packed)
                d["time"] = time.time()
                self.logger.debug("received worker ping: {0}".format(repr(d)))
                self.workers[d['uuid']] = d

if __name__ == "__main__":
    c = Controller()
    c.start_workers()
    while True:
        time.sleep(5)
        r = c.request(pack({"op":"all_stats"}))
        for x in unpack(r)['data']:
            print x
        #c.reload_workers()
