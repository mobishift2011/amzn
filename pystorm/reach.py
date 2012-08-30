#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import random
from collections import Counter

import storm

TWEETERS_DB = {
    "foo.com/blog/1": ["sally", "bob", "tim", "george", "nathan"],
    "engineering.twitter.com/blog/5": ["adam", "david", "sally", "nathan"],
    "tech.backtype.com/blog/123": ["tim", "mike", "john"],
}

FOLLOWERS_DB = {
    "sally": ["bob", "tim", "alice", "adam", "jim", "chris", "jai"],
    "bob": ["sally", "nathan", "jim", "mary", "david", "vivian"],
    "tim": ["alex"],
    "nathan": ["sally", "bob", "adam", "harry", "chris", "vivian", "emily", "jordan"],
    "adam": ["david", "carissa"],
    "mike": ["john", "bob"],
    "john": ["alice", "nathan", "jim", "mike", "bob"],
}

results = {}

class GetTweeter(storm.Bolt):
    def execute(self, url):
        for t in TWEETERS_DB.get(url, []):
            yield {"url",url,"tweeter":t}

class GetFollower(storm.Bolt):
    def execute(self, tweeter):
        for f in FOLLOWERS_DB.get(tweeter, []):
            yield {"url",url,"follower":f} 

class PartialUniquer(storm.Bolt):
    u = {}
    def execute(self, url, follower):
        u = PartialUniquer.u
        if url in u:
            u[url].add(follower)
        else:
            u[url] = set()
            u[url].add(follower)
        yield {"url":url, "count":len(u[url])}

class CountAggregator(storm.Bolt):
    c = Counter() 
    def execute(self, url, count):
        c[url] += count
        yield {"url":url,"reach":reach}
