#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Myhabit's crawling using API """
from gevent import monkey; monkey.patch_all()
import gevent.pool

import requests
import json
import re
from pprint import pprint
from datetime import datetime, timedelta

from models import Product, Event
from crawlers.common.events import common_saved

def time2utc(t):
    """ convert myhabit time format (json) to utc """
    return datetime.fromtimestamp(t['time']/1000.) + timedelta(minutes=t['offset'])
   

class Server(object):
    def __init__(self):
        self.rooturl = 'http://www.myhabit.com/request/getAllPrivateSales'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Cookie': 'session-id=178-9157968-0478701; session-id-time=19807407421; session-token="f+qT7qj0v+IRz8TvLgLWRc3HRcHcVop9FOmKAt3sgEsUe3lJYBuJIGNobc0VJ0i6vpx1yDcadTg3NHVIzIRJBg7jbM1bOtMEx/y0sBGApDYzmsULdEyGAGT67NZkm9DX8XlrJnPlhQ/Fagv8mq+PD74d1kBfubeOzN/XDCWzeUkobmdlBDSH4WSoeC07sd3iJbZF7i61SjG9k3DxC29q0+tGNgXskOAYFBDvI+jBcFQ="; ct-main="gx?vzAAVNmUyzY55jaGNtIIb?wiE@M1P"; ubid-main=188-4772784-7788317',
            'x-amzn-auth': '178-9157968-0478701',
        }

    def crawl_category(self, ctx):
        r = requests.get(self.rooturl, headers=self.headers)
        data = json.loads(r.text)

        for event in data['sales']:
            self._parse_event(event, ctx)

            # for each event, crawl all the products below
            for product, detail in event.get('asins', {}).items():
                product_url = event['prefix'] + detail['url']
                Product.objects(key=product).update(set__jslink=product_url, set__asin=product, updated=False, upsert=True)


    def crawl_product_plus(self):
        pool = gevent.pool.Pool(30)
        for p in Product.objects(updated=None):
            if not p.jslink:
                print p.key, p.jslink, 'not found'
                continue
            pool.spawn(self._parse_product, requests.get(p.jslink).text, 'haha')
        pool.join()

    def get_product_abstract_by_url(self, url):
        asin = re.compile(r'asin=([^&]+)').search(url).group(1)
        p = Product.objects.get(key=asin)
        jslink = p.jslink
        content = requests.get(jslink).content
        data = re.compile(r'parse_asin_\w+\((.*)\);$').search(content).group(1)
        data = json.loads(data)
        title = data['detailJSON']['title']
        listinfo = '\n'.join( data['productDescription']['bullets'][0]['bulletsList'] )
        return title.replace(' ','_')+'_'+jslink.rsplit('/',1)[-1][:-3], title + '\n' + listinfo

    def _parse_event(self, event, ctx):
        event_id = event['id']

        is_new = False
        e = Event.objects(event_id=event_id).first()
        if not e:
            is_new = True
            e = Event(event_id=event_id)

        info = event['saleProps']

        # updating fields
        e.events_begin = time2utc(event['start'])
        e.events_end = time2utc(event['end'])
        e.update_time = datetime.utcnow()
        e.dept = event['departments']
        e.sale_title = info['primary']['title']
        e.sale_description = info['primary']['desc']
        e.image_urls = [ info['prefix']+val for key, val in info['primary']['imgs'].items() if val in ['desc','hero', 'sale'] ]
        e.combine_url = event['prefix'] + event['url']
            
        # if it is an upcoming event, it's not that urgent, vice versa
        e.urgent = False if event.get('dataType') == 'upcoming' else True

        # get changed fields, this is ugly but works
        is_updated = True if e._get_changed_fields() else False
       
        e.save()
        common_saved.send(sender=ctx, key=e.event_id, url=e.combine_url, is_new=is_new, is_updated=is_updated)

    def _parse_product(self, content, ctx):
        # FIXME this parse is far away from complete, just for illustration purpose
        data = re.compile(r'parse_asin_\w+\((.*)\);$').search(content).group(1)
        data = json.loads(data)
        
        from pprint import pprint
        print 'title'
        pprint(data['detailJSON']['title'])
        pprint(data['productDescription'])
        p.title = data['detailJSON']['title']
        p.list_info = data['productDescipriton']['bullets'][0]['bulletsList']
        print 
        print 
        print 
        asin = data['detailJSON']['asin']
        p, is_new = Product.objects.get_or_create(pk=asin)
        
        p.title = data['detailJSON']['title']
        p.save()

if __name__ == '__main__':
    #print time2utc({u'offset': -480, u'time': 1352912400000})
    #Server().crawl_category('haha')
    #Server().crawl_product_plus()
    print Server().get_product_abstract_by_url('http://www.myhabit.com/#page=d&dept=men&sale=A25ZXVWLT0BY7D&asin=B009QTU916&cAsin=B009QTUEM0&ref=qd_b_img_d_1')
