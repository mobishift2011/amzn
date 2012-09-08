#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import storm
import pickle

class TiebaSpout(storm.Spout):
    """ spout urls to fetch """
    def execute(self):
        for tieba in ["akb48", "oricon", "wow", "dota"]:
            url = "http://tieba.baidu.com/f?kw=" + tieba
            ret = {"url":url, "selector":'//*[@id="thread_list"]/li'}
            self.logger.debug("spouting: {0}".format(repr(ret)))
            yield ret

        # submit this job every 86400 seconds
        time.sleep(86400)

class TiebaIndexFetcher(storm.SimpleFetcher):
    """ fetches tieba index """
    pass

class TiebaIndexProcessor(storm.Bolt):
    """ extract post info from index """ 
    def execute(self, url, content):
        import lxml.html
        from zlib import decompress

        t = lxml.html.fromstring(decompress(content))
        url = "http://tieba.baidu.com" + t.xpath("div[2]/div/div[1]/a")[0].get('href')
        ret = {"url":url, "selector":'//*[@id="j_p_postlist"]/div'}
        self.logger.debug("spouting: {0}".format(repr(ret)))
        yield ret
    
class TiebaPageFetcher(storm.SimpleFetcher):
    """ fetches tieba page """
    pass

class TiebaPageProcessor(storm.Outlet):
    """ extract post content from page """
    def execute(self, url, content):
        import lxml.html
        from zlib import decompress

        content = decompress(content)
        t = lxml.html.fromstring(content)

        # extract username
        username = t.xpath("div[1]/div[1]/div[1]/ul/li[2]/a")[0].text

        # save to database
        self.logger.debug(u"saving username={0} to database".format(username))

def run_tieba_scraper():
    t = storm.Topology() 
    
    # nodes
    s  = storm.Node(TiebaSpout, 1)
    f1 = storm.Node(TiebaIndexFetcher, 1)
    p1 = storm.Node(TiebaIndexProcessor, 1, storm.FIELD_GROUPING, ('url',))
    f2 = storm.Node(TiebaPageFetcher, 12)
    p2 = storm.Node(TiebaPageProcessor, 4)
    
    # connect them
    t.add_root(s).chain(f1).chain(p1).chain(f2).chain(p2)

    # create and run 
    t.create() 
    
    pickle.dump(t, open('/tmp/topology.dump','w'))

def stop_tieba_scraper():
    t = pickle.load( open('/tmp/topology.dump') )
    t.destroy()

if __name__ == "__main__":
    run_tieba_scraper()
    print "sleep 5 seconds, then destory topology"
    time.sleep(5)
    stop_tieba_scraper()
