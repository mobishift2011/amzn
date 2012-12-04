#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Tags Extractor

>>> from backends.matching.extractor import Extractor
>>> e = Extractor()
>>> e.extract('this is an sample text for extracting tags')
[u'sample']

"""
import time
import esm

from os.path import join, abspath, dirname

tag_path = join(dirname(abspath(__file__)), 'tags.list')

class Extractor(object):
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
                (r[0][1] == lens or s[ r[0][1] ] in self.stopwords) and \
                    r[1] not in ret:
                        ret.append( r[1] )
        return ret

        for match in matches:
            if (match[0][0] == 0 or brand[ match[0][0] -1 ] in self.stopwords) \
                and (match[0][1] == len(brand) or brand[ match[0][1] ] in self.stopwords) \
                ret.append(match[1])

def get_site_module(site):
    return __import__('crawlers.'+site+'.models', fromlist=['Category', 'Event', 'Product'])

def extract(site):
    e = Extractor()
    m = get_site_module(site)
    c = 0
    t = time.time()
    for p in m.Product.objects():
        s = p.list_info
        for name in ['summary', 'title']:
            if getattr(p, name):
                s.append(getattr(p, name))
        s = '\n'.join([ x.encode('utf-8') for x in s])
        c += 1
        es = e.extract(s)
        if es == []:
            print s
            raw_input()
    time_consumed = time.time() - t
    #print 'qps', c/time_consumed


if __name__ == '__main__':
    for site in ['myhabit','ruelala','zulily','hautelook','gilt','bluefly']:
        extract(site)
