#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import requests
import lxml.html
import time
import re
import pickle

nodes = [
    '1036592',      # Clothing & Accessories
    '672123011',    # Shoes
    '15743631',     # Handbags
    '1036700',      # Accessories
    '15743161',     # Luggage & Bags
    '3367581',      # Jewelry
    '377110011',    # Watches
    '3760911',      # Beauty
    #'1040662',      # Kids // through clothing
    '228013',       # Tools & Home Improvment
]

nodepattern = re.compile(r'%3A(\d+)&bbn')

def filter_rubbish(s):
    if 'AmazonGlobal Eligible' == s or \
        s.startswith('1') or \
        s.startswith('2') or \
        s.startswith('3') or \
        s.startswith('4') or \
        s.startswith('5') or \
        s.startswith('6') or \
        s.startswith('7') or \
        s.startswith('8') or \
        s.startswith('9') or \
        s in ['M', 'S', 'L', 'XS']:
        return True

def extract_tags(tree):
    #return set(x.text for x in tree.xpath('//span[@class="refinementLink"]'))
    thetags = []
    for x in tree.xpath('//div[@id="leftNavContainer"]//ul')[0].xpath('.//span[@class="refinementLink"]'):
        if filter_rubbish(x.text):
            break
        thetags.append(x.text)
    print 'sub category', thetags
    for keyword in ['Style', 'Shape', 'Height', 'Type', 'Feature', 'Special']:
        for h2 in tree.xpath('//h2[contains(text(),"{0}")]'.format(keyword)):
            keyword_tags = [ ]
            for x in h2.getnext().xpath('.//span[@class="refinementLink"]'):
                if filter_rubbish(x.text):
                    break
                keyword_tags.append(x.text)
            print 'keyword', keyword, keyword_tags
            thetags.extend( keyword_tags )
    return thetags

def extract_children_nodes(tree):
    nodes = []
    try:
        for x in tree.xpath('//div[@id="leftNavContainer"]//ul')[0].xpath(".//a"):
            nodes.append( nodepattern.search(x.get('href')).group(1) )
    except:
        pass
    return nodes

def node2url(node):
    return 'http://www.amazon.com/s/?rh=n%3A'+node
   
import gevent.queue
import gevent.pool

nodes_queue = gevent.queue.Queue()
nodes_processed = set()
tags = set()


def process_node(node):
    if node not in nodes_processed:
        nodes_processed.add(node)
    
        print 'processing node', node
        content = requests.get(node2url(node)).content

        tree = lxml.html.fromstring(content)
    
        new_nodes = extract_children_nodes(tree)
        for node in new_nodes:
            nodes_queue.put(node)
        tags.update( extract_tags(tree) )
        print 'tags size', len(tags)
    

def extract_tags_from_amazon():
    pool = gevent.pool.Pool(30)

    for node in nodes:
        nodes_queue.put(node)
    
    idle_count = 0

    while idle_count<30:
        try:
            node = nodes_queue.get_nowait()
        except Exception, e:
            #import traceback
            #traceback.print_exc()
            # no values in queue, we wait 1 second
            pickle.dump(tags, open('/tmp/tags.dump','w'))
            time.sleep(1)
            idle_count += 1
        else:
            pool.spawn(process_node, node) 
    
    pool.join()


if __name__ == '__main__':
    extract_tags_from_amazon()
