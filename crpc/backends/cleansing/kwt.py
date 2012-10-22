#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.wait
selenium.webdriver.support.wait.POLL_FREQUENCY = 0.05

import re
import time
import random
import threading
import collections
from Queue import Queue

MAX_BATCH = 50 # max batch size that google can handle

CREDENTIALS = [
    ('kwtools3456@gmail.com','1qaz2wsx!@'),
    ('kwtools3457@gmail.com','1qaz2wsx!@'),
    ('kwtools3458@gmail.com','1qaz2wsx!@'),
    ('kwtools3459@gmail.com','1qaz2wsx!@'),
    ('kwtools3460@gmail.com','1qaz2wsx!@'),
    ('kwtools3461@gmail.com','1qaz2wsx!@'),
    ('kwtools3462@gmail.com','1qaz2wsx!@'),
    ('kwtools3463@gmail.com','1qaz2wsx!@'),
    ('kwtools3464@gmail.com','1qaz2wsx!@'),
    ('kwtools3465@gmail.com','1qaz2wsx!@'),
    ('kwtools3466@gmail.com','1qaz2wsx!@'),
    ('kwtools3467@gmail.com','1qaz2wsx!@'),
    ('kwtools3468@gmail.com','1qaz2wsx!@'),
]

class AdwordsAutomater(object):
    def __init__(self, email, passwd, timeout=10):
        self.email = email
        self.passwd = passwd
        try:
            self.ff = webdriver.Chrome()
        except:
            self.ff = webdriver.Firefox()
            self.ff.set_page_load_timeout(timeout)
        self.ff.implicitly_wait(timeout)
        self.bad_network = timeout - 10
        self.busy = False
        self.is_login = False
        self.on_keyword_page = False
        self.kwurl = ''

    def login(self):
        email, passwd = self.email, self.passwd
        try:
            print 'getting adwords.google.com'
            self.ff.get('https://adwords.google.com')
        except TimeoutException:
            pass
        self.ff.find_element_by_id("Email").send_keys(email)
        self.ff.find_element_by_id("Passwd").send_keys(passwd)
        signin = self.ff.find_element_by_id('signIn')
        try:
            print 'submit login form'
            signin.submit()
        except TimeoutException:
            pass
        self.is_login = True
        time.sleep(self.bad_network)
        try:
            search = re.compile(r'(\?[^#]*)#').search(self.ff.current_url).group(1)
            self.kwurl = 'https://adwords.google.com/o/Targeting/Explorer'+search+'&__o=cues&ideaRequestType=KEYWORD_IDEAS';
        except:
            print self.ff.current_url, email, passwd

    def find_keyword_volumes(self, keywords):
        if not self.is_login:
            self.login()

        if not isinstance(keywords, collections.Iterable):
            keywords = [ keywords ]

        print self.email, 'querying', keywords
        self.busy = True
        ret = {}

        print 'visiting keyword tools'
        self.ff.get(self.kwurl)

        try:
            kwinput = self.ff.find_element_by_class_name("sEAB")
        except:
            return ret
        kwinput.send_keys('\n'.join(keywords))

        self.ff.find_element_by_css_selector("button.gwt-Button").click()

        try:
            # wait for at least one elements ready, implicitly
            self.ff.find_elements_by_xpath('//tr//*[contains(text(),"{0}")]'.format(random.choice(keywords)))
            text = self.ff.find_elements_by_xpath('//table[@class="sMNB"]')[0].text
        except Exception:
            # if we fail, fail gracefully
            print self.email, 'failed'
            pass 
        else:
            texts = text.split('\n')
            for i in range(1,len(texts)/4):
                ret[ texts[i*4] ] = (texts[i*4+2], texts[i*4+3]) 

        self.busy = False

        return ret

class KeywordSearch(object):
    def __init__(self):
        self.pool = []
        self.tasks = []
        self.rq = Queue()

        for email, passwd in CREDENTIALS:
            aa = AdwordsAutomater(email, passwd) 
            t = threading.Thread(target=aa.login)
            t.start()
            self.tasks.append(t)
            self.pool.append( aa )

        for t in self.tasks:
            t.join()

        self.tasks = []
        print 'initialized'

    def close(self):
        for aa in self.pool:
            aa.ff.quit()

    def search(self, keywords):
        if not isinstance(keywords, collections.Iterable):
            keywords = [keywords]

        if not self.pool:
            raise ValueError("No usable account!")
           
        num_left = pagenum = (len(keywords)-1)/MAX_BATCH+1
        for i in range(pagenum):
            threading.Thread(target=self._search, args=(keywords[i*MAX_BATCH:i*MAX_BATCH+MAX_BATCH],)).start()

        result = {}
        while True:
            try:
                r = self.rq.get_nowait()
            except:
                time.sleep(0.1)
            else:
                num_left -= 1
                result.update(r)
                if num_left == 0:
                    break 
        return result
        
    def _search(self, keywords):
        while True:
            found = False
            self.pool.insert(0, self.pool.pop())
            for aa in self.pool:
                if aa.busy == False:
                    aa.busy = True
                    found = True
                    break

            if not found:
                time.sleep(0.1) 
            else:
                break

        result = aa.find_keyword_volumes(keywords)
        if result == {}:
            aa.ff.quit()
            self.pool.remove(aa)
        print 'got result', result
        self.rq.put(result)
    
if __name__ == '__main__':
    #ks = KeywordSearch()
    t = time.time()
    #print ks.search(['ipad','cars','a0012k2k2','kindle','mac','beats','travel'])
    #print time.time() - t
    #t = time.time()
    #print ks.search([ str(x) for x in range(50000,51000) ])
    #print time.time() - t
    #ks.close()
    aa = AdwordsAutomater('kwtools3461@gmail.com','1qaz2wsx!@')
    print aa.find_keyword_volumes(['ipad','cars','kindle'])
