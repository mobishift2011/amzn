#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from gevent.pool import Pool
import re
import requests
import urllib
import lxml.html
from collections import Counter
from models import *

siteurl = 'http://www.techbargains.com'
pool = Pool(50)

def crawl_several_month():
    for i in range(2, 90):
        url = 'http://www.techbargains.com/recentnews.cfm?recent={0}'.format(i)
        print '\n\n', url , '\n\n'
        ret = requests.get(url)
        tree = lxml.html.fromstring(ret.content)
        for node in tree.cssselect('div#generalNews div.CBoxTDeal div.CBoxTDealStyling'):
            pool.spawn( parse_one_product, node )
    pool.join()


def crawl_deals():
    ret = requests.get(siteurl)
    tree = lxml.html.fromstring(ret.content)
    for node in tree.cssselect('div#generalNews div.CBoxTDeal div.CBoxTDealStyling'):
        parse_one_product(node)


def parse_one_product(node):
    title = node.cssselect('div.rightSort div.upperrightSort a')[0].text_content().strip()
    desc = node.cssselect('div.rightSort div.contentrightSort')[0].text_content().strip()
    info = node.cssselect('div.thumbnailPriceColumn')[0]
    listprice = info.cssselect('div.strikedtext')
    listprice = listprice[0].text_content().replace('$', '').replace(',', '') if listprice else ''
    price = info.cssselect('div.redboldtext')
    price = price[0].text_content().replace('$', '').replace(',', '') if price else ''
    shipping = info.cssselect('div.extraText')
    shipping = shipping[0].text_content() if shipping else ''

    image_url = info.cssselect('img[title]')[0].get('data-original')

    expired = True if node.cssselect('div.expiredDealIndicator') else False

    try:
        link = info.cssselect('a')[0].get('href')
        link = link if link.startswith('http') else siteurl + link
        key = re.compile('.*clkSubId=(\w+)&').match(link).group(1)
    except:
        print title,
        print link
        return

    original_url = find_original_url(link)

    deal = Deal.objects(key=key).first()
    if not deal:
        deal = Deal(key=key)
        deal.price = price
        deal.listprice = listprice
        deal.original_url = original_url
        deal.shipping = shipping
        deal.title = title
        deal.description = desc
        deal.image_url = image_url
        deal.expired = expired
    else:
        if price != deal.price:
            deal.price = price
        if listprice != deal.listprice:
            deal.listprice = listprice
        if expired != deal.expired:
            deal.expired = expired
    deal.save()


def find_original_url(url):
    ret = requests.get(url)
    tree = lxml.html.fromstring(ret.content)
    link = tree.cssselect('a#clickLink')[0].get('href')
    if not link.startswith('http'):
        link = siteurl + link
    extract_link = re.compile('.+=(http%3A%2F%2F.*$)').match(link)
    if extract_link:
        return_url = urllib.unquote( extract_link.group(1) )
    else:
        return_url = requests.get(link).url
    print return_url
    return return_url


def statistics_source_site():
    cnt = Counter()
    for d in Deal.objects().timeout(False):
        try:
            site = re.compile('https?://(.*?)/').match(d.original_url).group(1)
            cnt[site] += 1
        except:
            print d.original_url
    print cnt.most_common()

if __name__ == '__main__':
    statistics_source_site()
    exit()
    crawl_several_month()
    crawl_deals()
