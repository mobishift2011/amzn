#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import re
import requests
import lxml.html
from models import *

def crawl_deals():
    siteurl = 'http://www.techbargains.com'
    ret = requests.get(siteurl)
    tree = lxml.html.fromstring(ret.content)
    for node in tree.cssselect('div#generalNews div.CBoxTDeal div.CBoxTDealStyling'):
        title = node.cssselect('div.rightSort div.upperrightSort')[0].text_content().strip()
        desc = node.cssselect('div.rightSort div.contentrightSort')[0].text_content().strip()
        info = node.cssselect('div.thumbnailPriceColumn')[0]
        listprice = info.cssselect('div.strikedtext')
        listprice = listprice[0].text_content().replace('$', '').replace(',', '') if listprice else ''
        price = info.cssselect('div.redboldtext')
        price = price[0].text_content().replace('$', '').replace(',', '') if price else ''
        shipping = info.cssselect('div.extraText')
        shipping = shipping[0].text_content() if shipping else ''
        image_url = info.cssselect('a img')[0].get('data-original')

        link = info.cssselect('a')[0].get('href')
        link = link if link.startswith('http') else siteurl + link
        try:
            key = re.compile('.*clkSubId=(\w+)&').match(link).group(1)
        except:
            continue

        original_url = extract_original_url(link)

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
        else:
            if price != deal.price:
                deal.price = price
            if listprice != deal.listprice:
                deal.listprice = listprice
        deal.save()


def extract_original_url(url):
    ret = requests.get(url)
    tree = lxml.html.fromstring(ret.content)
    link = tree.cssselect('a#clickLink')[0].get('href')
    return_url = requests.get(link).url
    return return_url


if __name__ == '__main__':
    crawl_deals()
