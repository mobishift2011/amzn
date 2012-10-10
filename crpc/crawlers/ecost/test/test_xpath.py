#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import httplib2
import lxml.html
import requests
import re

category_test_url = {
    'onlyFlag': 'http://www.ecost.com/n/Blu-Ray-Dvd-Player/mainMenu-3368',
    'Computer': 'http://www.ecost.com/n/Computers/mainMenu-2045',
    'Appliances': 'http://www.ecost.com/n/Home-Appliances/mainMenu-3305',
    'Floor': 'http://www.ecost.com/n/Floor-Care/mainMenu-3418',
    'sitemap_false': 'http://www.ecost.com/n/Site-Map/msc-163',
    'Cutlery_false': 'http://www.ecost.com/s/Cutlery?cc=CI*,CIB*,CIA*,CIC*',
    'streamer_false': 'http://www.ecost.com/s?rch&q=steamers&includeImage=true',
    'plasma_false': 'http://www.ecost.com/s/Plasma-Tv?cc=%20YFKB*,%20YFKA*',
}

def iurl_otree(url):
    http = httplib2.Http()
    resp, cont = http.request(url, 'GET')
    tree = lxml.html.fromstring(cont)
    return tree


def browseCategory():
    for k,v in category_test_url.items():
        tree = iurl_otree(v)
#        if re.compile(r'<img.*src="/croppedWidgets/images.browseCategoriesTitle.png".*?>').search(content):
        if tree.xpath('//img[@src="/croppedWidgets/images.browseCategoriesTitle.png"]'):
            print k, True
        else:
            print k, False


def second_category():
    names, links = [], []

    for k,v in category_test_url.items():
        tree = iurl_otree(v)
        if tree.xpath('//img[@src="/croppedWidgets/images.browseCategoriesTitle.png"]'):
            categorys = tree.xpath('//div[@class="nav-list wt"]/h2[@class="wt"]/span/a')
            if not categorys:
                categorys = tree.xpath('//body[@class="wbd"]/table/./tr[4]//tr/td/a[@class="wt"]')
                if not categorys:
                    continue # treat as leaf

            for category in categorys:
                link = category.get('href')
                name = category.text_content()
                names.append(name)
                links.append(link)
            print k, names, links
        else:
            num = tree.xpath('//div[@class="searchHeaderDisplayTitle"]/span[1]/text()')
            if num:
                print k, num[0]
            else:
                print k, 'not a valid page {0}'.format(v)


def listing():
    url = 'http://www.ecost.com/n/Mac-Accessories/mainMenu-2085'
    url = 'http://www.ecost.com/n/Blu-Ray-Dvd-Player/mainMenu-3368'
    url = 'http://www.ecost.com/n/Floor-Care/mainMenu-3418'

    url = 'http://www.ecost.com/s/Computer-Webcams?cc=LAOB*'

    url = 'http://www.ecost.com/s/Tower-Servers?cc=3I*&op=zones.SearchResults.pageNo&pageNo=13'
    url = 'http://www.ecost.com/s/Usb-Memory?cc=6GC*'
    url = 'http://www.ecost.com/s/Projector-Accessories?cc=MCB*&op=zones.SearchResults.pageNo&pageNo=383'
    tree = iurl_otree(url)

    ecost = []
    prices = []
    models = []
    urls, titles = [], []
    num = tree.xpath('//div[@class="searchHeaderDisplayTitle"]/span[1]/text()')
    if num:
        total_num = int(num[0])
        nodes = tree.xpath('//div[@id="searchResultList"]/div[@class="sr-table_content"]')
        for node in nodes:
            pnode = node.xpath('.//td[@class="rscontent"]/span')
            for p in pnode:
                l = p.xpath('./font[1]/text()')
                if l:
                    prices.append( l[0].replace('$', '').replace(',', '') )
                else:
                    prices.append('')
            m = node.xpath('.//td[@class="sr-item_img rscontent"]//span[@class="wt11 rsPartNo"]/text()')
            for i in m:
                temp = i.split(u'\xa0')
                # [u'eCOST Part #: 9106327 ', u' ', u' ', u' Mfr. Part #: 960-000866']
                ecost.append( temp[0].split(u':')[1].strip() )
                models.append( temp[-1].split(u':')[1].strip() if 'Mfr. Part' in temp[-1] else '' )
            url = node.xpath('.//td[@class="sr-item_img rscontent"]//span[@class="sr-item_description"]/h5/a/@href')
            for l in url:
                urls.append( l if l.startswith('http') else 'http://www.ecost.com' + l )
        print len(prices), prices
        print len(ecost), ecost
        print len(models), models
        print len(urls), urls
    else:
        price = tree.xpath('//div[@class="noDisplayPricen"]//span[starts-with(@class, "itemFinalPrice wt14")]')
        print [p.text_content().strip() for p in price]
        # link = tree.xpath('//span[@class="itemImg"]/a/@href')
        # print [l for l in link]

        links = tree.xpath('//span[@class="itemName wcB1"]/a')
        for l in links:
            urls.append( l.get('href') )
            titles.append( l.text_content().strip() )
        print len(urls), urls
        print len(titles), titles



def product():
    url = 'http://www.ecost.com/p/Gear-Head-Webcams/product~dpno~8081796~pdp.gbaiijd'
    url = 'http://www.ecost.com/p/Logitech-Webcams/product~dpno~9106327~pdp.hcjhbic'
    url = 'http://www.ecost.com/p/CP-Technologies-Webcams/product~dpno~7043006~pdp.dfhhhab'
    url = 'http://www.ecost.com/p/Sylvania-Notebook-Computers/product~dpno~9231818~pdp.hgbjcba'

    tree = iurl_otree(url)

    title = tree.xpath('//h1[@class="prodInfo wt"]/text()')[-1]
    image = tree.xpath('//td[@width]/img[@src]/@src')[0]
    if image.startswith('//'):
        image = 'http' + image
    price = tree.xpath('//td[@class="leftPane"]//td[starts-with(@class, "infoPrice infoBorderContent")]//text()')
    if not price:
        price = tree.xpath('//td[@class="leftPane"]//td[@class="infoContent infoPrice wt15"]/text()')
    print title, image, price

    node = tree.xpath('//td[@class="rightPane"]/table//tr')
    for tr in node:
        name = tr.xpath('./td[@class="infoLabel"]/text()')
        if name:
            ret = label_value(name, tr) 
            if ret:
                print name, ret[0]

    tables = tree.xpath('//div[@class="simpleTab06 wt11 wcGray1"]/div[@id="pdpTechSpecs"]//tr[@class="dtls"]')
    print dict(t.text_content().strip().split('\n\t\t\t\t') for t in tables)

def label_value(name, tr):
    if name == ['eCOST Part#:']:
        return tr.xpath('./td[@class="infoContent wcGray2"]/text()')
    elif name == ['Mfr Part#:']:
        return tr.xpath('./td[@class="infoContent wcGray2"]/text()')
    elif name == ['Usually Ships:']:
        return tr.xpath('./td[@class="infoContent"]//td[1]/a/text()')
    elif name == ['Availability:']:
        return tr.xpath('./td[@class="infoLink"]/a/text()')
    elif name == ['Platform:']:
        return tr.xpath('./td[@class="infoContent wcGray2"]/text()')
    elif name == ['Manufacturer:']:
        return tr.xpath('./td[@class="infoLink wcGray2"]/a/text()')
    elif name == ['UPC:']:
        return tr.xpath('./td[@class="infoContent wcGray2"]/text()')
    elif name == ['Customer Rating:']:
        info = tr.xpath('./td[@class="infoContent wcGray2"]/span[@class="list-ratingy"]')
        if info:
            review = info[0].text_content().strip().replace('(', '').replace(')', '')
            rating = info[0].xpath('.//li/@style')[0].split(':')[-1]
            return [(review, rating)]
        elif tr.xpath('./td[@class="infoContent wcGray2"]/span[@class="list-ratingn"]'):
            return [0]
        else:
            print 'error'




if __name__ == '__main__':
#    top()
#    browseCategory()
#    second_category()
    listing()
#    product()


