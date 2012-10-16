#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Decoupling though callbacks

Usage:

1. issue signal when some event occur

>>> TASK_COMPLETE = 5001
>>> import signals
>>> signals.signal(TASK_COMPLETE, product_id=1, time_consumed=5.23)

2. at another module, bind event listeners to the event

>>> import signals
>>> @signals.bind(TASK_COMPLETE)
>>> def log_task(product_id, time_consumed):
...     print("Product {product_id} completed in {time_consumed} seconds".format(**locals()))

3. define a proper protocol for signals arguments and document it, that's it, we got decoupling modules cooperating happily without knowing the implementation of each other.

.. note::

    be aware that this module works for threads or coroutines but not for processes

"""
from collections import defaultdict
from multiprocessing import current_process

import log
logger = log.getlogger("helper.signals")

class Processer:
    def __init__(self):
        self.workers = defaultdict(set)
        self.funcnames = set()

    def add_worker(self, workername, callback):
        funcname = callback.__name__
        
        # a work around for multiple processing signals
        # when we reload a module, signals does not rebind
        # this might be an issue if we hook the module ``reload`` 
        # otherwise, this will be fine
        if funcname not in self.funcnames:
            self.workers[workername].add(callback)
            self.funcnames.add(funcname)

    def _execute_callbacks(self, workername, message):
        if workername not in self.workers:
            logger.warning("signal bingings on {workername} not found!".format(**locals()))
        else:
            try:
                data = message
                for w in self.workers[workername]:
                    w(*data['args'],**data['kwargs'])
            except Exception as e:
                logger.exception("Exception happened when executing callback")
                logger.error("workername, {workername}".format(**locals()))
                logger.error("message, {message}".format(**locals()))

    def send_message(self, workername, message):
        self._execute_callbacks(workername, message)

p = Processer()

def bind(workername):
    """ the decorator method for convinience """
    def _decorator(f):
        p.add_worker(str(workername), f)
        return f
    return _decorator

def signal(workername, *args, **kwargs):
    data = {'args':args,'kwargs':kwargs}
    p.send_message(workername, data)

if __name__ == '__main__':
    has_item = "has_item"

    @bind(has_item)
    def when_fight_finished_print_signal(tip, aid):
        print( "tip is {tip} and aid is {aid}".format(**locals()))

    signal(has_item, 'wow', aid=1)

