# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('catalogs',
    url(r'^brand/$', 'api.brands'),
    url(r'^brand/tasks/$', 'api.brandTaskHandle'),
    url(r'^test', 'api.test')
)