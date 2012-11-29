# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('catalogs',
    url(r'^brand/$', 'api.brands'),
    url(r'^brand/fail/$', 'api.brandFailHandle'),
    url(r'^test', 'api.test')
)