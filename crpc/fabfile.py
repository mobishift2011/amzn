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
from settings import PEERS, CRAWLER_PEERS, POWER_PEERS, TEXT_PEERS, ENV_NAME, USE_INDEX
from settings import CRPC_ROOT

from fabric.api import *
from fabric.contrib.files import exists
from fabric.contrib.project import rsync_project, upload_project

import os
import sys
import time
import multiprocessing

HOSTS = list(set([ p['host_string'] for p in  PEERS ]))

@parallel
@hosts(HOSTS)
def setup():
    """ Setup environment for crpc
    
    A ubuntu 12.04 or later distribution of linux is required
    """
    run("apt-get update")
    run("apt-get -y upgrade")
    run("apt-get -y install build-essential python-dev libevent-dev libxslt-dev uuid-dev python-setuptools dtach libzmq-dev redis-server chromium-browser xvfb unzip libjpeg8-dev gfortran libblas-dev liblapack-dev ganglia-monitor")
    run("apt-get -y build-dep python-imaging")
    run("ln -sf /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/")
    run("ln -sf /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/")
    run("ln -sf /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/")
    run("easy_install pip")
    run("pip install virtualenvwrapper")
    run("mkdir -p /opt/crpc")
    
    if not exists('/usr/bin/chromedriver'):
        run("wget -q -c http://chromedriver.googlecode.com/files/chromedriver_linux64_23.0.1240.0.zip -O tmp.zip && unzip tmp.zip && rm tmp.zip")
        run("chmod a+x chromedriver && mv chromedriver /usr/bin/")
        run("ln -s /usr/bin/chromium-browser /usr/bin/google-chrome")

    with settings(warn_only=True):
        run("killall chromedriver")
        run("kill -9 `pgrep -f crawlerserver`")
        run("kill -9 `pgrep -f powerserver`")
        #run("kill -9 `pgrep -f {0}`".format(ENV_NAME))

    with cd("/opt/crpc"):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            run("mkvirtualenv "+ENV_NAME)
            with prefix("workon "+ENV_NAME):
                run("pip install cython"+USE_INDEX)
                run("pip install numpy"+USE_INDEX)
                run("pip install scipy"+USE_INDEX)
                run("pip install scikit-learn pattern"+USE_INDEX)
                # The ez_setup is required for titlecase.
                run("pip install ez_setup"+USE_INDEX)

                if 'gevent==1.0' not in run("pip freeze|grep gevent").stdout:
                    run("pip install https://github.com/SiteSupport/gevent/tarball/master")
                run("pip install zerorpc lxml requests pymongo mongoengine redis redisco pytz Pillow titlecase mock selenium blinker cssselect boto python-dateutil virtualenvwrapper slumber esmre django supervisor"+USE_INDEX) 

def run_supervisor():
    """ let run.py not down """
    local("supervisord -c /srv/crpc/supervisord.conf -l /tmp/supervisord.log")

def deploy():
    """ deploy crawler&api server code to remotes """
    execute(stop)
    execute(copyfiles)
    execute(start)

@parallel
@hosts(HOSTS)
def copyfiles():
    """ rebuild the whole project directory on remotes """
    # copy files
    with settings(warn_only=True):
        local('find {0} -name "*.pyc" -delete'.format(CRPC_ROOT))
        run("rm -rf /opt/crpc")
        run("mkdir -p /opt/crpc")
        #put(CRPC_ROOT+"/*", "/opt/crpc/")
        upload_project(CRPC_ROOT+'/', '/opt/')

def stop():
    # TODO should implement better stopping mechanism
    execute(_stop_all)
    execute(_stop_monitor)
    execute(_stop_publish)
    execute(_stop_catalog)
    execute(_stop_admin)

def start():
    """ start remote executions """
#    execute(_start_xvfb)
    execute(_start_crawler)
    execute(_start_power)
    execute(_start_text)
    execute(_start_monitor)
    execute(_start_publish)
    execute(_start_catalog)
    execute(_start_admin)

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
@hosts(HOSTS)
def _stop_all():
    with settings(warn_only=True):
        run("killall Xvfb")
        run("killall chromedriver")
        run("killall chromium-browser")
        run("kill -9 `pgrep -f crawlerserver.py`")
        run("kill -9 `pgrep -f powerserver.py`")
        run("kill -9 `pgrep -f textserver.py`")
        run("ps aux | grep crawlerserver.py | grep -v grep | awk '{print $2}' | xargs kill -9")
        run("ps aux | grep powerserver.py | grep -v grep | awk '{print $2}' | xargs kill -9")
        run("ps aux | grep textserver.py | grep -v grep | awk '{print $2}' | xargs kill -9")
        run("rm /tmp/*.sock")

@parallel
@hosts(HOSTS)
def _start_xvfb():
    _runbg("Xvfb :99 -screen 0 1024x768x8 -ac +extension GLX +render -noreset", sockname="graphicXvfb")

def _start_crawler():
    for peer in CRAWLER_PEERS:
        print 'CRAWLER', peer
        multiprocessing.Process(target=__start_crawler, args=(peer['host_string'], peer['port'])).start()
        
def __start_crawler(host_string, port):
    with settings(host_string=host_string):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            with prefix("ulimit -s 1024"):
                with prefix("ulimit -n 4096"):
                    with cd("/opt/crpc"):
                        with prefix("source ./env.sh {0}".format(os.environ.get('ENV','TEST'))):
                            with prefix("export DISPLAY=:99"):
                                _runbg("python crawlers/common/crawlerserver.py {0}".format(port), sockname="crawlerserver.{0}".format(port))

def _start_power():
    for peer in POWER_PEERS:
        print 'POWER', peer
        multiprocessing.Process(target=__start_power, args=(peer['host_string'], peer['port'])).start()

def __start_power(host_string, port):
    with settings(host_string=host_string):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            with prefix("ulimit -s 1024"):
                with prefix("ulimit -n 4096"):
                    with cd("/opt/crpc"):
                        with prefix("source ./env.sh {0}".format(os.environ.get('ENV','TEST'))):
                            _runbg("python powers/powerserver.py {0}".format(port), sockname="powerserver.{0}".format(port))

def _start_text():
    for peer in TEXT_PEERS:
        print 'TEXT', peer
        multiprocessing.Process(target=__start_text, args=(peer['host_string'], peer['port'])).start()

def __start_text(host_string, port):
    with settings(host_string=host_string):
        with prefix("source /usr/local/bin/virtualenvwrapper.sh"):
            with prefix("ulimit -s 1024"):
                with prefix("ulimit -n 4096"):
                    with cd("/opt/crpc"):
                        with prefix("source ./env.sh {0}".format(os.environ.get('ENV','TEST'))):
                            _runbg("python powers/textserver.py {0}".format(port), sockname="textserver.{0}".format(port))

def crawler_login_file():
    """ change crawlers' login email, redeploy """
    for peer in CRAWLER_PEERS:
        multiprocessing.Process(target=__crawler_login_file, args=(peer['host_string'], peer['port'])).start()

def __crawler_login_file(host_string, port):
    with settings(host_string=host_string):
        put(CRPC_ROOT + '/crawlers/common/username.ini', '/opt/crpc/crawlers/common/')


def ganglia_client():
    """ change ganglia client's configration file """
    import itertools
    for peer in itertools.chain(POWER_PEERS, CRAWLER_PEERS):
        print peer['host_string'], peer['host_string'].split('@')[1].split('.')[0]
        multiprocessing.Process(target=__start_ganglia, args=(peer['host_string'], peer['host_string'].split('@')[1].split('.')[0])).start()

def __start_ganglia(host_string, name):
    with settings(host_string=host_string):
        run("sed -i 's/name = \"unspecified\"/name = \"{0}\"/' /etc/ganglia/gmond.conf".format(name))
        run("/etc/init.d/ganglia-monitor restart")

def _start_monitor():
    os.system("ulimit -n 4096 && cd {0}/backends/monitor && dtach -n /tmp/crpcscheduler.sock python run.py".format(CRPC_ROOT))
    os.system("cd {0}/backends/webui && dtach -n /tmp/crpcwebui.sock python main.py".format(CRPC_ROOT))

def _stop_monitor():
    os.system("ps aux | grep run.py | grep -v grep | awk '{print $2}' | xargs kill -9")
    os.system("ps aux | grep main.py | grep -v grep | awk '{print $2}' | xargs kill -9")
    os.system("rm /tmp/crpc*.sock")

def _start_publish():
    os.system("ulimit -n 4096 && dtach -n /tmp/publish.sock python {0}/publisher/publish.py -d".format(CRPC_ROOT))

def _stop_publish():
    os.system("ps aux | grep publish.py | grep -v grep | awk '{print $2}' | xargs kill -9")
    os.system("rm /tmp/publish*.sock")

def _start_catalog():
    os.system("dtach -n /tmp/catalog.sock python {0}/djCatalog/manage.py runserver 0.0.0.0:1319".format(CRPC_ROOT))    

def _stop_catalog():
    os.system("ps aux | grep 'runserver 0.0.0.0:1319' | grep -v grep | awk '{print $2}' | xargs kill -9")
    os.system("rm /tmp/catalog*.sock")

def _start_admin():
    os.system("cd {0}/admin && dtach -n /tmp/admin.sock python admin.py".format(CRPC_ROOT))

def _stop_admin():
    os.system("ps aux | grep admin | grep -v grep | awk '{print $2}' | xargs kill -9")
    os.system("rm /tmp/admin.sock")

def _runbg(cmd, sockname="dtach"):
    """ A helper function to run command in background """
    return run('dtach -n /tmp/{0}.sock {1}'.format(sockname, cmd))

if __name__ == "__main__":
    import resource
    resource.setrlimit(resource.RLIMIT_NOFILE, (4096, 4096))

