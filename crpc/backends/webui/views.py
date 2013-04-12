#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
from os import listdir
from os.path import join, isdir
from datetime import datetime, timedelta
from collections import Counter
from bson.objectid import ObjectId
from mongoengine import Q

from backends.monitor.models import Task, Schedule, fail, Stat
from powers.models import Brand
from powers.events import brand_refresh
from settings import CRPC_ROOT
from crawlers.common.stash import exclude_crawlers
from backends.monitor.models import ProductReport, EventReport


def mark_all_failed():
    Task.objects(status=Task.RUNNING) \
        .update(set__status=Task.FAILED, push__fails=fail(t.site, t.method, '', '', 'Monitor Restart'), inc__num_fails=1)

def task_all_tasks(offset=0, limit=50):
    tasks = Task.objects(updated_at__gt=datetime.utcnow()-timedelta(seconds=3600*24*3)).order_by('-updated_at')[offset:offset+limit]
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

def get_all_sites():
    return [name for name in listdir(join(CRPC_ROOT, 'crawlers')) \
            if name not in exclude_crawlers and isdir(join(CRPC_ROOT, 'crawlers', name))]

def get_one_site_schedule(site):
    tasks = Task.objects(site=site, updated_at__gt=datetime.utcnow()-timedelta(seconds=3600*24*3)).order_by('-started_at')
    return {'tasks': [t.to_json() for t in tasks]}


def get_publish_stats(site, doctype, time_value, time_cell, start_at, end_at):
    data = []
    kwargs = {}
    kwargs[time_cell] = time_value
    interval = timedelta(**kwargs)
    extent_right = end_at
    extent_left = (extent_right - interval) if (extent_right - interval) > start_at else start_at
    c = Counter()

    extents = []
    while extent_right > extent_left:
        extents.append((extent_left, extent_right))
        extent_right = extent_left
        extent_left  = (extent_right - interval) if (extent_right - interval) > start_at else start_at

    try:
        extent = extents.pop(0)
        stats = Stat.objects(site=site, doctype=doctype, interval__gte=start_at, interval__lt=end_at)
        for stat in stats:
            while stat.interval < extent[0]:
                if c['image_num'] or c['prop_num'] or c['publish_num']:
                    data.append({
                        'extent_left': extent[0],
                        'extent_right': extent[1],
                        'image_num': c['image_num'],
                        'prop_num': c['prop_num'],
                        'publish_num': c['publish_num']
                    })
                    c = Counter()
                try:
                    extent = extents.pop(0)
                except:
                    break

            if stat.interval >= extent[0] and stat.interval < extent[1]:
                for key in ('image_num', 'prop_num', 'publish_num'):
                    c[key] += getattr(stat, key)

        if c['image_num'] or c['prop_num'] or c['publish_num']:
            data.append({
                'extent_left': extent[0],
                'extent_right': extent[1],
                'image_num': c['image_num'],
                'prop_num': c['prop_num'],
                'publish_num': c['publish_num']
            })
    except:
        pass

    return data


def get_publish_report(_thedate):
    prds = ProductReport.objects(today_date=_thedate)
    events = EventReport.objects(today_date=_thedate)
    return {'event': [e.to_json() for e in events],
            'product': [p.to_json() for p in prds],
            'date': _thedate}


def import_brands(eb):
    brand = Brand.objects(title=eb['title']).update(
        set__title_edit = eb['title_edit'],
        set__title_checked = eb['title_checked'],
        set__alias = eb['alias'],
        set__keywords = eb['keywords'],
        set__url = eb['url'],
        set__url_checked = eb['url_checked'],
        set__blurb = eb['blurb'],
        set__images = eb['images'],
        set__level = eb['level'],
        set__dept = eb['dept'],
        set__is_delete = eb['is_delete'],
        set__done = eb['done'],
        set__created_at = eb['created_at'],
        upsert = True
    )

def refresh_brands():
    brand_refresh.send(None)
