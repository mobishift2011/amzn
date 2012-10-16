#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Fabfile 

* Note, ubuntu 12.04 or later is required for this to work

fabric is used to:
    1. automate environment setups
    2. deploy python code on remote machine and run

this module should not consider the following:
    1. monitor the code runs on remote machine
"""
from settings import PEERS, ENV_NAME, USE_INDEX
from settings import CRPC_ROOT
from fabric.api import *
import os

@parallel
@hosts(PEERS)
def setup_env():
    """ Setup environment for crpc
    
    A ubuntu 12.04 or later distribution of linux is required
    """
    run("apt-get update")
    run("apt-get -y upgrade")
    run("apt-get -y install build-essential python-dev libevent-dev libxslt-dev uuid-dev python-setuptools dtach libzmq-dev redis-server")
    run("easy_install pip")
    run("pip install virtualenvwrapper")
    run("mkdir -p /opt/crpc")

    with settings(warn_only=True):
        run("kill -9 `pgrep -f rpc.py`")
        run("kill -9 `pgrep -f {0}`".format(ENV_NAME))

    with cd("/opt/crpc"):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            run("mkvirtualenv "+ENV_NAME)
            with prefix("workon "+ENV_NAME):
                run("pip install cython"+USE_INDEX)
                run("pip install zerorpc lxml requests pymongo mongoengine redis redisco"+USE_INDEX) 

def deploy_rpc():
    """ deploy rpc server code to host """
    import multiprocessing
    tasks = []
    for host_string in PEERS:
        t = multiprocessing.Process(target=_deploy_rpc, args=(host_string,))
        tasks.append(t)
        t.start()

    for t in tasks:
        t.join()

def deploy_local():
    """ copy files to local dir """
    with settings(warn_only=True):
        local('find {0} -name "*.pyc" -delete'.format(CRPC_ROOT))
        local("rm -rf /opt/crpc")
        local("mkdir -p /opt/crpc")
        local("cp -r {0}/* /opt/crpc".format(CRPC_ROOT))

def _deploy_rpc(host_string):
    """ deploy rpc server code to host """
    crawlers = os.listdir(os.path.join(CRPC_ROOT, "crawlers"))
    crawlers = [ x for x in crawlers if os.path.isdir(os.path.join(CRPC_ROOT, "crawlers", x)) ]

    # copy files
    with settings(host_string=host_string, warn_only=True):
        local('find {0} -name "*.pyc" -delete'.format(CRPC_ROOT))
        run("rm -rf /opt/crpc")
        run("mkdir -p /opt/crpc")
        put(CRPC_ROOT+"/*", "/opt/crpc/")

    # remove if already exists
    with settings(host_string=host_string, warn_only=True):
        run("pkill -9 python")
        run("rm /tmp/*.sock")

    # dtach rpc @ /tmp/rpc.sock
    with settings(host_string=host_string):
        for name in crawlers:
            with cd(os.path.join("/opt/crpc/crawlers", name)):
                with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
                    with prefix("workon "+ENV_NAME):
                        with prefix("ulimit -s 1024"):
                            with prefix("ulimit -n 4096"):
                                _runbg("python server.py", sockname=name)

def _runbg(cmd, sockname="dtach"):
    """ A helper function to run command in background """
    return run('dtach -n /tmp/{0}.sock {1}'.format(sockname,cmd))

def amazon_listing():
    import time
    from crawlers.amazon.client import RPC_PORT, crawl_listing, crawl_product
    peers = [ "tcp://{0}:{1}".format(x.split('@')[-1], RPC_PORT) for x in PEERS ]
    while True:
        t = time.time()
        crawl_listing(peers)
        print time.time() - t
        time.sleep(3600)

def amazon_product():
    import time
    from crawlers.amazon.client import RPC_PORT, crawl_listing, crawl_product
    peers = [ "tcp://{0}:{1}".format(x.split('@')[-1], RPC_PORT) for x in PEERS ]
    while True:
        t = time.time()
        crawl_product(peers)
        print time.time() - t
        time.sleep(3600)

def newegg_product():
    import time
    from crawlers.newegg.client import RPC_PORT, crawl_product
    peers = [ "tcp://{0}:{1}".format(x.split('@')[-1], RPC_PORT) for x in PEERS ]
    while True:
        t = time.time()
        crawl_product(peers)
        print time.time() - t
        time.sleep(3600)
try:
    from crawlers.bestbuy.client import crawl_category as bestbuy_category
    from crawlers.bhphotovideo.client import crawl_category as bhphotovideo_category
    from crawlers.dickssport.client import crawl_category as dickssport_category
except:
    pass

def bestbuy_listing():
    import time
    from crawlers.bestbuy.client import RPC_PORT, crawl_category, crawl_listing, crawl_product
    peers = [ "tcp://{0}:{1}".format(x.split('@')[-1], RPC_PORT) for x in PEERS ]
    while True:
        t = time.time()
        crawl_listing(peers)
        print 'Crawl listing cost: {0} seconds.'.format(time.time() - t)
        bestbuy_product()
        time.sleep(3600)

def bestbuy_product():
    """ suggest to run bestbuy_listing(), we can crawl all of the fields.
    """
    import time
    from crawlers.bestbuy.client import RPC_PORT, crawl_category, crawl_listing, crawl_product
    peers = [ "tcp://{0}:{1}".format(x.split('@')[-1], RPC_PORT) for x in PEERS ]
    t = time.time()
    crawl_product(peers)
    print 'Crawl product cost: {0} seconds.'.format(time.time() - t)


def dickssport_listing():
    import time
    from crawlers.dickssport.client import RPC_PORT, crawl_category, crawl_listing, crawl_product
    peers = [ "tcp://{0}:{1}".format(x.split('@')[-1], RPC_PORT) for x in PEERS ]
    while True:
        t = time.time()
        crawl_listing(peers)
        print 'Crawl listing cost: {0} seconds.'.format(time.time() - t)
        dickssport_product()
        time.sleep(3600)

def dickssport_product():
    """ suggest to run dickssport_listing(), we can crawl all of the fields.
    """
    import time
    from crawlers.dickssport.client import RPC_PORT, crawl_category, crawl_listing, crawl_product
    peers = [ "tcp://{0}:{1}".format(x.split('@')[-1], RPC_PORT) for x in PEERS ]
    t = time.time()
    crawl_product(peers)
    print 'Crawl product cost: {0} seconds.'.format(time.time() - t)

def dickssport_update(*targs):
    """ update product with specific fields
        useful_param = ['price', 'available', 'shipping', 'rating', 'reviews']
    """
    import time
    from crawlers.dickssport.client import RPC_PORT, crawl_category, crawl_listing, crawl_product, update_product
    peers = [ "tcp://{0}:{1}".format(x.split('@')[-1], RPC_PORT) for x in PEERS ]
    t = time.time()
    update_product(peers, *targs)
    print 'Update product cost: {0} seconds.'.format(time.time() - t)


if __name__ == "__main__":
    pass
