#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#import httplib2
import Queue
import lxml.html
import requests
import re
from datetime import datetime, timedelta
#from settings import *
#from models import *

from selenium import webdriver
class myhabitLogin(object):
    def __init__(self, email=None, passwd=None):
        if email:
            self.email, self.passwd = email, passwd
        else:
            return
        try:
            self.browser = webdriver.Chrome()
        except:
            self.browser = webdriver.Firefox()
            self.browser.set_page_load_timeout(5)

    def login(self):
        self.browser.get('http://www.myhabit.com')
        self.browser.find_element_by_id('ap_email').send_keys(email)
        self.browser.find_element_by_id('ap_password').send_keys(passwd)
        signin_button = self.browser.find_element_by_id('signInSubmit')
        signin_button.submit()

    def crawl_category(self):
        depts = ['women', 'men', 'kids', 'home', 'designer']
        self.queue = Queue.Queue()
        self.upcoming_queue = Queue.Queue()

        for dept in depts:
            link = 'http://www.myhabit.com/homepage?#page=g&dept={0}&ref=qd_nav_tab_{0}'.format(dept)
            self.get_brand_list(dept, link)
        self.cycle_crawl_category()

        while not self.queue.empty():
            print self.queue.get()

    def get_brand_list(self, dept, url):
        self.browser.get(url)
        nodes = self.browser.find_elements_by_xpath('//div[@id="main"]/div[@id="page-content"]/div[@id="currentSales"]/div[starts-with(@id, "privateSale")]/div[@class="caption"]/a')
        for node in nodes:
            try: # if can't be found, cost a long time and raise NoSuchElementException
                node.find_element_by_xpath('./div[@class="image"]/a/div[@class="soldout"]')
            except:
                soldout = False
            else:
                soldout = True
            print soldout
            image = node.find_element_by_xpath('./div[@class="image"]/a/img').get_attribute('src')
            a_title = node.find_element_by_xpath('./div[@class="caption"]/a')
            l = a_title.get_attribute('href')
            link = l if l.startswith('http') else 'http://www.myhabit.com/homepage' + l
            sale_id = self.url2saleid(link)

            brand, is_new = Category.objects.get_or_create(pk=sale_id)
            if is_new:
                brand.dept = dept
                brand.sale_title = a_title.text
                brand.image_urls = [image]
            brand.soldout = soldout
            brand.update_time = datetime.utcnow()
            brand.save()
            category_saved.send(sender=DB + '.get_brand_list', site=DB, key=sale_id, is_new=is_new, is_updated=not is_new)

            self.queue.put( (dept, link) )



if __name__ == '__main__':

    email = 'freesupper_fangren@yahoo.com.cn'
    passwd = 'forke@me'
    lgin = myhabitLogin(email, passwd)
    lgin.login()
    lgin.crawl_category()

