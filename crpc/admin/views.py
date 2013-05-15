# -*- coding: utf-8 -*-
from settings import MASTIFF_HOST
from models import Brand, DealSchedule
from powers.models import Brand as PowerBrand, Link

from gevent import monkey; monkey.patch_all()
import gevent
from backends.monitor.ghub import GHub
from backends.monitor.throttletask import can_task_run, task_completed, is_task_already_running
from helpers.rpc import get_rpcs
from settings import CRAWLER_PEERS
from functools import partial

from bson.objectid import ObjectId
import slumber
import traceback
from urllib import unquote
from datetime import datetime

def get_all_brands(db='catalogIndex'):
	if db.lower() == "catalogindex":
		brands = [brand.to_json() for brand in Brand.objects()]
	elif db.lower() == "power":
		brands = [{
			'title': brand.title,
			'title_edit': brand.title_edit,
			'title_cn': brand.title_cn,
			'global_searchs': brand.global_searchs,
		} for brand in PowerBrand.objects()]
	return brands

def get_brand(title, db):
	if not db:
		db = 'e'
	if db == 'e':
		brand = Brand.objects.get(title=title)
	elif db == 'p':
		brand = PowerBrand.objects.get(title=title)
	return brand.to_json()

def update_brand(title, arguments):
	brand = Brand.objects.get(title=title) \
		if title else Brand()

	for k, v in arguments.iteritems():
		try:
			value = getattr(brand, k)
		except AttributeError:
			continue

		if hasattr(value, '__iter__'):
			setattr(brand, k, list(set(value) | set(v)))	
		else:
			value = v[0] if v else value
			if value == 'True':
				value = True
			elif value == 'False':
				value = False
			setattr(brand, k, value)

	brand.save()
	brand = Brand.objects.get(title=brand.title)
	return brand.to_json()


def delete_brand(title):
	brand = Brand.objects(title=title)
	if brand:
		brand.delete()
	else:
		return False

	return True


def update_brand_volumn(title, volumns):
	pb = PowerBrand.objects.get(title=title)
	pb.global_searchs = volumns
	pb.save()
	return pb.to_json()



link_api = slumber.API(MASTIFF_HOST)

def get_all_links():
	return [ link for link in link_api.affiliate.get().get('objects') ]


def post_link(patch=False, **kwargs):
	site = kwargs.get('site')
	affiliate = kwargs.get('affiliate')

	request = link_api.affiliate(kwargs.get('key')).patch(kwargs) \
		if patch else link_api.affiliate.post(kwargs)


def delete_link(key):
	links = Link.objects(key=key)
	links.delete()


def execute(site, method):
    """ execute CrawlerServer function for deals

    """
    if can_task_run(site, method):
        job = gevent.spawn(globals()[method], site, get_rpcs(CRAWLER_PEERS), concurrency=10)
        job.rawlink(partial(task_completed, site=site, method=method))
        GHub().extend('tasks', [job])


def delete_schedule(s):
    try:
        DealSchedule.objects.get(pk=s['pk']).delete()
        return {'status':'ok','pk':s['pk']}
    except Exception as e:
        traceback.print_exc()
        return {'status':'error','reason':repr(e)}

def get_all_schedules():
    ret = []
    for s in DealSchedule.objects().order_by('site', 'method'):
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
        enabled = d.get('enabled', False)
        if d.get('pk'):
            pk = ObjectId(d['pk'])
            s = DealSchedule.objects.get(pk=pk)
        else:
            s = DealSchedule(site=crawler, method=method)
        for name in ['description', 'enabled', 'minute', 'hour', 'dayofmonth', 'month', 'dayofweek']:
            setattr(s, name, locals()[name])
        s.save()
        return {'status':'ok', 'pk': str(s.pk)}
    except Exception as e:
        traceback.print_exc()
        return {'status':'error','reason':repr(e)}