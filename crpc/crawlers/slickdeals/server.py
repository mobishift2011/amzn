#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import re
import urllib
import lxml.html
import requests
from gevent.pool import Pool
from collections import Counter

from models import *


siteurl = 'http://slickdeals.net'
pool = Pool(1)

def crawl_several_month():
    tree = crawl_deals()
    for i in range(30):
        link = tree.xpath('//div[@id="maincontent"]/table//div[@class="pagenav_wrapper"]/div[@class="pagenav_box"]/a[contains(text(), "Next")]')[0].get('href')
        link = link if link.startswith('http') else siteurl + '/' + link
        print '\n\n', link, '\n\n'
        ret = requests.get(link)
        tree = lxml.html.fromstring(ret.content)
        for node in tree.cssselect('div#maincontent div#deal_list > a[id^="deal_header_"]'):
            pool.spawn( parse_one_product, node )
    pool.join()

def crawl_deals():
    ret = requests.get(siteurl)
    tree = lxml.html.fromstring(ret.content)
    for node in tree.cssselect('div#maincontent div#deal_list > a[id^="deal_header_"]'):
        pool.spawn( parse_one_product, node )
    pool.join()
    return tree

def parse_one_product(node):
    title = node.cssselect('span.dealblocktext h3')[0].text.strip()
    image_url = node.cssselect('span.dealblockimg img')[0].get('href')
    price = node.cssselect('span.dealblocktext h3 b')
    price = price[0].text.replace('$', '').replace(',', '').strip() if price else ''
    shipping = node.cssselect('span.dealblocktext h3 b em')
    shipping = shipping[0].text_content().strip() if shipping else ''

    manufacturer = node.cssselect('span.dealblocktext span.store')[0].text_content().strip()
    link = node.get('href')
    link = link if link.startswith('http') else siteurl + link
    key = link.rsplit('/', 1)[-1]

    original_url = find_original_url(link)

    deal = Deal.objects(key=key).first()
    if not deal:
        deal = Deal(key=key)
        deal.price = price
        deal.original_url = original_url
        deal.shipping = shipping
        deal.title = title
        deal.image_url = image_url
    else:
        if price != deal.price:
            deal.price = price
    deal.save()


def find_original_url(url):
    ret = requests.get(url)
    tree = lxml.html.fromstring(ret.content)
    link = tree.cssselect('div#maincontent div.content div.pd_img a.buynow')[0].get('href')
    jump = requests.get(link)
    if jump.url == link:
        t = lxml.html.fromstring(jump.content)
        original_url = t.cssselect('a[href]')[0].get('href')
    else:
        original_url = jump.url

    print original_url
    if 'www.eastbay.com' in original_url and 'linkshare' in original_url:
        original_url = re.compile('.*url=(.*)$').match(original_url).group(1)
        original_url = urllib.unquote(original_url)
    return original_url

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
    crawl_several_month()
    exit()
    crawl_deals()
