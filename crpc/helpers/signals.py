#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
helpers.signals
~~~~~~~~~~~~~~~

Decoupling though callbacks

Usage:

1. issue signal when some event occur

>>> import signals
>>> after_task_complete = signals.Signal('task completed')

2. at another module, bind event listeners to the event

>>> after_task_complete.bind
>>> def log_task(sender, **kwargs):
...     product_id = kwargs.get('product_id')
...     time_consumed = kwargs.get('time_consumed')
...     print("Sender {sender!r}: Product {product_id} completed in {time_consumed} seconds".format(**locals()))

3. in the task module, when task finished, send signal

>>> after_task_complete.send(sender="taskmodule", product_id=1, time_consumed=5.3)

4. define a proper protocol for signals arguments and document it, that's it, we got decoupling modules cooperating happily without knowing the implementation of each other.

.. note::

    be aware that this module works for threads or coroutines but not for processes

"""
from collections import defaultdict
from multiprocessing import current_process

import log

class Processer(object):
    def __init__(self):
        self._listeners = defaultdict(set)
        self.logger = log.getlogger("helper.signals.Processor")

    def add_listener(self, signal, callback):
        cbname = callback.__name__
        self._listeners[signal].add(callback)
        self.logger.debug("{signal!r} binded by <{cbname}>".format(**locals()))

    def send_message(self, sender, signal, **kwargs):
        self._execute_callbacks(sender, signal, **kwargs)

    def _execute_callbacks(self, sender, signal, **kwargs):
        if signal not in self._listeners:
            logger.warning("signal bingings for {signal!r} not found!".format(**locals()))
        else:
            try:
                for cb in self._listeners[signal]:
                    cb(sender, **kwargs)
            except Exception as e:
                logger.exception("Exception happened when executing callback")
                logger.error("sender: {sender}, signal: {signal!r}, kwargs: {kwargs!r}".format(**locals()))


p = Processer()

class Signal(object):
    def __init__(self, name):
        self._name = name

    def send(self, sender, **kwargs):
        data = {'kwargs':kwargs}
        p.send_message(sender, self, **kwargs)
        
    def connect(self, callback):
        p.add_listener(self, callback)

    def bind(self, f):
        self.connect(f)
        def _decorator():
            return f
        return _decorator

    def __str__(self):
        return "<Signal: {name}>".format(name=self._name)

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    after_item_init = Signal("after_item_init")

    @after_item_init.bind
    def log_item_init(sender, **kwargs):
        itemid  = kwargs.get('item_id')
        print("sender: {sender}, itemid: {itemid}".format(**locals()))

    after_item_init.send(sender="main", item_id=3)
