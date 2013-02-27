#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from datetime import datetime
from crawlers.common.stash import picked_crawlers

fetch_page_site = ['bluefly']
cookie_site = ['myhabit', 'hautelook']
req_site = ['nomorerack', 'modnique']
req_site.extend(cookie_site)

login_site = ['beyondtherack', 'belleandclive', 'ideeli', 'lot18', 'totsy', 'venteprivee']
not_need_login = ['gilt', 'onekingslane', 'ruelala', 'zulily' ]

def get_site_module(site):

    if not hasattr(get_site_module, 'mod'):
        setattr(get_site_module, 'mod', {})

    if site not in get_site_module.mod:
        for site in picked_crawlers:
            get_site_module.mod[site] = __import__("crawlers.{0}.models".format(site), fromlist=['Event', 'Category', 'Product'])

    return get_site_module.mod[site]

for crawler in picked_crawlers:
    old_exists, new_not_exist = 0, 0
    if crawler in req_site:
        login = __import__('crawlers.{0}.server'.format(crawler), fromlist=['req'])
    elif crawler in fetch_page_site:
        login = requests.Session()
    elif crawler in not_need_login:
        login = requests.Session()
    elif crawler in login_site:
        login = __import__('crawlers.{0}.server'.format(crawler), fromlist=['{0}Login'.format(crawler)])
    module = get_site_module(crawler)
    for prd in module.Product.objects(products_end__lte=datetime.utcnow()):
        # link not exist, or exist link statistics
        ret = login.get(prd['combine_url'])
        if ret.status_code == 200:
            old_exists += 1
    for prd in module.Product.objects(products_end__gt=datetime.utcnow()):
        ret = login.get( prd['combine_url'] )
        if ret.status_code != 200:
            new_not_exist += 1
