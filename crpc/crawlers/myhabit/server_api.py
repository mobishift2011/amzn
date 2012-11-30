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
    return datetime.utcfromtimestamp(t['time']//1000)
   

class Server(object):
    def __init__(self):
        self.rooturl = 'http://www.myhabit.com/request/getAllPrivateSales'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Cookie': 'session-id=178-9157968-0478701; session-id-time=19807407421; session-token="f+qT7qj0v+IRz8TvLgLWRc3HRcHcVop9FOmKAt3sgEsUe3lJYBuJIGNobc0VJ0i6vpx1yDcadTg3NHVIzIRJBg7jbM1bOtMEx/y0sBGApDYzmsULdEyGAGT67NZkm9DX8XlrJnPlhQ/Fagv8mq+PD74d1kBfubeOzN/XDCWzeUkobmdlBDSH4WSoeC07sd3iJbZF7i61SjG9k3DxC29q0+tGNgXskOAYFBDvI+jBcFQ="; ct-main="gx?vzAAVNmUyzY55jaGNtIIb?wiE@M1P"; ubid-main=188-4772784-7788317',
            'x-amzn-auth': '178-9157968-0478701',
        }

    def crawl_category(self, ctx=''):
        r = requests.get(self.rooturl, headers=self.headers)
        data = json.loads(r.text)

        for event_data in data['sales']:
            self._parse_event(event_data, ctx)

            # for each event, crawl all the products below
#            for product, detail in event_data.get('asins', {}).items():
#                product_url = event_data['prefix'] + detail['url']
#                Product.objects(key=product).update(set__jslink=product_url, set__asin=product, updated=False, upsert=True)

    def _parse_event(self, event_data, ctx):
        """.. :py:method::
        """
        event_id = event_data['id']
        info = event_data['saleProps']

        is_new, is_updated = False, False
        event = Event.objects(event_id=event_id).first()
        if not event:
            is_new = True
            event = Event(event_id=event_id)
            event.urgent = True
            event.combine_url = 'http://www.myhabit.com/homepage#page=b&sale={0}'.format(event_id)
            event.sale_title = info['primary']['title']
            event.sale_description = info['primary']['desc']
            event.image_urls = [ info['prefix']+val for key, val in info['primary']['imgs'].items() if key == 'hero']
            if 'brandUrl' in info['primary']:
                event.brand_link = info['primary']['brandUrl']

        # updating fields
        event.events_begin = time2utc(event_data['start'])
        event.events_end = time2utc(event_data['end'])
        [event.dept.append(dept) for dept in event_data['departments'] if dept not in event.dept]
        event.soldout = True if 'soldOut' in event_data and event_data['soldOut'] == 1 else False
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)


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
    Server().crawl_category('haha')
    #Server().crawl_product_plus()
    #print Server().get_product_abstract_by_url('http://www.myhabit.com/#page=d&dept=men&sale=A25ZXVWLT0BY7D&asin=B009QTU916&cAsin=B009QTUEM0&ref=qd_b_img_d_1')
