#!/usr/bin/python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import gevent

from bottle import route, post, request, run, template, static_file, redirect
from os.path import join, dirname

from auth import *
from backends.webui.events import log_event
from backends.monitor.events import run_command
from backends.webui.views import task_updates, task_all_tasks, mark_all_failed, get_all_fails
from backends.webui.views import update_schedule, get_all_schedules, delete_schedule 

@route('/assets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=join(dirname(__file__), 'assets'))

@route('/login')
def login():
   return template('login')

@post('/login')
@login_required
def signIn():
    redirect('/')

@route('/')
# @login_required
def index():
    redirect('/task')

@route('/task')
# @login_required
def task():
    return template('task')

@route('/task/all')
def task_all():
    offset = request.params.get('offset', '0') 
    limit = request.params.get('limit', '50')
    offset, limit = int(offset), int(limit)
    print offset, limit
    return task_all_tasks(offset, limit)

@route('/task/update')
# @login_required
def task_update():
    try:
        log_event.wait(timeout=5)
    except:
        # we shouldn't hang the user fovever
        # after 10 seconds, if no event occur, return empty
        pass
    return task_updates()

@route('/control')
# @login_required
def control():
    return template('control')

@route('/control/all')
# @login_required
def all_schedule():
    return {'schedules': get_all_schedules()}

@post('/control/save')
# @login_required
def save_schedule():
    return update_schedule(request.json)

@post('/control/del')
# @login_required
def del_schedule():
    return delete_schedule(request.json)

@post('/control/run')
# @login_required
def execute_command():
    method = request.json['method']
    site = request.json['site']
    run_command.send('webui', site=site, method=method)
    return {'status':'ok'}

@route('/task/:ctx/fails')
# @login_required
def get_task_fails(ctx):
    return get_all_fails(ctx);

@route('/progress')
# @login_required
def progress_all():
    return template('process.tpl')


#mark_all_failed()

run(server='gevent', host='0.0.0.0', port=1317, debug=True)
