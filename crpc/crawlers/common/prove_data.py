#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from datetime import datetime
from crawlers.common.stash import picked_crawlers

fetch_page_site = ['bluefly']
req_site = ['nomorerack', 'modnique']
req_site.extend(fetch_page_site)

login_site = ['beyondtherack', 'belleandclive', 'ideeli', 'lot18', 'onekingslane', 'ruelala', 'totsy', 'venteprivee', 'zulily']
not_nedd_login = ['gilt', ]
cookie_site = ['myhabit', 'hautelook']

def get_site_module(site):

    if hasattr(get_site_module, 'mod'):
        setattr(get_site_module, 'mod', {})

    if site not in get_site_module:
        for site in picked_crawlers:
            get_site_module.mod[site] = __import__("crawlers.{0}.models".format(site), fromlist=['Event', 'Category', 'Product'])

    return get_site_module.mod[site]

for crawler in picked_crawlers:
    module = get_site_module(crawler)
    for prd in module.Product.objects(products_end__lte=datetime.utcnow()):
        # link not exist, or exist link statistics
        
        __import__('crawlers.{0}.server'.format(crawler), fromlist=[])
        prd['combine_url']
    for prd in module.Product.objects(products_end__gt=datetime.utcnow()):
        prd['combine_url']
