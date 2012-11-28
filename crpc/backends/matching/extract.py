#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import esm

from os.path import join, abspath, dirname

tag_path = join(dirname(abspath(__file__)), 'tags.list')

class Extracter(object):
    def __init__(self, tags=None):
        self.stopwords = ' \t\r\n,;.%0123456789\'"_-'
        self.i = None
        self.tags = tags or [ t for t in open(tag_path).read().split('\n') if t ]
        self._rebuild_index()

    def _rebuild_index(self):
        self.i = esm.Index()
        for tag in self.tags:
            self.i.enter(tag.lower(), tag)
        self.i.fix()

    def extract(self, s):
        s = s.lower()
        results = self.i.query(s)
        ret = []
        lens = len(s)
        for r in results:
            if (r[0][0] == 0 or s[ r[0][0]-1 ] in self.stopwords) and \
                (r[0][1] == lens or s[ r[0][1] ] in self.stopwords):  # the char after keyword
                    ret.append( r[1] )
        return ret

def get_site_module(site):
    return __import__('crawlers.'+site+'.models', fromlist=['Category', 'Event', 'Product'])

def extract(site):
    e = Extracter()
    m = get_site_module('myhabit')
    c = 0
    t = time.time()
    for p in m.Product.objects():
        s = p.list_info
        for name in ['summary', 'title']:
            if getattr(p, name):
                s.append(getattr(p, name))
        s = '\n'.join([ x.encode('utf-8') for x in s])
        c += 1
        #print e.extract(s), s
    time_consumed = time.time() - t
    print 'qps', c/time_consumed


if __name__ == '__main__':
    for site in ['myhabit','ruelala','zulily','hautelook','gilt','bluefly']:
        extract('myhabit')

