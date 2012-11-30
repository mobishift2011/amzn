#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import sklearn.feature_extraction
import operator
from itertools import izip
from pprint import pprint
from stopwords import stopwords

tables = ['myhabit','hautelook', 'gilt', 'bluefly', 'ruelala', 'zulily']

def get_site_module(site):
    return __import__('crawlers.'+site+'.models', fromlist=['Category', 'Event', 'Product'])

def normalize(s):
    if isinstance(s, list):
        return '\n'.join(x.encode('utf-8') for x in s if x)
    elif s:
        return s.encode('utf-8')
    else:
        return ''

def get_document_list():
    dl = []
    for crawler in tables:
        m = get_site_module(crawler)
        for p in m.Product.objects():
            doc = normalize(p.title) + '\n' + normalize(p.list_info) + normalize(p.summary)
            doc = doc.strip()
            if doc:
                dl.append(doc)
                sys.stdout.write('.')       
                sys.stdout.flush()
    return dl

def do_counts():
    vectorizer = sklearn.feature_extraction.text.TfidfVectorizer()
    topkw = {}

    print 'generating document list from database'
    document_list = get_document_list()
    print 'document generated'

    print 'creating dimension', len(document_list), 'matrix'
    matrix = vectorizer.fit_transform(document_list)
    print 'matrix generated'

    print 'collecting term frequency'
    terms = vectorizer.get_feature_names()
    sums = matrix.sum(0).tolist()[0]
    for term, num in izip(terms, sums):
        topkw[term] = num
    print 'term frequency collected'
    
    print 'sorting dict'
    topkw_list = sorted(topkw.iteritems(), key=operator.itemgetter(1), reverse=True)

    with open('topkeywords.txt','w') as f:
        for term, score in topkw_list[:2000]:
            f.write('%-30s%s\n' % (term.encode('utf-8'), score))

if __name__ == '__main__':
    #get_document_list()
    do_counts()
