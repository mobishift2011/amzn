#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
helpers.signals2
~~~~~~~~~~~~~~~~

Decoupling though redmine

Usage:

1. define signal when some event occur

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
from gevent import monkey; monkey.patch_all()
from gevent.coros import Semaphore
from settings import *

from collections import defaultdict

#from msgpack import packb, unpackb

import cPickle as pickle
from pickle import loads as unpack, dumps as pack

from gevent.pool import Pool

import log
import gevent
import redisco
        
logger = log.getlogger("helper.signals")

class Processer(object):
    def __init__(self):
        self._listeners = defaultdict(set)
        self.channel = 'SIGNALS'
        self.rc = redisco.get_client()
        self.ps = self.rc.pubsub()
        self.ps.subscribe(self.channel)
        gevent.spawn(self._listen)

    def add_listener(self, signal, callback):
        cbname = callback.__name__
        self._listeners[signal].add(callback)
        logger.debug("{signal!r} binded by <{cbname}>".format(**locals()))

    def _listen(self):
        for m in self.ps.listen():
            if m['type'] == 'message':
                data = unpack(m['data'])
                self._execute_callbacks(data['sender'], data['signal'], **data['kwargs'])

    def send_message(self, sender, signal, **kwargs):
        data = pack( {'sender':sender,'signal':signal,'kwargs':kwargs} )       
        self.rc.publish(self.channel, data)

    def _execute_callbacks(self, sender, signal, **kwargs):
        if signal not in self._listeners:
            logger.warning("signal bindings for {signal!r} not found!".format(**locals()))
        else:
            try:
                for cb in self._listeners[signal]:
                    gevent.spawn(cb, sender, **kwargs)
                    #cb(sender, **kwargs)
            except Exception as e:
                logger.exception("Exception happened when executing callback")
                logger.error("sender: {sender}, signal: {signal!r}, kwargs: {kwargs!r}".format(**locals()))

p = Processer()

class Signal(object):
    """ a signal with capacity

    capacity specifies how many listeners can bind on this signal
    if capacity == 1, pubsub degrades to a FIFO queue, but can block on pop!
    """
    def __init__(self, name, capacity=None):
        self._name = name
        self._capacity = capacity
        self._lock = Semaphore(1)

    def send(self, sender, **kwargs):
        data = {'kwargs':kwargs}
        p.send_message(sender, self._name, **kwargs)
        
    def connect(self, callback):
        with self._lock:
            do_connect = False
            if self._capacity is not None:
                if self._capacity >= 1:
                    do_connect = True
                    self._capacity -= 1
            else:
                do_connect = True
            
            if do_connect:
                p.add_listener(self._name, callback)

    def bind(self, f):
        self.connect(f)
        def _decorator():
            return f
        return _decorator

    def __str__(self):
        return "<Signal: {name}>".format(name=self._name)

    def __repr__(self):
        return self.__str__()

class SignalQueue(Signal):
    """ a signal only can be binded once """
    def __init__(self, name, capacity=1):
        super(SignalQueue, self).__init__(name, capacity)


if __name__ == '__main__':
    after_item_init = SignalQueue("after_item_init")

    @after_item_init.bind
    def log_item_init(sender, **kwargs):
        itemid  = kwargs.get('item_id')
        print("0 sender: {sender}, itemid: {itemid}".format(**locals()))

    @after_item_init.bind
    def log_item_init(sender, **kwargs):
        itemid  = kwargs.get('item_id')
        print("1 sender: {sender}, itemid: {itemid}".format(**locals()))

    after_item_init.send(sender="main", item_id=3)
