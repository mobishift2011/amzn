#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
from backends.monitor.models import Task, Schedule, fail

from bson.objectid import ObjectId
from datetime import datetime, timedelta

from powers.models import EventProgress, ProductProgress

def mark_all_failed():
    Task.objects(status=Task.RUNNING) \
        .update(set__status=Task.FAILED, push__fails=fail(t.site, t.method, '', '', 'Monitor Restart'), inc__num_fails=1)

def task_all_tasks():
    tasks = Task.objects(updated_at__gt=datetime.utcnow()-timedelta(seconds=3600*24)).order_by('-updated_at')
#    tasks = Task.objects().fields(slice__fails=-10).order_by('-updated_at').limit(100).select_related()
    return {"tasks":[t.to_json() for t in tasks]}

def task_updates():
    tasks = Task.objects(updated_at__gt=datetime.utcnow()-timedelta(seconds=60)).fields(slice__fails=-10).select_related()
    return {"tasks":[t.to_json() for t in tasks]}

def delete_schedule(s):
    try:
        Schedule.objects.get(pk=s['pk']).delete()
        return {'status':'ok','pk':s['pk']}
    except Exception as e:
        traceback.print_exc()
        return {'status':'error','reason':repr(e)}

def get_all_schedules():
    ret = []
    for s in Schedule.objects().order_by('site', 'method'):
        ret.append({
            'pk':                   str(s.pk),
            'name':                 '{0}.{1}'.format(s.site, s.method),
            'description':          s.description,
            'crontab_arguments':    s.get_crontab_arguments(),
            'enabled':              s.enabled,
        })
    return ret

def update_schedule(d):
    try:
        crawler, method = d['name'].split('.')
        minute, hour, dayofmonth, month, dayofweek = [ x for x in d['crontab_arguments'].split(" ") if x ]
        description = d.get('description', u'这个人太懒了什么都没写')
        enabled = d['enabled']
        if d.get('pk'):
            pk = ObjectId(d['pk'])
            s = Schedule.objects.get(pk=pk)
        else:
            s = Schedule(site=crawler, method=method)
        for name in ['description', 'enabled', 'minute', 'hour', 'dayofmonth', 'month', 'dayofweek']:
            setattr(s, name, locals()[name])
        s.save()
        return {'status':'ok', 'pk': str(s.pk)}
    except Exception as e:
        traceback.print_exc()
        return {'status':'error','reason':repr(e)}

def get_all_fails(ctx):
    task = Task.objects.get(ctx=ctx)
    fails = task.fails[-10:]
    return {'fails': [fail.to_json() for fail in fails]}

def get_all_progresses():
    eps = EventProgress.objects() # TODO some filtering.
    pps = ProductProgress.objects()
    ep_list = [p.to_json() for p in eps]
    pp_list = [p.to_json() for p in pps]
    ep_list.extend(pp_list)
    return ep_list
