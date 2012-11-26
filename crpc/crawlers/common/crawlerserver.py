#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.common.rpcserver
~~~~~~~~~~~~~~~~~~~~~~~~~

Provides a meta programmed integrated RPC call for all callers

"""
from gevent import monkey; monkey.patch_all()
from settings import CRAWLER_PORT, CRPC_ROOT, MONGODB_HOST
from os import listdir
from os.path import join, abspath, dirname, isdir
from helpers import log
        
import lxml.html
import requests
import urllib
import time
import zerorpc

class CrawlerServer(object):
    """ :py:class:crawlers.common.crawlerserver.CrawlerServer
    
    gathers information in crawlers/crawlername/server.py 
    generates callback for remote procedure call
    
    >>> zs = zerorpc.Server(CrawlerServer()) 
    >>> zs.bind("tcp://0.0.0.0:{0}".format(CRAWLER_PORT))
    >>> zs.run()

    To wrap certain crawler in CrawlerServer, we define the following rules for service:

    -  a service should  be inside unique  directory under ``crawlers``
    -  there should be a ``server.py`` inside that directory
    -  a class named "Server" must exists in that file
    """
    def __init__(self):
        excludes = ['common', 'ecost', 'bhphotovideo', 'bestbuy', 'dickssport', 'overstock', 'cabelas']
        self.logger = log.getlogger("crawlers.common.rpcserver.CrawlerServer")
        self.crawlers = {}
        for name in listdir(join(CRPC_ROOT, "crawlers")):
            path = join(CRPC_ROOT, "crawlers", name)
            if name not in excludes and isdir(path):
                service = self.get_service(name)
                if service:
                    self.crawlers[name] = service

    def get_service(self, name):
        """ Given name of a crawler, determine whether there's valid service inside it 

        :param str name: name of the crawler's directory
        :rtype: None or Class
        """ 
        try:
            m = __import__("crawlers."+name+".server", fromlist=['Server'])
            service = m.Server()
        except Exception as e:
            self.logger.exception(e.message)
        else:
            return service

    def call(self, crawler, method, args=(), kwargs={}):
        """ this is a router function for crawlers """
        service = self.crawlers[crawler]
        if service:
            return getattr(service, method)(*args, **kwargs)
        else:
            raise ValueError("{crawler} does not seems to a valid crawler".format(**locals()))
    
if __name__ == '__main__':
    zs = zerorpc.Server(CrawlerServer()) 
    zs.bind("tcp://0.0.0.0:{0}".format(CRAWLER_PORT))
    zs.run()
