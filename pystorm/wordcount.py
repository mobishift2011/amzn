#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import random
from collections import Counter

import storm

SENTENCES = [
    "the cow jumped over the moon",
    "an apple a day keeps the doctor away",
    "four score and seven years ago",
    "snow white and the seven dwarfs",
    "i am at two with nature"
]

class SentenceGenerator(storm.Spout):
    def execute(self):
        time.sleep(0.1)
        yield {"sentence":random.choice(SENTENCES)}
    
class LineSplitter(storm.Bolt):
    def execute(self, sentence):
        time.sleep(0.1)
        for word in sentence.split():
            yield {"word":word}

class CountAggregator(storm.Outlet):
    c = Counter()
    def execute(self, word):
        time.sleep(0.1)
        c = CountAggregator.c
        c[word] += 1
        print word, c[word]

def count_word():
    t = storm.Topology() 
    
    # nodes
    g = storm.Node(SentenceGenerator, 2)
    s = storm.Node(LineSplitter, 6, storm.FIELD_GROUPING, ("word",))
    c = storm.Node(CountAggregator, 3)
    
    # connect them
    t.set_root(g)
    g.add_child(s)
    s.add_child(c)

    # create and run
    t.create() 
    t.start()
    time.sleep(10)
    t.shutdown()

if __name__ == "__main__":
    count_word()
