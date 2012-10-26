#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawlers.common.rpcserver
~~~~~~~~~~~~~~~~~~~~~~~~~

Provides a meta programmed integrated RPC call for all callers

"""
from settings import RPC_PORT, CRPC_ROOT, MONGODB_HOST
from os import listdir
from os.path import join, abspath, dirname, isdir
from helpers import log

from gevent.coros import Semaphore
lock = Semaphore()
from selenium.common.exceptions import *
import lxml.html
import requests
import urllib

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
        excludes = ['common', 'ecost', 'bhphotovideo', 'bestbuy', 'dickssport', 'overstock', 'cabelas', 'ruelala', 'bluefly' ]
        self.logger = log.getlogger("crawlers.common.rpcserver.RPCServer")
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

    def call(self, crawler, method, args, kwargs):
        """ this is a router function for crawlers """
        service = self.crawlers[crawler]

        if service:
            return getattr(service, method)(*args, **kwargs)
        else:
            raise ValueError("{crawler} does not seems to a valid crawler".format(**locals()))


def safe_lock(func,*arg,**kwargs):
    def wrapper(*arg,**kwargs):
        lock.acquire()
        res = func(*arg,**kwargs)
        lock.release()
        return res
    return wrapper

class BaseServer:
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    siteurl = ''
    email = 'huanzhu@favbuy.com'
    passwd = '4110050209'
    session = requests.session()
    session.headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
                        'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 '}

    def bopen(self,url):
        """ open url with browser
        """
        try:
            self.browser.get(url)
        except TimeoutException:
            return False
        else:
            self.html = self.browser.content
            self.tree = lxml.html.fromstring(self.html)
            return True

    def ropen(self,url):
        """ open url with requests
        """
        res = self.session.get(url)
        status_code = res.status_code

        if status_code in [200,301]:
            self.html = res.text
            self.tree = lxml.html.fromstring(self.html)
            return self.tree
        else:
            raise HttpError(status_code,url)

    def login(self, email=None, passwd=None):
        pass
    
    @safe_lock
    def crawl_category(self,*args,**kwargs):
        """.. :py:method::
            From top depts, get all the events
        """
        pass

    @safe_lock
    def crawl_listing(self,sale_id,event_url):
        pass

    @safe_lock
    def crawl_product(self,product_id,product_url):
        pass

    def format_url(self,url):
        if url.startswith('http://'):
            return url
        else:
            return  urllib.basejoin(self.siteurl,url)

if __name__ == '__main__':
    server = Server()

