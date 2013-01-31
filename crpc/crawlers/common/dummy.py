#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import uuid
from powers.events import ready_for_batch
from crawlers.common.stash import picked_crawlers

method_new = ['new_']
method_update = ['update_']

def send_signal():
    for site in picked_crawlers:
        ctx = "{0}.{1}.{2}".format(site, method_new, uuid.uuid1().hex + uuid.uuid4().hex)
        ready_for_batch.send(sender=ctx, site=site, doctype='event')    #listing
        ready_for_batch.send(sender=ctx, site=site, doctype='product')  #product

@ready_for_publish.bind
def send_one_site(sender, **kwargs):
    site = kwargs.get('site', '')
    if not site:
        return
    ctx = "{0}.{1}.{2}".format(site, method_new, uuid.uuid1().hex + uuid.uuid4().hex)
    ready_for_batch.send(sender=ctx, site=site, doctype='event')    #listing
    ready_for_batch.send(sender=ctx, site=site, doctype='product')  #product


if __name__ == '__main__':
    import time
    send_signal()
