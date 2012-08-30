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

logger = logging.getLogger("api")

class Worker(object):
    """ Worker class to execute some code 
    
    * do some basic statistics
    * respond to controller's ping request
    * throttled subject to configs
    """
    default_configs = {
        'num_coroutines' : 1,   # num of concurrently running greenlets
        'qps_limit'      : 0,   # 0 -> not limiting, not implemented yet
    }
    def __init__(self, execute, configs = {}):
        self.execute = execute
        self.configs = default_configs
        self.configs.update(configs)
        self.logger = logging.getLogger("api.Worker")
        
    def execute(self, *args, **kwargs):
        if self._not_throttled():
            try:
                self.execute(*args, **kwargs)
            except Exception, e:
                self.logger.exception(e.message)
            else:
                self._executed()

    def stop(self):
        pass

    def _not_throttled(self):
        # TODO implement throttling
        return True

    def _executed(self):
        # TODO implement statistics
        pass

class Controller(object):
    """ Controls worker executes
    
    * schedule workers
    * monitor workers
    """
    workers = []
    def __init__(self):
        self.logger = logging.getLogger("api.Controller")
        
    def start_workers(self):
        self.reload_workers()

    def request(self, request):
        """ processing request
    
        {"op":"all_stats"} -> a dict or stats
        """
        response = ""
        return response

    def stop_workers(self):
        workers = Controller.workers
        for w in workers:
            w.stop()

    def reload_workers(self):
        """ reload all workers from workers subdir
    
        * each worker lives in a .py file
        * each worker has a `execute` method and a `configs` dict
        """
        if not os.path.exists("workers"):
            self.logger.warning("workers directory does not exist")
            return

        for path in os.listdir("workers"):
            if path.endswith(".py"): 
                code = open(path).read()
                try:
                    exec(code)
                except Exception, e:
                    self.logger.error("worker {0} cannot exec {1}".format(path, e.message))
                else:
                    w = locals().get("execute")
                    c = locals().get("configs")
