# -*- coding: utf-8 -*-

from settings import CRPC_ROOT
from powers.configs import SITES
from backends.monitor.models import Schedule
from os import listdir
import os

"""
A script tool to insert schedules for monitor.
"""
def insert():
    excludes = ['common', 'ecost', 'bhphotovideo', 'bestbuy', 'dickssport', 'overstock', 'cabelas']
    methods = ('new', 'new_category', 'new_listing', 'new_product', 'update', 'update_category', 'update_listing', 'update_product')
    crontab_arguments = '*/30 * * * *'
    for site in SITES:#listdir(os.path.join(CRPC_ROOT, "crawlers")):
        for method in methods:
            s = Schedule.objects(site=site, method=method)
            if not s:
                s = Schedule(site=site, method=method)
                s.description = '{0} {1} test'.format(site , method)
                s.minute, s.hour, s.dayofmonth, s.month, s.dayofweek = [ x for x in crontab_arguments.split(" ") if x ]
                s.save()

insert()
