#!/usr/bin/python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import gevent

from bottle import route, post, request, run, template, static_file, redirect
from os.path import join, dirname

from backends.webui.events import log_event
from backends.monitor.events import run_command
from backends.webui.views import task_updates, task_all_tasks, mark_all_failed
from backends.webui.views import update_schedule, get_all_schedules, delete_schedule 

@route('/assets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=join(dirname(__file__), 'assets'))

@route('/')
def index():
    redirect('/task')

@route('/task')
def task():
    return template('task')

@route('/task/all')
def task_all():
	return task_all_tasks()

@route('/task/update')
def task_update():
    try:
	    log_event.wait(timeout=5)
    except:
        # we shouldn't hang the user fovever
        # after 10 seconds, if no event occur, return empty
        pass
    return task_updates()

@route('/control')
def control():
    return template('control')

@route('/control/all')
def all_schedule():
    return {'schedules': get_all_schedules()}

@post('/control/save')
def save_schedule():
    return update_schedule(request.json)

@post('/control/del')
def del_schedule():
    return delete_schedule(request.json)

@post('/control/run')
def execute_command():
    method = request.json['method']
    site = request.json['site']
    run_command.send('webui', site=site, method=method)
    return {'status':'ok'}

#mark_all_failed()

run(server='gevent', host='0.0.0.0', port=1317)
