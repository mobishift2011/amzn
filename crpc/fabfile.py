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
from settings import PEERS, CRAWLER_PEERS, POWER_PEERS, ENV_NAME, USE_INDEX
from settings import CRPC_ROOT

from fabric.api import *
from fabric.contrib.files import exists

import os
import sys
import time
import multiprocessing

@parallel
@hosts(PEERS)
def setup():
    """ Setup environment for crpc
    
    A ubuntu 12.04 or later distribution of linux is required
    """
    run("apt-get update")
    run("apt-get -y upgrade")
    run("apt-get -y install build-essential python-dev libevent-dev libxslt-dev uuid-dev python-setuptools dtach libzmq-dev redis-server chromium-browser xvfb unzip")
    run("easy_install pip")
    run("pip install virtualenvwrapper")
    run("mkdir -p /opt/crpc")
    
    if not exists('/usr/bin/chromedriver'):
        run("wget -q -c http://chromedriver.googlecode.com/files/chromedriver_linux64_23.0.1240.0.zip -O tmp.zip && unzip tmp.zip && rm tmp.zip")
        run("chmod a+x chromedriver && mv chromedriver /usr/bin/")

    with settings(warn_only=True):
        run("killall chromedriver")
        run("kill -9 `pgrep -f crawlerserver`")
        run("kill -9 `pgrep -f powerserver`")
        #run("kill -9 `pgrep -f {0}`".format(ENV_NAME))
        run("ln -s /usr/bin/chromium-browser /usr/bin/google-chrome")

    with cd("/opt/crpc"):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            run("mkvirtualenv "+ENV_NAME)
            with prefix("workon "+ENV_NAME):
                run("pip install cython"+USE_INDEX)
                run("pip install https://github.com/SiteSupport/gevent/tarball/master")
                run("pip install zerorpc lxml requests pymongo mongoengine redis redisco pytz mock selenium blinker cssselect boto python-dateutil virtualenvwrapper"+USE_INDEX) 

@parallel
@hosts(PEERS)
def deploy():
    """ deploy crawler&api server code to remotes """
    execute(stop)
    # copy files
    with settings(warn_only=True):
        local('find {0} -name "*.pyc" -delete'.format(CRPC_ROOT))
        run("rm -rf /opt/crpc")
        run("mkdir -p /opt/crpc")
        put(CRPC_ROOT+"/*", "/opt/crpc/")
    execute(restart)

def stop():
    # TODO should implement better stopping mechanism
    execute(_stop_crawler)
    execute(_stop_power)
    execute(_stop_monitor)

def start():
    """ start remote executions """
    execute(_start_crawler)
    execute(_start_power)
    execute(_start_monitor)

def restart():
    """ stop & start """
    execute(stop)
    sys.stdout.write('sleeping for 3 seconds.')
    sys.stdout.flush()
    for _ in range(3):
        time.sleep(1)
        sys.stdout.write('.')
        sys.stdout.flush()
    sys.stdout.write('\n\n\n')
    sys.stdout.flush()
    execute(start)

@parallel
@hosts(CRAWLER_PEERS)
def _stop_crawler():
    with settings(warn_only=True):
        run("killall Xvfb")
        run("killall chromedriver")
        run("killall chromium-browser")
        run("kill -9 `pgrep -f rpcserver.py`")
        run("kill -9 `pgrep -f crawlerserver.py`")
        run("rm /tmp/*.sock")

@parallel
@hosts(CRAWLER_PEERS)
def _start_crawler():
    _runbg("Xvfb :99 -screen 0 1024x768x8 -ac +extension GLX +render -noreset", sockname="graphicXvfb")
    with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
        with prefix("ulimit -s 1024"):
            with prefix("ulimit -n 4096"):
                with cd("/opt/crpc"):
                    with prefix("source ./env.sh {0}".format(os.environ.get('ENV',''))):
                        with prefix("export DISPLAY=:99"):
                            _runbg("python crawlers/common/crawlerserver.py", sockname="crawlerserver")

@parallel
@hosts(POWER_PEERS)
def _start_power():
    with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
        with prefix("ulimit -s 1024"):
            with prefix("ulimit -n 4096"):
                with cd("/opt/crpc"):
                    with prefix("source ./env.sh {0}".format(os.environ.get('ENV',''))):
                        _runbg("python powers/powerserver.py", sockname="powerserver")

@parallel
@hosts(POWER_PEERS)
def _stop_power():
    with settings(warn_only=True):
        run("kill -9 `pgrep -f apiserver.py`")
        run("kill -9 `pgrep -f powerserver.py`")
        run("rm /tmp/*.sock")

def _start_monitor():
    os.system("ulimit -n 4096 && cd {0}/backends/monitor && dtach -n /tmp/crpcscheduler.sock python run.py".format(CRPC_ROOT))
    os.system("cd {0}/backends/webui && dtach -n /tmp/crpcwebui.sock python main.py".format(CRPC_ROOT))

def _stop_monitor():
    os.system("kill -9 `pgrep -f run.py`")
    os.system("kill -9 `pgrep -f main.py`")
    os.system("rm /tmp/crpc*.sock")

def _runbg(cmd, sockname="dtach"):
    """ A helper function to run command in background """
    return run('dtach -n /tmp/{0}.sock {1}'.format(sockname, cmd))

if __name__ == "__main__":
    import resource
    resource.setrlimit(resource.RLIMIT_NOFILE, (4096, 4096))

