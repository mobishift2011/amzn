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
from settings import PEERS, ENV_NAME
from fabric.api import *

@parallel
@hosts(PEERS)
def setup_env():
    """ Setup environment for pystorm
    
    A ubuntu 12.04 or later distribution of linux is required
    """
    run("apt-get -y install build-essential python-dev libevent-dev libxslt-dev uuid-dev python-setuptools dtach")
    run("easy_install pip")
    run("pip install virtualenvwrapper")
    run("mkdir -p /opt/pystorm")
    with cd("/opt/pystorm"):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            run("mkvirtualenv "+ENV_NAME)
            with prefix("workon "+ENV_NAME):
                run("pip install cython")
                run("pip install zerorpc gevent lxml requests") 

def run_code(host_string, code, filename="code.py"):
    """ Run a code block on a specific host

    :param host_string: a host_string required by fabric
    :param code: an executable code block 
    :param filename: filename that will hold the code on the host

    Example::

    >>> run_code("root@192.168.1.1", '''from test.pystone import pystones\\npystones()''')

    """
    try:
        compile(code, '<string>', 'exec')
    except:
        raise ValueError("Code Cannot Compile")
    else:
        with settings(host_string=host_string):
            # kill if we already have that program running
            stop_code(host_string, filename)

            # save & upload & dtach the code file
            open("/tmp/"+filename,"w").write(code)
            with cd("/opt/pystorm"):
                put("/tmp/"+filename, filename)
                with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
                    with prefix("workon "+ENV_NAME):
                        _runbg("python "+filename, sockname="code")

def stop_code(host_string, filename="code.py"):
    """ Stop a running script on host
    """
    with settings(host_string=host_string, warn_only=True):
        run("rm /tmp/{0}.sock".format("code"))
        run("kill -9 `pgrep -f {0}`".format(filename))

def _runbg(cmd, sockname="dtach"):
    """ A helper function to run command in background """
    return run('dtach -n /tmp/{0}.sock {1}'.format(sockname,cmd))

if __name__ == "__main__":
    run_code("root@192.168.56.102", """#!/usr/bin/env python
import time

c = 0
while True:
    c += 1
    open("/tmp/test","a").write(str(c)+"\\n")
    time.sleep(1)
""")
