#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
import httplib2

#url = 'http://www.bestbuy.com/site/Dell+-+19%22+OptiPlex+Desktop+Computer+-+4+GB+Memory+-+400+GB+Hard+Drive/5099112.p?id=1218611367672&skuId=5099112'

url = 'http://www.bestbuy.com/site/Samsung+-+Galaxy+Tab+2+10.1+with+16GB+Memory+-+Titanium+Silver/5215429.p?id=1218625359021&skuId=5215429'
url = 'http://www.bestbuy.com/site/Insignia%26%23153%3B+-+32%26%2334%3B+Class+/+LCD+/+720p+/+60Hz+/+HDTV+DVD+Combo/4677209.p?id=1218505281362&skuId=4677209'
url = 'http://www.bestbuy.com/site/Samsung+-+46%22+Class+-+LED+-+1080p+-+240Hz+-+Smart+-+3D+-+HDTV/4837437.p?id=1218540192660&skuId=4837437'

http = httplib2.Http()
response, content = http.request(url, 'GET')
tree = lxml.html.fromstring(content)
node = tree.xpath('//div[@id="content"]/div[@id="pdpcenterwell"]')[0]


#item = node.xpath('.//div[@id="productsummary"]/div[@id="financing"]//li/a/text()') # will add a \n to the tail of every field
item = node.xpath('.//div[@id="productsummary"]/div[@id="financing"]//li/a')
#['\n18-Month Financing', '\nGet 4% Back in Rewards: See How']
print [a.text_content().strip() for a in item]

item = node.xpath('.//div[@id="productdetail"]/div[@id="pdptabs"]/div[@id="tabbed-specifications"]/ul/li/div')
item = [i.text_content() for i in item]
print item

b = []
for a in item:
    if 'Customer Reviews' in a:
        break
    if a != '\n':
        b.append( a.strip('\n') )

length = len(b)
print length, b
dic = {}
i = 0
key = ''
while i < length:
    if i + 2 < length and b[i+2] == ' ':
        if key:
            dic[key].append(b[i+1])
        else:
            dic[ b[i] ] = [ b[i+1] ]
            key = b[i]
        print key, dic[key]
    else:
        key = ''
        if b[i] is ' ' or b[i] is '':
            # ['Estimated Yearly Operating Cost', '$17', '', 'UPC', '600603146435', ' ', '']
            i += 1
            if i >= length:
                break
            continue
        else:
            dic[ b[i] ] = b[i+1]
            print b[i], dic[ b[i] ]
    i += 2

item = node.xpath('.//div[@id="productdetail"]//div[@id="pdptabs"]//div[@id="tabbed-accessories"]//div[@class="prodlink"]')
print item
item = tree.xpath('//div[@id="container"]//div[@id="pdpcenterwell"]//div[@id="tabbed-accessories"]//div[@class="prodlink"]')
print item
