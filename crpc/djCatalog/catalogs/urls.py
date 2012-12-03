# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('catalogs',
	url(r'^$', 'api.brandTasksHandle'),
    url(r'^brand/tasks/$', 'api.brandTasksHandle'),
    url(r'^brand/task/(?P<task_id>\w+)/$', 'api.brandTaskHandle'),
    url(r'^test', 'api.test')
)