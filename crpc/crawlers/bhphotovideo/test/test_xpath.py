#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import httplib2
import lxml.html
import requests
import re

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


def second_category():
#    url = 'http://www.bhphotovideo.com/c/browse/Professional-Audio/ci/12154/N/4294550705'
#    url = 'http://www.bhphotovideo.com/c/browse/Professional-Video-Tapes/ci/9957/N/4294548481'
#    url = 'http://www.bhphotovideo.com/c/buy/Roll-Film/ci/2545/N/4294548524'
#    url = 'http://www.bhphotovideo.com/c/browse/Musical-Instruments-Accessories/ci/12156/N/4294550192'

    tree = iurl_otree(url)

    items = tree.xpath('//div[@class="tMain"]//div[@class="column"]//li/a')
    if not items:
        items = tree.xpath('//div[@class="tMain"]//table[@class="catColumn"]//tr[@valign="top"]//a')

    if items:
        links = [item.get('href') for item in items]
        names = [item.text_content() for item in items]
    else:
        items = tree.xpath('//div[@id="mainContent"]//div[@class="categoryGroup staticBody"]/div/a')
        if items:
            links = [item.get('href') for item in items]
            names = [item.xpath('.//img')[0].get('alt') for item in items]
        else:
            links, names = [], []
            try:
                num = tree.xpath('//div[@class="tMain"]//div[@id="Plistbar"]/div[@id="PfirstRow"]/span[@id="PitemNum"]/text()')[0]
                total_num = int(num.replace('\t', '').strip().split('\n')[-1].split()[0])
            except:
                print '!! {0} neither a category nor a list page'.format(url)
            finally:
                print total_num

    print len(links), links
    print len(names), names
    

def listing():
    url = 'http://www.bhphotovideo.com/c/buy/Drum-Machines/ci/4883/N/4294550181'
#    url = 'http://www.bhphotovideo.com/c/buy/Camcorders/ci/1871/N/4294548093'
#    url = 'http://www.bhphotovideo.com/c/buy/Card-Readers/ci/1096/N/4204446866'

#    url = 'http://www.bhphotovideo.com/c/buy/PAL-Camcorders-Cameras/ci/18228/pn/1/N/4175089459'
    url = 'http://www.bhphotovideo.com/c/buy/KVM-Cables/ci/11482/N/4206279350'
    tree = iurl_otree(url)
    iter_ret = tree.xpath('//div[@class="tMain"]//div[starts-with(@class, "productBlock clearfix ")]')

    num = tree.xpath('//div[@class="tMain"]//div[@id="Plistbar"]/div[@id="PfirstRow"]/span[@id="PitemNum"]/text()')[0]
    total_num = int(num.replace('\t', '').strip().split('\n')[-1].split()[0])
    print total_num

    bahs = []
    images = []
    urls = []
    reviews = []

    brands = []
    titles = []
    description = []
    available = []
    models = []
    prices = []
    shippings = []
    for j in xrange(len(iter_ret)):
        bah = iter_ret[j].xpath('.//div[@class="productBlockCenter"]/div[@class="points"]//li[1]/span[@class="value"]/text()')[0]
        node = iter_ret[j].xpath('.//div[@class="productBlockLeft"]')[0]
        image = node.xpath('./a/img/@src')[0]
        image = 'http://www.bhphotovideo.com' + image
        url = node.xpath('./a/@href')[0]
        review = node.xpath('./div[@class="ratingBox"]/a[@class="info"]/text()')
        if review:
            m =re.compile('\d+').search(review[0])
            reviews.append(m.group())
        else:
            reviews.append('')

        bahs.append(bah)
        images.append(image)
        urls.append(url)


        node = iter_ret[j].xpath('.//div[@class="productBlockCenter"]')[0]
        brand = node.xpath('./div[@class="clearfix"]/div[@class="brandTop"]/text()')[0]
        title = node.xpath('./div[@id="productTitle"]//a/text()')[0]
        desc = node.xpath('./ul/li')
        desc = [d.text_content() for d in desc]
        avail = node.xpath('.//div[@class="availability"]//text()')
        avail = [a.strip() for a in avail if not a.isspace()]

        brands.append(brand)
        titles.append(title)
        description.append(desc)
        available.append(avail)

        model = iter_ret[j].xpath('.//div[@class="productBlockCenter"]/div[@class="points"]//li[2]/span[@class="value"]/text()')
        if model:
            models.append(model[0])
        else:
            models.append('')

        price = iter_ret[j].xpath('.//div[@id="productRight"]/ul[starts-with(@class, "priceList ")]/li[@class]/span[@class="value"]/text()')
        if price:
            price = price[0].replace(',', '').replace('$', '')
        else:
            price = iter_ret[j].xpath('.//div[@id="productRight"]/ul[@class="priceList "]/li[@class="map youPay"]/span[@class="value"]/text()')
            if price:
                price = price[0].strip().replace(',', '').replace('$', '')
            else:
                data = iter_ret[j].xpath('.//div[@id="productRight"]/ul[@class="priceList priceContainer"]/li[contains(@class, "cartLinkPrice")]/@data-href')
                if data:
                    param0, param1 = ['string:{0}'.format(i) for i in data[0].split('_')]
                    page = '/c/buy/Drum-Machines/ci/4883/N/4294550181'
                    cinum = '4883'
                    param3 = 'string:cat@__{0}@__type@__PrdLst'.format(cinum)
                    param4 = 'string:' + cinum
                    post_data = { 
                        'c0-methodName': 'addToCart',
                        'c0-scriptName': 'DWRHelper',
                        'c0-id': '0',
                        'batchId': '10',
                        'callCount': '1',
                        'windowName': 'bhmain',
                        'page': page,
                        'httpSessionId': 'wwh9QYSPBd!-1310320805',
                        'scriptSessionId': '60F4DF55163FC3A41DF6C7B70D572C73',
                        'c0-param0': param0,
                        'c0-param1': param1,
                        'c0-param2': 'string:1',
                        'c0-param3': param3,
                        'c0-param4': param4
                    }
                    jsurl = 'http://www.bhphotovideo.com/bnh/dwr/call/plaincall/DWRHelper.addToCart.dwr'
                    s = requests.session()
                    resp = s.post(jsurl, data=post_data).content
                    m = re.compile(r'<span class=\\"atcLayerPricePrice\\">(.*?)</span>').search(resp)
                    price = m.group(1).replace('\\n', '').replace(' ', '').replace(',', '').replace('$', '')


        if price:
            prices.append(price)
        else:
            price.append('')

        shipping = iter_ret[j].xpath('.//div[@id="productRight"]/ul[contains(@class, "priceList ")]/li[last()]/a/text()')
        if shipping:
            shippings.append(shipping[0])
        else:
            shippings.append('')

    print len(bahs),'bahs', bahs
    print len(reviews), 'reviews', reviews
    print len(images), 'images', images
    print len(urls), 'urls', urls
    print len(brands), 'brands', brands
    print len(titles), 'titles', titles
    print len(description), description
    print len(available), 'avaiable', available
    print len(models), 'models', models
    print len(prices), 'prices', prices 
    print len(shippings), 'shippings', shippings
    

def product():
    url = 'http://www.bhphotovideo.com/c/product/871872-REG/Apple_MD231LL_A_Macbook_Air_Ci5_1_8g_4GB_128GB_SSD_13_3.html'
    url = 'http://www.bhphotovideo.com/c/product/749190-REG/Canon_4923B002_VIXIA_HF_G10_Flash.html'
#    url = 'http://www.bhphotovideo.com/c/product/79228-REG/Ilford_1771318_Multigrade_IV_RC_DLX.html'

    url = 'http://www.bhphotovideo.com/c/product/817095-REG/Canon_XF105E_XF105_HD_Professional_PAL.html'

    tree = iurl_otree(url)
    node = tree.xpath('//div[@class="tMain"]//div[@id="productAllWrapper"]/div[@id="productMainWrapper"]')[0]

    bill_later = node.xpath('.//div[@id="productRight"]//div[contains(@class, "altPayment findLast")]//li/a//text()')
    print [a.strip() for a in bill_later]

    buy_together = tree.xpath('.//div[@class="productInfoArea adm findLast"]/a/@href')
    if buy_together:
        intree = iurl_otree(buy_together[0])
        ones = intree.xpath('//div[@class="ui-dialog-content"]//div[@class="col titleDetails"]')
        for one in ones:
            title = one.xpath('./div[@class="title"]/span//text()')
            info = [t.strip() for t in title if t.strip()]
            model = one.xpath('./div[@class="details"]/p/text()')[0]
            info.append(model)
            print info

    specifications = {}
    tables = node.xpath('.//div[@id="bottomWrapper"]//div[@id="Specification"]//table[@class="specTable"]')
    for table in tables:
        key = table.xpath('.//tr/td[@class="specTopic"]')
        value = table.xpath('.//tr/td[@class="specDetail"]')
        k = [k.text_content().strip() for k in key]
        v = [v.text_content().strip() for v in value]
        specifications.update(dict( zip(k, v) ))
    print specifications

    in_box = node.xpath('.//div[@id="bottomWrapper"]//div[@id="WhatsInTheBox"]/ul/li')
    print [a.text_content().strip() for a in in_box]

    rating = node.xpath('.//div[@id="bottomWrapper"]//div[@id="costumerReview"]//div[@class="pr-snapshot-rating rating"]/span/text()')
    print rating

#    items = node.xpath('.//div[@id="bottomWrapper"]//div[@class="accGroup "]//form[@class="addToCartForm"]//div[@class="accDetails"]')
    items = node.xpath('.//div[@id="bottomWrapper"]//div[@id="ui-tabs-1"]')
    print items
    for item in items:
        title = item.xpath('./div[1]')
        print title[0].text_content()
        model = item.xpath('./div[@class="ItemNum"]/span')
        print model[0].text_content()



if __name__ == '__main__':
#    top()
#    second_category()
#    listing()
    product()


