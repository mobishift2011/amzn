#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import re
import urllib
import lxml.html
import requests
from models import *

def crawl_deals():
    siteurl = 'http://slickdeals.net'
    ret = requests.get(siteurl)
    tree = lxml.html.fromstring(ret.content)
    for node in tree.cssselect('div#maincontent div#deal_list > a[id^="deal_header_"]'):
        title = node.cssselect('span.dealblocktext h3')[0].text.strip()
        image_url = node.cssselect('span.dealblockimg img')[0].get('href')
        price = node.cssselect('span.dealblocktext h3 b')[0].text
        price = price.replace('$', '').replace(',', '') if price else ''
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
            if listprice != deal.listprice:
                deal.listprice = listprice
        deal.save()



def find_original_url(url):
    ret = requests.get(url)
    tree = lxml.html.fromstring(ret.content)
    link = tree.cssselect('div#maincontent div.content div.pd_img a.buynow')[0].get('href')
    original_url = requests.get(link).url
    if 'www.eastbay.com' in original_url and 'linkshare' in original_url:
        original_url = re.compile('.*url=(.*)$').match(original_url).group(1)
        original_url = urllib.unquote(original_url)
    return original_url

if __name__ == '__main__':
    crawl_deals()
