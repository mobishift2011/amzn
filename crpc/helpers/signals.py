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
from gevent.queue import Queue

import log
import gevent
import redisco
        
logger = log.getlogger("helper.signals")

class Processor(object):
    rc = redisco.get_client()
    channel = 'SIGNALS'
    channelsingleton = 'SIGNALS_SINGLETON'
    signalqueue = 'SIGNALS_QUEUE'
    flagrunning = 'SIGNALS_FLAG_RUNNING'

    def __init__(self):
        if self.rc.get(self.flagrunning) != 'yes':
            self.rc.set(self.flagrunning, 'yes')
        else:
            self.rc.publish(self.channelsingleton, 'another processor forked!')

        self._listeners = defaultdict(set)
        self.ps = self.rc.pubsub()
        self.ps.subscribe(self.channel)
        self.ps2 = self.rc.pubsub()
        self.ps2.subscribe(self.channelsingleton)
        self.queues = {} # dict of Queues
        self.jobs = [
            gevent.spawn(self._channel_listener),
            gevent.spawn(self._channel_singleton),
            gevent.spawn(self._queued_executor),
            gevent.spawn_later(1, self._queue2pubsub_worker)
        ]

    def add_listener(self, signal, callback, mode):
        """ add listener to hub

        :param mode: can be 'async' or 'sync'
        """
        cbname = callback.__name__
        self._listeners[signal].add((callback, mode))
        if signal not in self.queues:
            self.queues[signal] = Queue()
        logger.debug("{signal!r} binded by <{cbname}>".format(**locals()))

    @classmethod
    def send_message(cls, sender, signal, **kwargs):
        """ send message to signalqueue """
        data = pack( {'sender':sender,'signal':signal,'kwargs':kwargs} )       
        cls.rc.rpush(cls.signalqueue, data)

    def _channel_singleton(self):
        """ receives control signals """
        for m in self.ps2.listen():
            if m['type'] == 'message':
                logger.error('You Initialized Another Processor!!')
                #gevent.killall(self.jobs)

    def _channel_listener(self):
        """ listens to the channel, execute callbacks attached to it """
        for m in self.ps.listen():
            if m['type'] == 'message':
                data = unpack(m['data'])
                self._execute_callbacks(data['sender'], data['signal'], **data['kwargs'])

    def _queue2pubsub_worker(self):
        """ Pop Message from List and Push to publish """
        while True:
            data = self.rc.blpop(self.signalqueue, timeout=5)
            if data:
                channel, message = data
                self.rc.publish(self.channel, message)

    def _queued_executor(self):
        """ callback that runs in a 'sync' mode """
        for signal, queue in self.queues.iteritems():
            gevent.spawn(self.__queued_executor, queue)

    def __queued_executor(self, queue):
        """ callback that runs in a 'sync' mode """
        while True:
            try:
                cb, sender, kwargs = queue.get() 
                cb(sender, **kwargs)
            except Exception, e:
                logger.exception(e.message)

    def _execute_callbacks(self, sender, signal, **kwargs):
        if signal not in self._listeners:
            logger.warning("signal bindings for {signal!r} not found!".format(**locals()))
        else:
            try:
                for cb, mode in self._listeners[signal]:
                    if mode == 'async':
                        gevent.spawn(cb, sender, **kwargs)
                    else:
                        # put synchronous code into a queue executor
                        self.queues[signal].put((cb, sender, kwargs))
            except Exception as e:
                logger.exception("Exception happened when executing callback")
                logger.error("sender: {sender}, signal: {signal!r}, kwargs: {kwargs!r}".format(**locals()))


class Signal(object):
    """ a signal with capacity

    capacity specifies how many listeners can bind on this signal
    if capacity == 1, pubsub degrades to a FIFO queue, but can block on pop!
    """
    p = None
    def __init__(self, name, capacity=None):
        self._name = name
        self._capacity = capacity
        self._lock = Semaphore(1)

    def send(self, sender, **kwargs):
        data = {'kwargs':kwargs}
        Processor.send_message(sender, self._name, **kwargs)
        
    def connect(self, callback, mode):
        with self._lock:
            do_connect = False
            if self._capacity is not None:
                if self._capacity >= 1:
                    do_connect = True
                    self._capacity -= 1
            else:
                do_connect = True
            
            if do_connect:
                if not Signal.p:
                    logger.warning('Initiating Global Processor for current Process, This message should only be print if you are using monitor/run.py')
                    Signal.p = Processor()
                Signal.p.add_listener(self._name, callback, mode)

    def bind(self, formode='async'):
        if hasattr(formode, '__call__'):
            # @xxx.bind
            mode = 'sync'
            f = formode
            self.connect(f, mode)
            return f
        else:
            # @xxx.bind('sync')
            mode = formode
            def _deco(f):
                self.connect(f, mode)
                return f
            return _deco

    def __str__(self):
        return "<Signal: {name}>".format(name=self._name)

    def __repr__(self):
        return self.__str__()

class SignalQueue(Signal):
    """ a signal only can be binded once """
    def __init__(self, name, capacity=1):
        super(SignalQueue, self).__init__(name, capacity)


if __name__ == '__main__':
    import time
    after_item_init = Signal("after_item_init")

    @after_item_init.bind('sync')
    def log_item_init1(sender, **kwargs):
        itemid  = kwargs.get('item_id')
        time.sleep(1)
        print("1 sender: {sender}, itemid: {itemid}".format(**locals()))

    @after_item_init.bind('sync')
    def log_item_init2(sender, **kwargs):
        itemid  = kwargs.get('item_id')
        time.sleep(2)
        print("0 sender: {sender}, itemid: {itemid}".format(**locals()))

    after_item_init.send(sender="main", item_id=3)
    time.sleep(5)
