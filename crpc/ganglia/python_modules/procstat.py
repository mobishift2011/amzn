#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import zerorpc
import time
import subprocess

def _cpu_handler(name):
    pid = subprocess.Popen('ps aux | grep {0} | grep -v grep | grep -v dtach'.format(name), shell=True, stdout=subprocess.PIPE).communicate()[0].split()[1]
    cont = open('/proc/{0}/stat'.format(pid)).read()
    proctime = sum( int(i) for i in cont.split()[13:17] )
    cont = open('/proc/stat').readline().strip()
    cputime = sum( int(i) for i in cont.split()[1:] )

    time.sleep(2)
    cont = open('/proc/{0}/stat'.format(pid)).read()
    proctime2 = sum( int(i) for i in cont.split()[13:17] )
    cont = open('/proc/stat').readline().strip()
    cputime2 = sum( int(i) for i in cont.split()[1:] )

    return (proctime2 - proctime) *100 / (cputime2 - cputime)


def _cpu(name):
    cont = subprocess.Popen('ps aux | grep {0} | grep -v grep | grep -v dtach'.format(name.split('_')[0]), shell=True, stdout=subprocess.PIPE).communicate()[0].split()
    return float(cont[2])

def _memory(name):
    cont = subprocess.Popen('ps aux | grep {0} | grep -v grep | grep -v dtach'.format(name.split('_')[0]), shell=True, stdout=subprocess.PIPE).communicate()[0].split()
    return float(cont[3])

def _socket(name):
    if not hasattr(_socket, 'rpc_client'):
        setattr(_socket, 'rpc_client', None)

    if not _socket.rpc_client:
        _socket.rpc_client = zerorpc.Client()
        _socket.rpc_client.connect('tcp://127.0.0.1:6357')
    return _socket.rpc_client.get_socket(name)


def metric_init(params):
    d1 = { 
        'name': 'run.py_cpu',
        'call_back': _cpu,
        'time_max': 90, 
        'value_type': 'float',
        'units': '%',
        'slope': 'both',
        'format': '%f',
        'description': 'Cpu usage of run.py process',
        'groups': 'prostat',
    }

    d2 = {
        'name': 'run.py_memory',
        'call_back': _memory,
        'time_max': 90,
        'value_type': 'float',
        'units': '%',
        'slope': 'both',
        'format': '%f',
        'description': 'Memory usage of run.py process',
        'groups': 'prostat',
    }

    d3 = {
        'name': 'run.py_socket',
        'call_back': _socket,
        'time_max': 90,
        'value_type': 'int',
        'units': 'socket number',
        'slope': 'both',
        'format': '%d',
        'description': 'Socket number of run.py process',
        'groups': 'prostat',
    }

    d4 = {
        'name': 'publish.py_cpu',
        'call_back': _cpu,
        'time_max': 90,
        'value_type': 'float',
        'units': '%',
        'slope': 'both',
        'format': '%f',
        'description': 'Cpu usage of publish.py process',
        'groups': 'prostat',
    }

    d5 = {
        'name': 'publish.py_memory',
        'call_back': _memory,
        'time_max': 90,
        'value_type': 'float',
        'units': '%',
        'slope': 'both',
        'format': '%f',
        'description': 'Memory usage of publish.py process',
        'groups': 'prostat',
    }

    descriptors = [d1, d2, d3, d4, d5]
    return descriptors

def metric_cleanup():
    pass

def metric_handler(name):
    pass

if __name__ == '__main__':
    descriptors = metric_init({})
    for d in descriptors:
        v = d['call_back'](d['name'])
        print 'value for %s is %u' % (d['name'],  v)
