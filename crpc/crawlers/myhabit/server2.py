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

        pool = gevent.pool.Pool(30)

        for event in data['sales']:
            self._parse_event(event, ctx)

            # for each event, crawl all the products below
            for product, detail in event.get('asins', {}).items():
                product_url = event['prefix'] + detail['url']
                pool.spawn(self._parse_product, requests.get(product_url).text, ctx)

        pool.join()

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
        
        asin = data['detailJSON']['asin']
        p, is_new = Product.objects.get_or_create(pk=asin)
        
        p.title = data['detailJSON']['title']
        p.save()

if __name__ == '__main__':
    #print time2utc({u'offset': -480, u'time': 1352912400000})
    Server().crawl_category('haha')
