#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import esm

class Extracter(object):
    def __init__(self):
        self.i = esm.Index()
        tags = [ t.lower() for t in open('tags.list').read().split('\n') if t ]
        for tag in tags:
            self.i.enter(tag)
        self.i.fix()
        self.stopwords = ' \t\r\n,;.%\d+\'"_-'

    def extract(self, s):
        results = self.i.query(s)
        ret = []
        for r in results:
            if (r[0][0] == 0 or s[ r[0][0]-1 ] in self.stopwords) and \
                (r[0][1] == -1 or s[ r[0][1] ] in self.stopwords):  # the char after keyword
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

