#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent.event import Event
from crawlers.common.events import common_saved, common_failed
import time

log_event =  Event()

last_logged = time.time()

@common_saved.bind
def trigger_saved_event(sender, **kwargs):
    global last_logged
    if time.time() - last_logged > 0.1:
        log_event.set()
        log_event.clear() 
        last_logged = time.time()

@common_failed.bind
def trigger_failed_event(sender, **kwargs):
    global last_logged
    if time.time() - last_logged > 0.1:
        log_event.set()
        log_event.clear() 
        last_logged = time.time()

