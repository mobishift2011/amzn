#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Scheduler: runs crawlers in background
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from gevent import monkey; monkey.patch_all()
import gevent

from bson.objectid import ObjectId

from crawlers.common.routine import update_category, update_listing, update_product
from .models import Schedule

import zerorpc
from settings import PEERS, RPC_PORT

def delete_schedule(s):
    try:
        print s['pk']
        Schedule.objects.get(pk=s['pk']).delete()
        return {'status':'ok','pk':s['pk']}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {'status':'error','reason':repr(e)}

def get_all_schedules():
    ret = []
    for s in Schedule.objects():
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
        description = d['description']
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
        import traceback
        traceback.print_exc()
        return {'status':'error','reason':repr(e)}


def get_rpcs():
    rpcs = []
    for peer in PEERS:
        host = peer[peer.find('@')+1:]
        c = zerorpc.Client('tcp://{0}:{1}'.format(host, RPC_PORT), timeout=None)
        if c:
            rpcs.append(c)
    return rpcs

class Scheduler(object):
    """ make schedules easy """
    def get_schedules(self):
        return Schedule.objects(enabled=True) 

    def run(self):
        while True:
            for s in get_schedules():
                if s.timematch():
                    gevent.spawn(globals()[s.method], s.site, get_rpcs())
            gevent.sleep(60)
