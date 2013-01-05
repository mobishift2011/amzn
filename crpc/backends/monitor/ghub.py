#!/usr/bin/env python
""" We register every Greenlet here so we can kill them later on
"""
import gevent

class GHub(object):
    """Among all the Greenlets we spawn, there are four categories of them
    
    1. the tasks that we spawns
    2. the schedulers that arranges the tasks, aka, acs
    3. the essentials we need to keep the program functioning correctly
    4. those spawned by the signals

    category 3 can be ignored, and it's same to category 4, because we decided that signals should execute and finish very soon.
    the main greenlets we focus here will be ``tasks``, and ``schedulers``  
    """
    _instance = None

    greenlets = {
        'tasks': [],
        'acs': [],
        'essentials': [],
        'signal_executors': [], 
    }

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GHub, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
   
    @classmethod
    def extend(cls, category='tasks', tasks=[]):
        cls.greenlets[category].extend(tasks)

    @classmethod
    def stop(cls, category='tasks'):
        if cls.greenlets[category]:
            gevent.killall(cls.greenlets[category], block=True) 
            cls.greenlets[category] = []

    @classmethod 
    def has_greenlets(cls, category='acs'):
        return cls.greenlets[category]

    @classmethod
    def acs_exists(cls):
        return bool(cls.has_greenlets('acs'))
