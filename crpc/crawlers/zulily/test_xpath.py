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
                brand.image_url = image
            brand.soldout = soldout
            brand.update_time = datetime.utcnow()
            brand.save()
            category_saved.send(sender=DB + '.get_brand_list', site=DB, key=sale_id, is_new=is_new, is_updated=not is_new)

            self.queue.put( (dept, link) )

def iurl_otree(url):
    http = httplib2.Http()
    resp, cont = http.request(url, 'GET')
    tree = lxml.html.fromstring(cont)
    return tree

def get_orm_category(url):
    catname, catn = url2catname2catn(url)
    # without first() it return a list
    cate = Category.objects(catn=catn).first()
    if cate is None:
        cate = Category(catn=catn)
        if catname:
            cate.catname = catname
    cate.update_time = datetime.utcnow()
    return cate

def second_category():
    caturl = 'http://www.myhabit.com'
    caturl = 'https://www.amazon.com/ap/signin?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&pageId=quarterdeck&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&clientContext=191-3012795-6627645&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&marketPlaceId=A39WRC2IB8YGEK&openid.assoc_handle=quarterdeck&openid.return_to=https%3A%2F%2Fwww.myhabit.com%2Fsignin&&siteState=http%3A%2F%2Fwww.myhabit.com%2Fhomepage%3Fhash%3D'
    auth = ('freesupper_fangren@yahoo.com.cn', 'forke@me')
    ss = requests.Session(auth=auth)
    cont = ss.get(caturl).content
    print cont.find(r'Sign Out')
    from requests.auth import HTTPDigestAuth
    a = requests.get(caturl, auth=HTTPDigestAuth('freesupper_fangren@yahoo.com.cn', 'forke@me'))
    print a.text.find('Sign Out')


def listing():
    url = 'http://www.cabelas.com/catalog/browse/hunting-two-way-radios/_/N-1100169/Ns-CATEGORY_SEQ_104785380?WTz_l=SBC%3Bcat104791680'
    tree = iurl_otree(url)

    try:
        nodes = tree.xpath('//div[@id="siteContent"]//div[@class="layoutCenterColumn"]/div[@class="itemsWrapper"]/div[@class="resultsColumn"]//div[@class="itemEntryInner"]')
    except:
        log.log_traceback(self.logger_list, 'Did not parse node: {0}'.format(url))
        return

    timenow = datetime.utcnow()
    time_diff = timedelta(1)
    titles = []
    prices = []
    links = []

    for node in nodes:
        price = node.xpath('.//div[@class="price"]/div/div[@class="textSale"]/text()')
        if not price:
            price = node.xpath('.//div[@class="price"]/div/div/text()')
        if not price:
            price = ''
            log.log_traceback(self.logger_list, 'do not get price {0}'.format(url))
        prices.append(price[0])
        t = node.xpath('.//id/a[@class="itemName"]')[0]
        link = t.get('href')
        links.append(link)
        title = t.text_content()
        titles.append(title)


    print len(titles), 'titles', titles
    print len(links), 'links', links
    print len(prices), 'prices', prices 
    

def product():

    url = 'http://www.dickssportinggoods.com/product/index.jsp?productId=10828736'
    url = 'http://www.dickssportinggoods.com/product/index.jsp?productId=11259348'

    url = 'http://www.dickssportinggoods.com/product/index.jsp?productId=2040792'
    url = 'http://www.dickssportinggoods.com/product/index.jsp?productId=12261498'

    url = 'http://www.dickssportinggoods.com/product/index.jsp?productId=12319729'
    tree, cont = iurl_otree(url)

    try:
        node = tree.xpath('//div[@id="wrapper"]/div[@id="frame"]/div[@id="align"]')[0]
    except:
        print 'Parsing page problem'

    also_like = []
    like = node.xpath('./div[@id="lCol"]//div[@class="mbContent"]//ul/li')
    for l in like:
        link = l.xpath('./a/@href')[0]
        title = l.xpath('./a/text()')[0]
        link = link if link.startswith('http') else 'http://www.dickssportinggoods.com' + link
        also_like.append( (title, link) )

    print also_like

    title = node.xpath('./div[@id="rCol"]//h1[@class="productHeading"]/text()')[0]
    price = node.xpath('./div[@id="rCol"]//div[@class="op"]/text()')[0]
    if not price:
        print 'Page donot have a price'
    else:
        price = price.split(':')[1].strip().replace('$', '').replace(',', '')

    print [title], [price]

    shipping = node.xpath('./div[@id="rCol"]//div[@class="fs"]//font[@class="alert"]/text()')
    img = node.xpath('./div[@id="rCol"]/div[@class="r1w secSpace"]//div[@id="galImg"]/a/img/@src')
    if not img:
        img = tree.xpath('//div[@id="wrapper"]/div[@id="frame"]/form[@name="path"]/input/@value')
    if not img:
        print 'Page donot have a image'

    if shipping:
        print [shipping],
    print [img[0]]

    info = node.xpath('./div[@id="rCol"]/div[@id="FieldsetProductInfo"]')
    description = info[0].text_content()
    available = node.xpath('./div[@id="rCol"]//div[@id="prodpad"]//div[@class="availability"]/text()')
    if available:
        # ['\n\n    \n    ', ' In stock, leaves warehouse in 1 - 2 full bus. days. ', '\n\t']
        available = ''.join(available).strip()

    print [description], [available]

    rating = node.xpath('./div[@id="rCol"]/div[@id="FieldsetCustomerReviews"]//div[@class="pr-snapshot-rating rating"]/span[@class="pr-rating pr-rounded average"]/text()')
    reviews = node.xpath('./div[@id="rCol"]/div[@id="FieldsetCustomerReviews"]//div[@class="pr-snapshot-rating rating"]//span[@class="count"]/text()')
    comment = []
    comment_all = node.xpath('./div[@id="rCol"]/div[@id="FieldsetCustomerReviews"]//div[starts-with(@id, "pr-contents-")]//div[@class="pr-review-wrap"]')
    for comm in comment_all:
        rate = comm.xpath('.//span[@class="pr-rating pr-rounded"]/text()')
        head = comm.xpath('.//p[@class="pr-review-rating-headline"]/text()')
        text = comm.xpath('./div[@class="pr-review-main-wrapper"]//p[@class="pr-comments"]/text()')
        comment.append( (rate, head, text) )

    print [rating], [reviews], '++', comment
    m = re.compile(r'.*(Model|Model Number):(.*)\n').search(description)
    if m:
        model = m.group(2).strip()
        print model


if __name__ == '__main__':
#    top()
#    second_category()
#    listing()
#    product()

    email = 'freesupper_fangren@yahoo.com.cn'
    passwd = 'forke@me'
    lgin = myhabitLogin(email, passwd)
    lgin.login()
    lgin.crawl_category()

