#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Myhabit's crawling using API """
import requests
import json
import re
from datetime import datetime, timedelta

from models import Jslinker
from models import Event, Product

class Myhabit(object):
    def __init__(self):
        self.s = requests.session()
        self.rooturl = 'http://www.myhabit.com/request/getAllPrivateSales'
        self.headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Ubuntu/12.10 Chromium/22.0.1229.94 Chrome/22.0.1229.94 Safari/537.4',
    'Cookie': 'session-id=187-2590046-5168141; session-id-time=1981953112l; session-token="Du3P0R8YKirRoBoLUW7vGfb+S4AxLHVDHugauuoNNbe7GL7+HdYVbj4R6E0qd0kOYZP1p08iLRS4ifjAM9g3q++7Lnin99mUIyiifqkyaVyFlYZgMzNQRFPtBch2NtU6zsVHt7E0ZipCJzZCBR9wa0RcALAyoWXh3O3XQ2LqcmilYQDqvGwRruHKDHBMFGrsJ8m23uWs+OU9tEn4C9p0IO9kl6t0xjv/0im28qSEE+s="; ct-main=dggZr9fLGRQ6nJUa9lswPE8VamKEexge; ubid-main=180-1581204-1041538',
    'x-amzn-auth': '187-2590046-5168141',
        }

    def check_product_right(self):
        utcnow = datetime.utcnow()
        obj = Product.objects(products_end__gt=utcnow).timeout(False)
        print 'Myhabit have {0} products.'.format(obj.count())

        for prd in obj:
            ret = self.s.get(prd.jslink, headers=self.headers)
            data = re.compile(r'parse_asin_\w+\((.*)\);$').search(ret.text).group(1)
            js = json.loads(data)
            asin = js['detailJSON']['asin']
            title = js['detailJSON']['title']
            brand = js['detailJSON']['brand']
            if 'amount' in js['detailJSON']['ourPrice']:
                price = float( js['detailJSON']['ourPrice']['amount'] )
                if price != float( prd.price.replace('$', '') ):
                    print 'myhabit product[{0}] price error: {1} vs {2}'.format(prd.combine_url, price, prd.price)
            else:
                print 'myhabit product[{0}] price can not get from network {1}'.format(prd.combine_url, prd.price)
            if 'amount' in js['detailJSON']['listPrice']:
                listprice = float( js['detailJSON']['listPrice']['amount'] )
                if listprice != float( prd.listprice.replace('$', '') ):
                    print 'myhabit product[{0}] listprice error: {1} vs {2}'.format(prd.combine_url, listprice, prd.listprice)
            else:
                print 'myhabit product[{0}] listprice can not get from network {1}'.format(prd.combine_url, prd.listprice)
            if title.lower() != prd.title.rsplit('(', 1)[0].rstrip().lower():
                print 'myhabit product[{0}] title error: {1} vs {2}'.format(prd.combine_url, [title, prd.title])
            if brand != prd.brand:
                print 'myhabit product[{0}] brand error: {1} vs {2}'.format(prd.combine_url, brand, prd.brand)


    def bootstrap_jslink(self):
        r = self.s.get(self.rooturl, headers=self.headers)
        data = json.loads(r.content)

        for event in data['sales']:
            # for each event, save all jslink info
            for product, detail in event.get('asins', {}).items():
                product_url = event['prefix'] + detail['url']
                Jslinker.objects(asin=product).update(set__jslink=product_url, upsert=True)
        print 'myhabit jslink bootstraped'


    def get_product_abstract_by_url(self, url):
        asin = re.compile(r'asin=([^&]+)').search(url).group(1)
        j = Jslinker.objects.get(asin=asin)
        jslink = j.jslink
        content = self.s.get(jslink).content
        data = re.compile(r'parse_asin_\w+\((.*)\);$').search(content).group(1)
        data = json.loads(data)
        title = data['detailJSON']['title'].encode('utf-8')
        listinfo = u'\n'.join( data['productDescription']['bullets'][0]['bulletsList'] )
        listinfo = listinfo.encode('utf-8', 'xmlcharreplace')
        return 'myhabit_'+asin, title + '\n' + listinfo

if __name__ == '__main__':
    myhabit = Myhabit()
    myhabit.check_product_right()
