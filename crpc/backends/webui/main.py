#!/usr/bin/python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import gevent

from bottle import route, post, request, run, template, static_file, redirect
from os.path import join, dirname
from backends.monitor.logstat import log_event, task_updates, task_all_tasks, mark_all_failed
from backends.monitor.scheduler import update_schedule, get_all_schedules, delete_schedule, Scheduler, get_rpcs
from crawlers.common.routine import update_category, update_listing, update_product

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
def run_command():
    try:
        method = request.json['method']
        site = request.json['site']
        if globals().get(method):
            gevent.spawn(globals()[method], site, get_rpcs())
            return {'status':'ok'}
        else:
            return {'status':'error', 'reason':'method not found: '+method}
    except Exception as e:
        return {'status':'error', 'reason':repr(e)}

gevent.spawn(Scheduler().run)

mark_all_failed()

run(server='gevent', host='0.0.0.0', port=1317)
