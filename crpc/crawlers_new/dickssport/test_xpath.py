#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import httplib2
import lxml.html
import requests
import re
from datetime import datetime, timedelta
from settings import *
from models import *

def url2catid(url):
    """ 1. top category: http://www.dickssportinggoods.com/category/index.jsp;jsessionid=31VQQy9V1m7Gwyxn9zjLPGLh7pKQyvSfwVLmmppY2nZZpGhPJLCr!248088961?ab=TopNav_Footwear&categoryId=4413987&sort=%26amp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bquot%3B].passthru%28%27id%27%29.exit%28%29.%24a[%26amp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bamp%3Bquot%3B
        2. category http://www.dickssportinggoods.com/category/index.jsp?categoryId=4413987
        3. leaf category: http://www.dickssportinggoods.com/family/index.jsp?categoryId=12150078
    """
    m = re.compile(r'http://www.dickssportinggoods.com/(category|family)/index.jsp(.*)categoryId=(\d+)').match(url)
    if not m:
        print url
    return m.group(1), m.group(3)


def iurl_otree(url):
    http = httplib2.Http()
    resp, cont = http.request(url, 'GET')
    tree = lxml.html.fromstring(cont)
    return tree


def top():
    url = 'http://www.bhphotovideo.com'
    tree = iurl_otree(url)

    links = tree.xpath('//div[@class="mainCategoryLinks"]//li/a/@href')
    print len(links), links
    names = tree.xpath('//div[@class="mainCategoryLinks"]//li/a/span/text()')
    print len(names), names
    print dict(zip(names, links))

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
    caturl = 'http://www.dickssportinggoods.com'
#    url = 'http://www.dickssportinggoods.com/category/index.jsp?categoryId=4414069'
    url = 'http://www.dickssportinggoods.com/category/index.jsp?categoryId=4414030'

#    url = 'http://www.dickssportinggoods.com/category/index.jsp?categoryId=4414427'
#    url = 'http://www.dickssportinggoods.com/category/index.jsp?categoryId=12137921'
#    url = 'http://www.dickssportinggoods.com/category/index.jsp?categoryId=4414021'

    tree = iurl_otree(url)

    nodes = tree.xpath('//div[@id="wrapper"]/div[@id="frame"]/div[@id="contentLeft"]/div[@class="leftNavNew "]/ul[@id="leftNavUL"]/li/a')
    if not nodes:
        nodes = tree.xpath('//div[@id="wrapper"]/div[@id="frame"]/div[@id="catLeftContent"]/div[@id="left1"]//ul/li/a')
    if not nodes: 
        print 'Url can not be parsed ', url
        return

    for node in nodes:
        link = node.get('href')
        name = node.text_content()
        if not link.startswith('http'):
            link = caturl + link
        if name.startswith("View All"):
            if url2catid(link)[0] == 'family':
                continue

        if name != 'View All':
            print name, link


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
    product()


