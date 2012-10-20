#!/usr/bin/python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()

from bottle import route, run, template, static_file
from os.path import join, dirname
from backends.monitor.logstat import log_event, task_updates, task_all

@route('/assets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=join(dirname(__file__), 'assets'))

@route('/')
def index():
    return template('index')

@route('/table')
def table():
    return template('table')

@route('/table/all')
def table_all():
	return task_all()

@route('/table/update')
def table_update():
    try:
	    log_event.wait(timeout=10)
    except:
        # we shouldn't hang the user fovever
        # after 10 seconds, if no event occur, return empty
        pass
	return task_updates()

@route('/angular')
def table():
    return template('angular')

run(server='gevent', host='0.0.0.0', port=1317)
