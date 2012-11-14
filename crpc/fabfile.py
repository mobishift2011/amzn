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
    run("apt-get -y install build-essential python-dev libevent-dev libxslt-dev uuid-dev python-setuptools dtach libzmq-dev redis-server chromium-browser xvfb unzip")
    run("easy_install pip")
    run("pip install virtualenvwrapper")
    run("mkdir -p /opt/crpc")
    run("wget -q -c http://chromedriver.googlecode.com/files/chromedriver_linux64_23.0.1240.0.zip -O tmp.zip && unzip tmp.zip && rm tmp.zip")
    run("chmod a+x chromedriver && mv chromedriver /usr/bin/")

    with settings(warn_only=True):
        run("killall chromedriver")
        run("kill -9 `pgrep -f rpcserver`")
        #run("kill -9 `pgrep -f {0}`".format(ENV_NAME))
        run("ln -s /usr/bin/chromium-browser /usr/bin/google-chrome")

    with cd("/opt/crpc"):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
#            run("mkvirtualenv "+ENV_NAME)
            with prefix("workon "+ENV_NAME):
                run("pip install cython"+USE_INDEX)
                run("pip install https://github.com/SiteSupport/gevent/tarball/master")
                run("pip install zerorpc lxml requests pymongo mongoengine redis redisco pytz mock selenium blinker cssselect"+USE_INDEX) 

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

def restart_rpc():
    import multiprocessing
    tasks = []
    for host_string in PEERS:
        t = multiprocessing.Process(target=_restart_rpc, args=(host_string,))
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

    _restart_rpc(host_string)

def _restart_rpc(host_string):
    # remove if already exists
    with settings(host_string=host_string, warn_only=True):
        run("killall -9 Xvfb")
        run("killall chromedriver")
        run("kill -9 `pgrep -f rpcserver`")
        run("pkill -9 python")
        run("killall chromium-browser")
        run("rm /tmp/*.sock")
        run("sleep 3")

    # dtach rpc @ /tmp/rpc.sock
    with settings(host_string=host_string):
        with cd("/opt/crpc/crawlers/common"):
            with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
                with prefix(". ../../env.sh {0}".format(os.environ['ENV'])):
                    with prefix("ulimit -s 1024"):
                        with prefix("ulimit -n 4096"):
                            _runbg("Xvfb :99 -screen 0 1024x768x8 -ac +extension GLX +render -noreset", sockname="graphicXvfb")
                            with prefix("export DISPLAY=:99"):
                                _runbg("python rpcserver.py", sockname="crawlercommon")

def _runbg(cmd, sockname="dtach"):
    """ A helper function to run command in background """
    return run('dtach -n /tmp/{0}.sock {1}'.format(sockname, cmd))


def deploy_monitor():
    local("sh deploy_monitor.sh")
#    deploy_root = '/home/deploy/projects/amzn/crpc'
#    with settings(warn_only=True):
#        local("kill -9 `pgrep -f run.py`")
#        local("kill -9 `pgrep -f main.py`")
#    _deploy_monitor_run(deploy_root)
#
#def _deploy_monitor_run(deploy_root):
#    with lcd(deploy_root):
#        with prefix(". env.sh TEST"):
#            local("ulimit -n 4096 && dtach -n /tmp/monitormain.sock python backends/webui/main.py")


if __name__ == "__main__":
    import resource
    resource.setrlimit(resource.RLIMIT_NOFILE, (4096, 4096))

