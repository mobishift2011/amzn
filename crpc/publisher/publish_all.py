#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import sys
import slumber
import traceback
import os
from os import listdir
from os.path import join, isdir
from datetime import datetime, timedelta

from crawlers.common.routine import get_site_module
from crawlers.common.stash import exclude_crawlers
from settings import MASTIFF_HOST, MONGODB_HOST, CRPC_ROOT


class Publisher:
    ALL_EVENT_PUBLISH_FIELDS = ["sale_title", "sale_description", "events_end", "events_begin",
                                "image_path", "highest_discount", "favbuy_tag", "favbuy_brand", "favbuy_dept"]

    ALL_PRODUCT_PUBLISH_FIELDS = ["combine_url", "events", "favbuy_price", "favbuy_listprice", "soldout",
                                "color", "title", "summary", "list_info", "image_path", "favbuy_tag", "favbuy_brand", "favbuy_dept",
                                "returned", "shipping", "products_begin", "products_end", "second_hand" ]
    def __init__(self):
        self.mapi = slumber.API(MASTIFF_HOST)
        self.m = {}

        for name in listdir(join(CRPC_ROOT, "crawlers")):
            path = join(CRPC_ROOT, "crawlers", name)
            if name not in exclude_crawlers and isdir(path):
                self.m[name] = get_site_module(name)

    def get_module(self, site):
        return self.m[site]


    def get_ev_uris(self, prod):
        '''return a list of Mastiff URLs corresponding to the events associated with the product.
        '''
        m = obj_to_module(prod)
        ret = []

        for evid in prod.event_id:
            evs = m.Event.objects(event_id=evid)
            if evs:
                for ev in evs:
                    if ev.muri:
                        ret.append( ev.muri )
        return ret
           

    def publish_event(self, ev, fields=[]):
        '''publish event data to the mastiff service.
        
        :param ev: event object.
        :param mode: update mode. "soldout": only soldout info needs to be published;
            "onshelf": event is recently put on shelf, therefore multiple fields such as soldout, dept
            need to be published.
        '''
        m = obj_to_module(ev)
        site = obj_to_site(ev)
        fields = self.ALL_EVENT_PUBLISH_FIELDS

        ev_data = {}
        for f in fields:
            if f=="sale_title": ev_data['title'] = obj_getattr(ev, 'sale_title', '')
            elif f=="sale_description": ev_data['description'] = obj_getattr(ev, 'sale_description', '')
            elif f=="events_end":
                ret = obj_getattr(ev, 'events_end', '')
                if ret: ev_data['ends_at'] = ret.isoformat()
                else: ev_data['ends_at'] = ret
            elif f=="events_begin": ev_data['starts_at'] = obj_getattr(ev, 'events_begin', datetime.utcnow()).isoformat()
            elif f=="image_path": ev_data['cover_image'] = ev['image_path'][0] if ev['image_path'] else {}
            elif f=="highest_discount": 
                try:
                    ev_data['highest_discount'] = ev['highest_discount'][:ev['highest_discount'].find('.')+3] if ev['highest_discount'] else None
                except:
                    print traceback.format_exc()
            elif f=="soldout": ev_data['sold_out'] = m.Product.objects(event_id=ev.event_id, soldout=False).count()==0
            elif f=="favbuy_tag": ev_data['tags'] = ev.favbuy_tag
            elif f=="favbuy_brand": ev_data['brands'] = ev.favbuy_brand
            elif f=="favbuy_dept": ev_data['departments'] = ev.favbuy_dept
        ev_data['site_key'] = site+'_'+ev.event_id
        if not ev_data: return         

        ev_resource = self.mapi.event.post(ev_data)
        ev.muri = ev_resource['resource_uri']; 
        ev.publish_time = datetime.utcnow()
        ev.save()

    def publish_product(self, prod, fields=[]):
        '''
        Publish product data to the mastiff service.

        :param prod: product object.
        '''
        site = obj_to_site(prod)
        fields = self.ALL_PRODUCT_PUBLISH_FIELDS

        pdata = {}
        for f in fields:
            # if f=="favbuy_url": pdata["original_url"] = prod.favbuy_url if prod.url_complete else prod.combine_url
            if f=="combine_url": pdata["original_url"] = prod.combine_url
            elif f=="events":
                ret = self.get_ev_uris(prod)
                if not ret: continue
                pdata["events"] = ret
            elif f=="favbuy_price": pdata["our_price"] = float(obj_getattr(prod, 'favbuy_price', 0))
            elif f=="favbuy_listprice": pdata["list_price"] = float(obj_getattr(prod, 'favbuy_listprice', 0))
            elif f=="soldout": pdata["sold_out"] = prod.soldout
            elif f=="color": pdata["colors"] = [prod['color']] if 'color' in prod and prod['color'] else []
            elif f=="title": pdata["title"] = prod.title
            elif f=="summary": pdata["info"] = prod.summary
            elif f=="list_info": pdata["details"] = obj_getattr(prod, 'list_info', [])
            elif f=="image_path": 
                pdata["cover_image"] = prod.image_path[0] if prod.image_path else {}
                pdata["images"] = obj_getattr(prod, 'image_path', [])
            elif f=="favbuy_brand": pdata["brand"] = obj_getattr(prod, 'favbuy_brand','')
            elif f=='favbuy_tag': pdata["tags"] = obj_getattr(prod, 'favbuy_tag', [])
            elif f=='favbuy_dept': pdata["department_path"] = obj_getattr(prod, 'favbuy_dept', [])
            elif f=="returned": pdata["return_policy"] = obj_getattr(prod, 'returned', '')
            elif f=="shipping": pdata["shipping_policy"] = obj_getattr(prod, 'shipping', '')
            elif f=="products_begin": 
                pb = obj_getattr(prod, 'products_begin', None)
                if pb: pdata["starts_at"] = pb.isoformat()
            elif f=="products_end": 
                pe = obj_getattr(prod, 'products_end', None)
                if pe: pdata["ends_at"] = pe.isoformat()
            elif f == 'second_hand':
                pdata['second_hand'] = obj_getattr(prod, 'second_hand', False)
        pdata["site_key"] = site+'_'+prod.key
        if not pdata: return

        r = self.mapi.product.post(pdata)
        prod.muri = r['resource_uri']; 
            
        prod.publish_time = datetime.utcnow()
        prod.save()


def obj_to_module(obj):
    '''find the corresponding Python module associated with the object.
    '''
    return sys.modules[obj.__module__]

def obj_to_site(obj):
    '''obj is either an event object or product object.
    '''
    return obj.__module__.split('.')[1]  # 'crawlers.gilt.models'

def obj_getattr(obj, attr, defval):
    '''get attribute value associated with an object. If not found, return a default value.
    '''
    if not hasattr(obj, attr):
        return defval
    else:
        val = getattr(obj, attr)
        return val if val else defval

if __name__ == '__main__':
    import pymongo
    from sh import ssh, rsync
    from crawlers.common.stash import picked_crawlers
    ssh("root@crpc.favbuy.org", "rm -rf /tmp/dumpp; mongodump -o /tmp/dumpp/")
    ssh("root@crpc.favbuy.org", "rm -rf /tmp/dumpp")
    for site in picked_crawlers:
        ssh("root@crpc.favbuy.org", "mongodump -d {0} -o /tmp/dumpp/".format(site))

    os.system("rm -rf /tmp/dumpp/")
    rsync("-avze", "ssh", "root@crpc.favbuy.org:/tmp/dumpp/", "/tmp/dumpp/")
    os.system("mongorestore --drop /tmp/dumpp")
    print 'dump crawler db ok.'

    conn = pymongo.MongoClient(MONGODB_HOST)
    dbs = conn.database_names()
    for crawler in picked_crawlers:
        col = conn[crawler].collection_names()
        if 'event' in col:
            conn[crawler].event.remove({'create_time': {'$lt': datetime.utcnow() - timedelta(days=30)}})
        conn[crawler].product.remove({'create_time': {'$lt': datetime.utcnow() - timedelta(days=30)}})

        ll = []
        for pr in conn[crawler].product.find({}, {'event_id': 1}):
            for evid in pr['event_id']:
                if conn[crawler].event.find({'event_id': evid}).count() == 0:
                    ll.append(pr)
        for pr in ll:
            conn[crawler].product.remove(pr)

    print 'delete old data'

    monhost = MASTIFF_HOST.split('//')[-1].split(':')[0]
    client = pymongo.MongoClient(monhost)
    client.mastiff.event.drop()
    client.mastiff.product.drop()
    os.system("curl -XDELETE http://{0}:9200/mastiff".format(monhost))
    print 'delete mastiff data'

    p = Publisher()
    for site in picked_crawlers:
        m = p.get_module(site)
        if hasattr(m, 'Event'):
            for ev in m.Event.objects:
                p.publish_event(ev)
        for prd in m.Product.objects:
            p.publish_product(prd)
    print 'publish mastiff data ok'
