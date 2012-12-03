#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Myhabit's crawling using API """
import requests
import json
import re
from pprint import pprint
from datetime import datetime, timedelta

from models import Jslinker

class Myhabit(object):
    def __init__(self):
        self.s = requests.session()
        self.rooturl = 'http://www.myhabit.com/request/getAllPrivateSales'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Cookie': 'session-id=178-9157968-0478701; session-id-time=19807407421; session-token="f+qT7qj0v+IRz8TvLgLWRc3HRcHcVop9FOmKAt3sgEsUe3lJYBuJIGNobc0VJ0i6vpx1yDcadTg3NHVIzIRJBg7jbM1bOtMEx/y0sBGApDYzmsULdEyGAGT67NZkm9DX8XlrJnPlhQ/Fagv8mq+PD74d1kBfubeOzN/XDCWzeUkobmdlBDSH4WSoeC07sd3iJbZF7i61SjG9k3DxC29q0+tGNgXskOAYFBDvI+jBcFQ="; ct-main="gx?vzAAVNmUyzY55jaGNtIIb?wiE@M1P"; ubid-main=188-4772784-7788317',
            'x-amzn-auth': '178-9157968-0478701',
        }
        self.bootstrap_jslink()

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
    print myhabit.get_product_abstract_by_url('http://www.myhabit.com/#page=d&dept=men&sale=A25ZXVWLT0BY7D&asin=B009QTU916&cAsin=B009QTUEM0&ref=qd_b_img_d_1')
