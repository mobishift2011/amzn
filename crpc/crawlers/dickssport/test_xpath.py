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
    url = 'http://www.cabelas.com/product/Boating/Electric-Trolling-Motors/Bow-Mount%7C/pc/104794380/c/104716980/sc/104233680/MotorGuide174-Brute-Series-Bow-Mount-150-75-FB/1152272.uts?destination=%2Fcatalog%2Fbrowse%2Fboating-electric-trolling-motors-bow-mount%2F_%2FN-1100545%2FNs-CATEGORY_SEQ_104233680%3FWTz_l%3DSBC%253BMMcat104794380%253Bcat104716980&WTz_l=SBC%3BMMcat104794380%3Bcat104716980%3Bcat104233680'
    url = 'http://www.cabelas.com/product/Hunting/Hunting-Game-Calls/Turkey-Calls|/pc/104791680/c/104725980/sc/104662980/WoodHaven-TKM-Diaphragm-Call-Three-Pack/1324129.uts?destination=%2Fcatalog%2Fbrowse%2Fhunting-hunting-game-calls-turkey-calls%2F_%2FN-1100097%2FNs-CATEGORY_SEQ_104662980%3Fpcrid%3D8195158497%26WTz_l%3DSBC%253BMMcat104791680%253Bcat104725980&WTz_l=SBC%3BMMcat104791680%3Bcat104725980%3Bcat104662980'

    url = 'http://www.cabelas.com/product/714212.uts'
    url = 'http://www.cabelas.com/product/738848.uts'
    url = 'http://www.cabelas.com/product/755814.uts'
#    url = 'http://www.cabelas.com/product/1328017.uts'
    tree, cont = iurl_otree(url)

    try:
        node = tree.xpath('//div[@id="siteContent"]//div[@id="productDetailsTemplate"]/div[@class="layoutWithRightColumn"]')[0]
    except:
        log.log_traceback(self.logger_product, 'Parsing page problem: {0}'.format(url))

    timenow = datetime.utcnow()

    also_like = []
    like = node.xpath('./div[@class="layoutRightColumn"]/div[@class="youMayAlsoLike"]//div[@class="item"]//a[@class="itemName"]')
    for l in like:
        link = l.get('href') if l.get('href').startswith('http') else 'http://www.cabelas.com' + l.get('href')
        also_like.append( (l.text_content(), link) )

#    img = node.xpath('./div[@class="layoutCenterColumn"]/div[@class="js-itemImageViewer itemImageInclude"]/img/@src')
    img = tree.xpath('/html/head/meta[@property="og:image"]/@content')
    image = img[0] if img else ''

    info = node.xpath('./div[@class="layoutCenterColumn"]/div[@id="productInfo"]')[0]
    available = info.xpath('.//div[@class="variantConfigurator"]//div[@class="stockMessage"]/span/text()')
    if not available:
        if info.xpath('.//div[@class="variantConfigurator"]//div[@class="js-availabilityMessage"]'):
            jsid = re.compile(r"ddWidgetEntries\['js-vc13280170'] =(.*), values ").search(cont).group(1).split(':')[-1].strip()
            post_data = {
                'productVariantId': jsid,
            }
            jsurl = 'http://www.cabelas.com/catalog/includes/availabilityMessage_include.jsp'
            sess = requests.Session()
            resp_cont = sess.post(jsurl, data=post_data).content
            available = re.compile(r'<span class="availabilityMessage">(.*)</span>').search(resp_cont).group(1)

    price = info.xpath('.//div[@class="price"]/dl[@class="salePrice"]/dd[1]/text()')
    if not price:
        price = info.xpath('.//div[@class="price"]/dl[1]/dd[1]/text()')
    if not price:
        avail = info.xpath('.//div[@class="variantConfigurator"]/span[@class="soldOut"]/text()')
        if avail == ['Sold Out']:
            available = 'Sold Out'

    price = price[0].replace(',', '').replace('$', '')

    itemNO = info.xpath('.//div[@class="variantConfigurator"]//span[@class="itemNumber"]/text()') # this xpath need strip()
    if not itemNO:
        itemNO = tree.xpath('//div[@id="siteContent"]//div[@class="w100"]/meta[1]/@content')
    if not itemNO:
        print 'Page donot have a itemNO: {0}'.format(url)
    else:
        itemNO = itemNO[0].strip()


    ship = info.xpath('.//div[@class="bottomNote"]//td/img/@alt')
    if ship and ship[0] == 'In-Store Pick Up':
        shipping = 'free shipping'
    else:
        shipping = ''


    desc = node.xpath('./div[@class="layoutCenterColumn"]/div[@id="tabsCollection"]//div[@id="description"]')
    description = desc[0].text_content()

    if node.xpath('./div[@class="layoutCenterColumn"]/div[@id="tabsCollection"]//div[@class="panel"]//div[@id="RRQASummaryBlock"]/div[@id="BVRRSummaryContainer"]'):
        jsurl = 'http://reviews.cabelas.com/8815/{0}/reviews.djs?format=embeddedhtml'.format(itemNO.split('-')[-1])
        tree, rating_content = iurl_otree(jsurl)
        m = re.compile(r'<span class=\\"BVRRNumber BVRRRatingNumber\\">(.*?)<\\/span>').search(rating_content)
        if m:
            rating = float(m.group(1))
        m = re.compile(r'<span class=\\"BVRRNumber BVRRBuyAgainTotal\\">(.*?)<\\/span>').search(rating_content)
        if m:
            review = float(m.group(1))
        print rating, review


    model = []
    models = node.xpath('./div[@class="layoutCenterColumn"]/div[@id="productChart"]//tbody/tr/td[1]/text()')
    for m in models:
        model.append(m)

    print also_like
    print image, itemNO, shipping
    print price, available
    print description
    print model


if __name__ == '__main__':
#    top()
    second_category()
#    listing()
#    product()


