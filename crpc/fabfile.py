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
from cuisine import *
from fabric.api import *
from fabric.context_managers import *
from fabric.utils import puts
from fabric.colors import red, green

import os
import sys
import time
import multiprocessing

sys.path.insert(0, os.path.dirname(__file__))

GIT_REPO = 'git@repo.favbuy.org:amzn.git'

ENV = 'DEV'
CRPC = []
HOSTS = []
CRAWLER_HOSTS = []
POWER_HOSTS = []
TEXT_HOSTS = []

def dev():
    global CRPC
    CRPC = ['root@127.0.0.1']
    _setup_env('DEV')

def production():
    global CRPC
    CRPC = ['root@crpc.favbuy.org']
    _setup_env('PRODUCTION')

def integrate():
    global CRPC
    CRPC = ['root@mongodb.favbuy.org']
    _setup_env('INTEGRATE') 

def _setup_env(env):
    global ENV, CRPC, HOSTS, CRAWLER_HOSTS, POWER_HOSTS, TEXT_HOSTS
    ENV = env
    os.environ['ENV'] =  ENV
    from settings import PEERS, CRAWLER_PEERS, POWER_PEERS, TEXT_PEERS
    global PEERS, CRAWLER_PEERS, POWER_PEERS, TEXT_PEERS

    puts(red('Using PRODUCTION settings'))
    HOSTS = list(set([ p['host_string'] for p in  PEERS ])) + CRPC
    CRAWLER_HOSTS = list(set([ p['host_string'] for p in CRAWLER_PEERS ]))
    POWER_HOSTS = list(set([ p['host_string'] for p in POWER_PEERS ]))
    TEXT_HOSTS = list(set([ p['host_string'] for p in TEXT_PEERS ]))

def setup_packages():
    puts(green('Installing Ubuntu Packages'))
    env.hosts = HOSTS
    execute(_setup_packages)

@parallel
def _setup_packages():
    sudo("apt-get update")
    sudo("apt-get -y install build-essential python-dev libevent-dev libxslt-dev uuid-dev python-setuptools dtach redis-server chromium-browser xvfb unzip libjpeg8-dev gfortran libblas-dev liblapack-dev ganglia-monitor")
    sudo("apt-get -y build-dep python-imaging")
    sudo("ln -sf /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/")
    sudo("ln -sf /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/")
    sudo("ln -sf /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/")
    sudo("easy_install pip")
    sudo("pip install cython")
    sudo("pip install numpy")
    sudo("pip install scipy")
    sudo("pip install scikit-learn pattern")
    sudo("pip install ez_setup")
    sudo("pip install https://github.com/SiteSupport/gevent/tarball/master")
    sudo("pip install zerorpc lxml requests pymongo mongoengine redis redisco pytz Pillow titlecase mock selenium blinker cssselect boto python-dateutil virtualenvwrapper slumber esmre django supervisor")

def setup_users():
    puts(green('Creating Ubuntu Users'))

def setup_folders():
    puts(green('Creating Folders'))
    execute(_setup_folders)

@parallel
def _setup_folders():
    sudo("mkdir -p /srv/crpc")

def configure_mongodb():
    puts(green('Configuring MongoDB'))

def configure_supervisor():
    pass

def sync_latest_code():
    env.hosts = HOSTS
    execute(_sync_latest_code)  

@parallel
def _sync_latest_code():
    puts(green('Syncing Latest Code'))
    with cd('/srv/crpc'):
        puts(green('Syncing Latest Code'))
        if dir_exists('/srv/crpc/src'):
            with cd('/srv/crpc/src'):
                sudo('git checkout -- .')
                sudo('git pull')
                sudo('cp -r /srv/crpc/src/crpc/* /srv/crpc/')
        else:
            sudo('git clone %s src' % GIT_REPO)
            sudo('cp -r /srv/crpc/src/crpc/* /srv/crpc/')
        
        puts(green('Installing dependencies'))
        sudo('pip install -r requirements.txt')
    
        puts('Injecting supervisor settings')
        with mode_sudo():
            basic_conf = text_strip_margin('''
            |[unix_http_server]
            |file=/tmp/supervisor_monitor.sock
            |
            |[supervisord]
            |directory=/srv/crpc
            |pidfile=/tmp/supervisord_monitor.pid
            |logfile_backups=1
            |
            |[rpcinterface:supervisor]
            |supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface
            |
            |[supervisorctl]
            |serverurl = unix:///tmp/supervisor_monitor.sock
            |
            ''')
            file_write('/srv/crpc/supervisord.conf', basic_conf)

            crawler_confs = []
            for peer in CRAWLER_PEERS:
                if peer['host_string'] == env.host_string:
                    crawler_conf = text_strip_margin('''
                    |
                    |[program:crawler{0}]
                    |directory = /srv/crpc/crawlers/common
                    |environment = PYTHONPATH=/srv/crpc, ENV={1}
                    |command = python crawlerserver.py {2}
                    |
                    '''.format(peer['port'],ENV,peer['port']))
                    crawler_confs.append(crawler_conf)
            if env.host_string in CRAWLER_HOSTS:
                for cc in crawler_confs:
                    file_append('/srv/crpc/supervisord.conf', cc)

            power_confs = []
            for peer in POWER_PEERS:
                if peer['host_string'] == env.host_string:
                    power_conf = text_strip_margin('''
                    |
                    |[program:power{0}]
                    |directory = /srv/crpc/powers
                    |environment = PYTHONPATH=/srv/crpc, ENV={1}
                    |command = python powerserver.py {2}
                    |
                    '''.format(peer['port'],ENV,peer['port']))
                    power_confs.append(power_conf)
            if env.host_string in POWER_HOSTS:
                for pc in power_confs:
                    file_append('/srv/crpc/supervisord.conf', pc)

            text_confs = []
            for peer in TEXT_PEERS:
                if peer['host_string'] == env.host_string:
                    text_conf = text_strip_margin('''
                    |
                    |[program:text]
                    |directory = /srv/crpc/powers
                    |environment = PYTHONPATH=/srv/crpc, ENV={0}
                    |command = python textserver.py {1}
                    |
                    '''.format(ENV,peer['port']))
                    text_confs.append(text_conf)
            if env.host_string in TEXT_HOSTS:
                for tc in text_confs:
                    file_append('/srv/crpc/supervisord.conf', tc)

            for host_string in CRPC:
                if host_string == env.host_string:
                    admin_conf = text_strip_margin('''
                    |
                    |[program:admin]
                    |directory = /srv/crpc/admin
                    |environment = PYTHONPATH=/srv/crpc, ENV={0}
                    |command = python admin.py
                    |
                    '''.format(ENV))
                    file_append('/srv/crpc/supervisord.conf', admin_conf)

                    scheduler_conf = text_strip_margin('''
                    |
                    |[program:scheduler]
                    |directory = /srv/crpc/backends/monitor
                    |environment = PYTHONPATH=/srv/crpc, ENV={0}
                    |command = python run.py
                    |
                    '''.format(ENV))
                    file_append('/srv/crpc/supervisord.conf', scheduler_conf)

                    publisher_conf = text_strip_margin('''
                    |
                    |[program:publisher]
                    |directory = /srv/crpc/publisher
                    |environment = PYTHONPATH=/srv/crpc, ENV={0}
                    |command = python publish.py -d
                    |
                    '''.format(ENV))
                    file_append('/srv/crpc/supervisord.conf', publisher_conf)
                    
                    webui_conf = text_strip_margin('''
                    |
                    |[program:webui]
                    |directory = /srv/crpc/backends/webui
                    |environment = PYTHONPATH=/srv/crpc, ENV={0}
                    |command = python main.py
                    |
                    '''.format(ENV))
                    file_append('/srv/crpc/supervisord.conf', webui_conf)
        
                    monitor_conf = text_strip_margin('''
                    |
                    |[program:monitor]
                    |directory = /srv/crpc
                    |environment = PYTHONPATH=/srv/crpc, ENV={0}
                    |command = python monitor.py
                    |
                    '''.format(ENV))
                    file_append('/srv/crpc/supervisord.conf', monitor_conf)

def restart_crawler_server():
    env.hosts = CRAWLER_HOSTS
    execute(_restart_zero)

def restart_power_server():
    env.hosts = POWER_HOSTS
    execute(_restart_zero)

def restart_text_server():
    env.hosts = TEXT_HOSTS
    execute(_restart_zero)

def restart_zero_server():
    env.hosts = HOSTS
    for host in CRPC:
        env.hosts.remove(host)
    execute(_restart_zero)

def restart_all():
    execute(stop_crpc_server)
    execute(restart_zero_server)
    execute(start_crpc_server)

def stop_crpc_server():
    env.hosts = CRPC
    execute(_stop_crpc)

def _stop_crpc():
    puts(green("Stopping CRPC Servers"))
    with settings(warn_only=True):
        run('killall supervisord')
        run('sleep 0.5')

def start_crpc_server():
    for host_string in CRPC:
        with settings(host_string=host_string, warn_only=True):
            with cd('/srv/crpc'):
                run('supervisord -c supervisord.conf -l /tmp/supervisord.log')
        
def _restart_zero():
    puts(green("Restarting Zero Servers"))
    with settings(warn_only=True):
        run('killall supervisord')
        run('sleep 0.5')
        with cd('/srv/crpc'):
            run('supervisord -c supervisord.conf -l /tmp/supervisord.log')

def deploy():
    """ setup environment, configure, and start """
    puts(green('Starting deployment'))
    setup_packages()
    setup_users()
    setup_folders()

    configure_mongodb()
    configure_supervisor()
    
    sync_latest_code()

    restart_ganglia_client()
    restart_all()

def crawler_login_file():
    """ change crawlers' login email, redeploy """
    for peer in CRAWLER_PEERS:
        multiprocessing.Process(target=__crawler_login_file, args=(peer['host_string'], peer['port'])).start()

def __crawler_login_file(host_string, port):
    with settings(host_string=host_string):
        put(CRPC_ROOT + '/crawlers/common/username.ini', '/opt/crpc/crawlers/common/')


def restart_ganglia_client():
    """ change ganglia client's configration file """
    import itertools
    for peer in itertools.chain(POWER_PEERS, CRAWLER_PEERS):
        print peer['host_string'], peer['host_string'].split('@')[1].split('.')[0]
        multiprocessing.Process(target=__start_ganglia, args=(peer['host_string'], peer['host_string'].split('@')[1].split('.')[0])).start()

def __start_ganglia(host_string, name):
    with settings(host_string=host_string):
        run("sed -i 's/name = \"unspecified\"/name = \"{0}\"/' /etc/ganglia/gmond.conf".format(name))
        run("/etc/init.d/ganglia-monitor restart")

if __name__ == "__main__":
    pass
