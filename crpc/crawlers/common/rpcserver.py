#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.common.rpcserver
~~~~~~~~~~~~~~~~~~~~~~~~~

Provides a meta programmed integrated RPC call for all callers

"""
from settings import RPC_PORT, CRPC_ROOT

from os import listdir
from os.path import join, abspath, dirname, isdir

from helpers import log

class RPCServer(object):
    """ :py:class:crawlers.common.rpcserver.RPCServer
    
    gathers information in crawlers/crawlername/server.py 
    generates callback for remote procedure call
    
    >>> zs = Zerorpc.Server(RPCServer()) 
    >>> zs.bind("tcp://0.0.0.0:{0}".format(RPC_PORT))
    >>> zs.run()

    To wrap certain crawler in RPCServer, we define the following rules for service:

    -  a service should  be inside unique  directory under ``crawlers``
    -  there should be a ``server.py`` inside that directory
    -  a class named "Server" must exists in that file
    """
    def __init__(self):
        excludes = ['common']
        self.logger = log.getlogger("crawlers.common.rpcserver.RPCServer")
        self.crawlers = []
        for name in listdir(join(CRPC_ROOT, "crawlers")):
            path = join(CRPC_ROOT, "crawlers", name)
            if name not in excludes and isdir(path):
                self.is_service_defined(name)
                self.crawlers.append( (name, path) ) 

    def is_service_defined(self, name):
        """ Given name of a crawler, determine whether there's valid service inside it 

        :param str name: name of the crawler's directory
        :rtype: bool
        """ 
        try:
            m = __import__("crawlers."+name+".server", fromlist=['Server'])
            print m.Server()
        except Exception as e:
            self.logger.exception(e.message)
            return False
        else:
            return True

if __name__ == "__main__":
    RPCServer()
