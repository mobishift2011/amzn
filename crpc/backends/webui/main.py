#!/usr/bin/python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()
import gevent

from bottle import route, get, post, request, run, template, static_file, redirect
from os.path import join, dirname
from datetime import datetime
import time
import pytz
import json

from auth import *
from backends.webui.events import log_event
from backends.monitor.events import run_command
from backends.webui.views import task_updates, task_all_tasks, mark_all_failed, get_all_fails
from backends.webui.views import update_schedule, get_all_schedules, delete_schedule, get_one_site_schedule
from backends.webui.views import get_all_sites, get_publish_stats
from backends.webui.views import import_brands, refresh_brands
from backends.monitor.upcoming_ending_events_count import upcoming_events, ending_events
from backends.monitor.publisher_report import wink

from tests.publisher.chkpub import PubChecker
from backends.monitor.events import auto_scheduling

from backends.monitor.models import Stat

@route('/toggle-auto-scheduling/:onoff')
def toggle_auto_scheduling(onoff):
    if onoff == 'on':
        onoff = True
    else:
        onoff = False
    auto_scheduling.send('webui', auto=onoff)
    
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

@route('/publish')
# @login_required
def publish():
    return template('publish.tpl')

@get('/publish/chkpub')
# @login_required
def chkpub_template():
    return template('chkpub.tpl', {'stats':None, 'sites': get_all_sites()})

@post('/publish/chkpub')
# @login_required
def chkpub():
    site = request.forms.get('site')
    doctype = request.forms.get('doctype')
    sites = get_all_sites() if site == 'all' else [site]
    stats = [ {'site': site, \
            'data': getattr(PubChecker(), 'check_{0}'.format(doctype))(site) or [] } \
                for site in sites]
    # data = getattr(PubChecker(), 'check_{0}'.format(doctype))(site) or []
    return template('chkpub.tpl', {'stats': stats})

@get('/publish/stats')
# @login_required
def publish_stats_template():
    return template('pubstats.tpl', {'stats':None, 'sites': get_all_sites()})

@post('/publish/stats')
# @login_required
def publish_stats():
    site = request.forms.get('site')
    doctype = request.forms.get('doctype')
    time_value = int(request.forms.get('time_value'))
    time_cell = request.forms.get('time_cell')
    str_begin = request.forms.get('begin_at')
    str_end = request.forms.get('end_at')

    begin_at = datetime.strptime(str_begin, '%Y-%m-%d %H:%M:%S') \
                if str_begin else datetime.utcnow()
    end_at = datetime.strptime(str_end, '%Y-%m-%d %H:%M:%S') \
                if str_end else datetime.utcnow()

    data = get_publish_stats(site, doctype, time_value, time_cell, begin_at, end_at)
    return template('pubstats.tpl', {'stats': data, 'sites': [site]})

@route('/publish/report')
def today_publish_report():
    _utcnow = datetime.utcnow()
    wink(_utcnow)
    return template('report.tpl')

@route('/publish/report?date=<date>')
def publish_report(date):
    return template('report.tpl')

@post('/brand/')
def brands_import():
    eb = json.loads(request.POST['brand'])
    import_brands(eb)

@post('/brands/refresh')
def brands_refresh():
    refresh_brands()

@route('/history')
def history():
    return template('history')

@route('/site/<site>')
def see_site(site):
    return template('site.tpl', get_one_site_schedule(site))

@route('/schedule/<action>')
def schedule(action):
    if action == 'upcoming':
        return template('schedule.tpl', {'schedules': upcoming_events()})
    elif action == 'ending':
        return template('schedule.tpl', {'schedules': ending_events()})

@route('/graph')
def graph():
    return template('graph.tpl', {})
    
@route('/graph/event/<site>')
def graph_event_detail(site):
    stats = Stat.objects(site=site, doctype='event').order_by('interval')
    graphdata = []
    graphdata.append({'name':'crawled', 'data':[(int(time.mktime(s.interval.timetuple())*1000), s.crawl_num) for s in stats]})
    graphdata.append({'name':'image', 'data':[(int(time.mktime(s.interval.timetuple())*1000), s.image_num) for s in stats]})    
    graphdata.append({'name':'propagated', 'data':[(int(time.mktime(s.interval.timetuple())*1000), s.prop_num) for s in stats]})
    graphdata.append({'name':'published', 'data':[(int(time.mktime(s.interval.timetuple())*1000), s.publish_num) for s in stats]})            
    return json.dumps(graphdata)
    
@route('/graph/product/<site>')
def graph_prouct_detail(site):
    stats = Stat.objects(site=site, doctype='product').order_by('interval')
    graphdata = []
    graphdata.append({'name':'crawled', 'data':[(int(time.mktime(s.interval.timetuple())*1000), s.crawl_num) for s in stats]})    
    graphdata.append({'name':'image', 'data':[(int(time.mktime(s.interval.timetuple())*1000), s.image_num) for s in stats]})
    graphdata.append({'name':'published', 'data':[(int(time.mktime(s.interval.timetuple())*1000), s.publish_num) for s in stats]})            
    return json.dumps(graphdata)
    
#mark_all_failed():

run(server='gevent', host='0.0.0.0', port=1317, debug=True)
