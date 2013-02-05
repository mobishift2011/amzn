
from gevent import monkey; monkey.patch_all()
from crawlers.common.events import common_saved
from crawlers.common.routine import get_site_module
from powers.events import image_crawled, ready_for_publish
from backends.monitor.models import Stat
from settings import CRPC_ROOT
from mysettings import MINIMUM_PRODUCTS_READY, MASTIFF_ENDPOINT
from helpers import log
from mongoengine import Q
import slumber
from datetime import datetime, timedelta
import sys
from os import listdir
from os.path import join, isdir
from crawlers.common.stash import exclude_crawlers

class Publisher:
    def __init__(self):
        self.mapi = slumber.API(MASTIFF_ENDPOINT)
        self.logger = log.getlogger("publisher", "/tmp/publisher.log")
        self.m = {}
        
        for name in listdir(join(CRPC_ROOT, "crawlers")):
            path = join(CRPC_ROOT, "crawlers", name)
            if name not in exclude_crawlers and isdir(path):
                self.m[name] = get_site_module(name)
                
    def get_module(self, site):
        return self.m[site]
        
    def try_publish_all(self, site):
        '''publish all events and products in a site that meet publish condition.
        
        :param site: all objects under site will be examined for publishing.
        '''
        self.logger.debug("try_publish_all site:%s", site)
        m = self.get_module(site)

        # try look for both unpublished events and events published but requiring update
        if hasattr(m, 'Event'):
            for ev in m.Event.objects:
                if self.should_publish_event_upd(ev):
                    self.publish_event(ev, upd=True)
                else:   
                    self._try_publish_event(ev, skip_products=True)

        # try look for both unpublished products and products published but requiring update
        for prod in m.Product.objects:
            if self.should_publish_product(prod, chk_ev=True):
                self.publish_product(prod)
            elif self.should_publish_product_upd(prod):
                self.publish_product(prod, upd=True)
        self.logger.debug("try_publish_all completed site:%s", site)
        
    def try_publish_event(self, site, evid):
        '''check if event is ready for publish and if so, publish it.
        Include publishing the contained products if eligible.

        :param site: the site evid is associated with
        :param evid: event id
        '''
        self.logger.debug("try_publish_event %s:%s", site, evid)
        m = self.get_module(site)        
        ev = m.Event.objects.get(event_id=evid)
        self._try_publish_event(ev)
        
    def try_publish_product(self, site, prod_key):
        '''check if product is ready for publish and if so, publish it.
        
        :param site: site of the product.
        :param prod_key: key of the product.
        '''
        self.logger.debug("try_publish_product %s:%s", site, prod_key)
        m = self.get_module(site)
        prod = m.Product.objects.get(key=prod_key)
        if self.should_publish_product(prod):
            # event may become eligible, too, as event publish is
            # conditioned on the number of products ready
            for ev in self.ready_events(prod):
                self._try_publish_event(ev)
            # current product may not get published in the above, as it may not be associated
            # with any events
            prod.reload()  # db content modified in the above step
            if self.should_publish_product(prod, chk_ev=True):
                self.publish_product(prod)
        else:
            self.logger.debug("product {}:{} not ready for publishing".format(obj_to_site(prod),prod_key))
                            
    def try_publish_event_update(self, site, evid):
        '''try publishing an event update only (not first publish)
        
        :param site: site of the event
        :param evid: event id
        :param fields: fields that need to be updated.
        '''
        self.logger.debug("try_publish_event_update %s:%s", site, evid)
        m = self.get_module(site)
        ev = m.Event.objects.get(event_id=evid)
        if self.should_publish_event_upd(ev):
            self.publish_event(ev, upd=True)
        else:
            self.logger.debug("event {}:{} not ready for publishing".format(obj_to_site(ev), evid))
            
    def try_publish_product_update(self, site, prod_key):
        '''try publishing a product update only (not first publish)

        :param site: site string
        :param prod_key: product key
        '''
        self.logger.debug("try_publish_product_update %s:%s", site, prod_key)
        m = self.get_module(site)
        prod = m.Product.objects.get(key=prod_key)
        if self.should_publish_product_upd(prod):
            self.publish_product(prod, upd=True)
        else:
            self.logger.debug("product %s:%s not ready for publishing", obj_to_site(prod),prod_key)
            
    def _try_publish_event(self, ev, skip_products=False):
        '''
        Check if the event meets publish condition and if so, publish it. Note we take care of
        events that were published before but were happening in future, in which case we need
        to publish additional information of the event such as department, soldout info, etc..
        We then publish all containing products under the events that are ready for publish.

        :param ev: event object
        :param skip_products: if False, also publish all the products contained in the event
        '''
        m = obj_to_module(ev)
        if self.should_publish_event(ev):
            self.publish_event(ev)
            if not ev.publish_time: return # publishing failure
            # republish published products that are associated with the newly published event (event URI field
            # needs to be updated)
            for prod in m.Product.objects(publish_time__exists=True, event_id=ev.event_id):
                self.publish_product(prod, upd=True, fields=['events'])
        elif self.should_publish_event_newly_onshelf(ev):
            self.publish_event(ev, upd=True)
        elif ev.publish_time:
            self.logger.debug("event %s:%s already published", obj_to_site(ev), ev.event_id)
        else:
            self.logger.debug("event %s:%s not ready for publish", obj_to_site(ev), ev.event_id)
            return # we know event is not ready, therefore no need to continue to next step

        if skip_products:
            return
        # it's a full publish, so we need to publish all contained yet unpublished products
        for prod in m.Product.objects(publish_time__exists=False, event_id=ev.event_id):
            if self.should_publish_product(prod):
                self.publish_product(prod)

    def ready_events(self, prod):
        '''return all events the prod is associated with that are ready for publishing.
        
        :param prod: product object        
        '''
        m = obj_to_module(prod)
        events = [m.Event.objects.get(event_id=evid) for evid in prod.event_id]
        return [ev for ev in events if self.should_publish_event(ev)]
        
    def ready_standalone_products(self, m):
        '''returns a list of all ready-to-publish standalone (no events associated with) products.
        :param m: module that contains the products.
        '''
        # $$ include non-obsolete and not out-of-stock condition?
        return m.Product.objects(publish_time__exists=False, event_type=False, image_complete=True, dept_complete=True)
                    
    def should_publish_event(self, ev):
        '''condition for publishing the event for first time.
        
        :param ev: event object        
        '''
        now = datetime.utcnow()
        # for future events, don't publish non-leaf ones
        return not ev.publish_time and ev.image_complete and ev.image_path and \
                (ev.events_begin and ev.events_begin>now and ev.is_leaf != False or ev.propagation_complete \
                 and self.sufficient_products_ready_publish(ev, MINIMUM_PRODUCTS_READY))
    
    def should_publish_event_upd(self, ev):
        '''condition for publishing event update. (event was published before)
        
        :param ev: event object
        '''
        update_time = max(ev.update_history.values()) if ev.update_history else None
        return ev.publish_time and update_time and ev.publish_time < update_time
        
    def should_publish_event_newly_onshelf(self, ev):
        '''all events that were future events and published before but recently became on-shelf and 
        finished propagation'''
        now = datetime.utcnow()
        return ev.publish_time and ev.events_begin and ev.publish_time<ev.events_begin and\
                ev.events_begin<=now and ev.image_complete and ev.propagation_complete
        
    def sufficient_products_ready_publish(self, ev, threshold):
        '''is number of products ready for publish no less than threshold?

        :param ev: event object
        :param threshold: threshold for the number of products ready for publishing
        '''
        m = obj_to_module(ev)

        # there could be many products published already, due to they are associated to both this event
        # and other published events. So we need to perform first check on published products.
        n = m.Product.objects(publish_time__exists=True, event_id=ev.event_id).count()
        if n>threshold: return True

        for prod in m.Product.objects(publish_time__exists=False, event_id=ev.event_id):
            if self.should_publish_product(prod): n += 1
            if n>threshold: return True
        
        self.logger.debug("insufficient products ready (%d) for publish under event %s:%s", n, obj_to_site(ev), ev.event_id)
        return False
        
    def should_publish_product(self, prod, chk_ev=False):
        '''
        is product ready for first-time publishing?
        
        :param chk_ev: indicates if event-level checking is included in the condition or now.
        '''
        if chk_ev and prod.event_id:
            allow_publish = False
            m = obj_to_module(prod)
            for ev in [m.Event.objects.get(event_id=evid) for evid in prod.event_id]:
                if ev.publish_time:
                    allow_publish = True
                    break
            if not allow_publish:
                return False
        return not prod.publish_time and prod.image_complete and prod.image_path and prod.dept_complete

    def should_publish_product_upd(self, prod):
        '''condition for publishing product update (the product was published before).
        :param prod: product object. Note: now only handle favbuy text update.
        '''
        update_time = max(prod.update_history.values()) if prod.update_history else None
        return prod.publish_time and update_time and prod.publish_time < update_time
        
    def ev_updflds_for_publish(self, ev):
        return [fld for fld in ev.update_history.keys() if ev.update_history[fld]>ev.publish_time] if ev.update_history else []
        
    def prod_updflds_for_publish(self, prod):
        return [fld for fld in prod.update_history.keys() if prod.update_history[fld]>prod.publish_time] if prod.update_history else []
        
    ALL_EVENT_PUBLISH_FIELDS = ["sale_title", "sale_description", "events_end", "events_begin",
                                "image_path", "highest_discount", "favbuy_tag", "favbuy_brand", "favbuy_dept"]
    def publish_event(self, ev, upd=False, fields=[]):
        '''publish event data to the mastiff service.
        
        :param ev: event object.
        :param upd: update only. (if False it's a full publish.)
        :param mode: update mode. "soldout": only soldout info needs to be published;
            "onshelf": event is recently put on shelf, therefore multiple fields such as soldout, dept
            need to be published.
        '''
        try:
            m = obj_to_module(ev)
            site = obj_to_site(ev)
            if not upd:
                fields = self.ALL_EVENT_PUBLISH_FIELDS
            elif not fields:
                fields = self.ev_updflds_for_publish(ev)

            ev_data = {}
            for f in fields:
                if f=="sale_title": ev_data['title'] = obj_getattr(ev, 'sale_title', '')
                elif f=="sale_description": ev_data['description'] = obj_getattr(ev, 'sale_description', '')
                elif f=="events_end": ev_data['ends_at'] = obj_getattr(ev, 'events_end', datetime.utcnow()+timedelta(days=7)).isoformat()
                elif f=="events_begin": ev_data['starts_at'] = obj_getattr(ev, 'events_begin', datetime.utcnow()).isoformat()
                elif f=="image_path": ev_data['cover_image'] = ev['image_path'][0] if ev['image_path'] else {}
                elif f=="highest_discount": 
                    try:
                        ev_data['highest_discount'] = ev['highest_discount'][:ev['highest_discount'].find('.')+3]
                    except:
                        pass
                elif f=="soldout": ev_data['sold_out'] = m.Product.objects(event_id=ev.event_id, soldout=False).count()==0
                elif f=="favbuy_tag": ev_data['tags'] = ev.favbuy_tag
                elif f=="favbuy_brand": ev_data['brands'] = ev.favbuy_brand
                elif f=="favbuy_dept": ev_data['departments'] = ev.favbuy_dept
            if not upd:
                ev_data['site_key'] = site+'_'+ev.event_id
            if upd and not ev_data: return         
            self.logger.debug("publish event data: %s", ev_data)

            if upd:
                self.mapi.event(muri2mid(ev.muri)).patch(ev_data)
                self.logger.debug("published event update %s:%s, fields=%s", site, ev.event_id, fields)
            else:
                ev_resource = self.mapi.event.post(ev_data)
                ev.muri = ev_resource['resource_uri']; 
                self.logger.debug("published event %s:%s, resource_id=%s", site, ev.event_id, ev_resource['id'])
            
                # For monitoring publish flow stat
                interval = datetime.utcnow().replace(second=0, microsecond=0)
                Stat.objects(site=site, doctype='event', interval=interval).update(inc__publish_num=1, upsert=True)

            ev.publish_time = datetime.utcnow(); ev.save()
        except Exception as e:
            self.logger.error(e)
            self.logger.error("publishing event %s:%s failed", obj_to_site(ev), ev.event_id)
    
    ALL_PRODUCT_PUBLISH_FIELDS = ["favbuy_url", "events", "favbuy_price", "favbuy_listprice", "soldout",
                                "color", "title", "summary", "list_info", "image_path", "favbuy_tag", "favbuy_brand", "favbuy_dept",
                                "returned", "shipping", "products_begin", "products_end" ]
    def publish_product(self, prod, upd=False, fields=[]):
        '''
        Publish product data to the mastiff service.

        :param prod: product object.
        :param upd: update only. (if False, then it'll be a full publish.)
        '''
        try:
            site = obj_to_site(prod)
            if not upd:
                fields = self.ALL_PRODUCT_PUBLISH_FIELDS
            elif not fields:
                fields = self.prod_updflds_for_publish(prod)

            pdata = {}
            for f in fields:
                if f=="favbuy_url": pdata["original_url"] = prod.favbuy_url if prod.url_complete else prod.combine_url
                elif f=="events": pdata["events"] = self.get_ev_uris(prod)
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
            if not upd:
                pdata["site_key"] = site+'_'+prod.key
            if upd and not pdata: return
            self.logger.debug("publish product data: %s", pdata)

            if upd:
                self.mapi.product(muri2mid(prod.muri)).patch(pdata)
                self.logger.debug("published product update %s:%s", site, prod.key)
            else:
                r = self.mapi.product.post(pdata)
                prod.muri = r['resource_uri']; 
                self.logger.debug("published product %s:%s, resource_id=%s", site, prod.key, r['id'])
                
                # For monitoring publish flow stat
                interval = datetime.utcnow().replace(second=0, microsecond=0)
                Stat.objects(site=site, doctype='product', interval=interval).update(inc__publish_num=1, upsert=True)
            
            prod.publish_time = datetime.utcnow(); prod.save()
            
        except Exception as e:
            self.logger.error(e)
            self.logger.error("publishing product %s:%s failed", obj_to_site(prod), prod.key)
            
    def mget_event(self, site, evid):
        '''get event data back from mastiff service.
        '''
        m = self.get_module(site)
        try:
            ev = m.Event.objects.get(event_id=evid)
            if not ev.muri:
                self.logger.error("event %s:%s has not been published before", site, evid)
            else:
                return self.mapi.event(muri2mid(ev.muri)).get()
        except Exception as e:
            self.logger.error(e)
            
    def mget_product(self, site, prod_key):
        '''get product data back from mastiff service.
        '''
        m = self.get_module(site)
        try:
            p = m.Product.objects.get(key=prod_key)
            if not p.muri:
                self.logger.error("product %s:%s has not been published before", site, prod_key)
            else:
                return self.mapi.product(muri2mid(p.muri)).get()
        except Exception as e:
            self.logger.error(e)
            
    def get_ev_uris(self, prod):
        '''return a list of Mastiff URLs corresponding to the events associated with the product.
        '''
        m = obj_to_module(prod)
        return [ev.muri for ev in [m.Event.objects.get(event_id=evid) for evid in prod.event_id] if ev.muri]
        
p = Publisher()

def sender_to_site(sender):
    '''extract site info from signal sender.
    '''
    return sender.split(".")[0]

def obj_to_site(obj):
    '''obj is either an event object or product object.
    '''
    return obj.__module__.split('.')[1]  # 'crawlers.gilt.models'
    
def obj_to_module(obj):
    '''find the corresponding Python module associated with the object.
    '''
    return sys.modules[obj.__module__]
    
def obj_getattr(obj, attr, defval):
    '''get attribute value associated with an object. If not found, return a default value.
    '''
    if not hasattr(obj, attr):
        return defval
    else:
        val = getattr(obj, attr)
        return val if val else defval
        
def muri2mid(muri):
    '''extract mastiff resource ID from mastiff URI.
    '''
    return muri.split("/")[-2]
    
@common_saved.bind('globalsync')
def process_common_saved(sender, **kwargs):
    '''signa handler for common_saved. Currently common_saved
    signal is only useful in publisher to monitor soldout updates.
    '''
    is_update = kwargs.get('is_updated')
    if not is_update:
        return # obj is not ready for publishing
    
    site = sender_to_site(sender)
    obj_type = kwargs.get('obj_type')
    key = kwargs.get('key')
    
    if obj_type == 'Product':
        p.try_publish_product_update(site, key)
    elif obj_type == 'Event':
        p.try_publish_event_update(site, key)
        
@image_crawled.bind('globalsync')
def process_image_crawled(sender, **kwargs):
    '''signal handler for image_crawled.
    '''
    site = sender_to_site(sender)
    obj_type = kwargs.get('model')
    key = kwargs.get('key')
    if obj_type == 'Event':
        p.try_publish_event(site, key)
    elif obj_type == 'Product':
        p.try_publish_product(site, key)
    
@ready_for_publish.bind('globalsync')
def process_propagation_done(sender, **kwargs):
    '''signal handler for ready_for_publish. This triggers the publishing of all events
    and products should the publishing conditions for these events and products are met.
    '''
    site = kwargs.get('site', None)
    if not site:
        return
    p.try_publish_all(site)

def dump_obj_in_db(obj):
    for attr in dir(obj):
        if attr.startswith("_"): continue
        print attr, "======>", getattr(obj, attr)

if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser(usage='usage: %prog [options]')
    # parameters
    parser.add_option('-c', '--cmd', dest='cmd', help='command of the signal(update, initial, all)', default='')
    parser.add_option('--mput', dest='mput', action="store_true", help='publish to mastiff service', default=False)
    parser.add_option('--upd', dest='upd', action="store_true", help='update mode(mput only)', default=False)
    parser.add_option('--mget', dest='mget', action="store_true", help='get published result back from mastiff service', default=False)
    parser.add_option('--dbget', dest='dbget', action="store_true", help='get data from db', default=False)    
    parser.add_option('-s', '--site', dest='site', help='site info', default='')
    parser.add_option('-e', '--ev', dest='ev', help='event id', default='')
    parser.add_option('-p', '--prod', dest='prod', help='product id', default='')
    parser.add_option('-f', '--flds', dest='flds', help='fields', default='')
    parser.add_option('-d', '--daemon', dest='daemon', action="store_true", help='daemon mode(no other parameters)', default=False)
    
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit()

    options, args = parser.parse_args(sys.argv[1:])

    if options.daemon:
        import gevent
        while True:
            gevent.sleep(5)

    elif options.cmd == "update":
        if options.site and options.ev:
            p.try_publish_event_update(options.site, options.ev)
        elif options.site and options.prod:
            p.try_publish_product_update(options.site, options.prod)
    elif options.cmd == "initial":
        if options.site and options.ev:
            p.try_publish_event(options.site, options.ev)
        elif options.site and options.prod:
            p.try_publish_product(options.site, options.prod)
    elif options.cmd == "all" and options.site:
        p.try_publish_all(options.site)
        
    elif options.mput:
        if options.site and options.ev:
            m = get_site_module(options.site)
            if options.ev == 'all':
                if not options.upd:
                    print "operation not supported"
                    sys.exit()
                evs = m.Event.objects(publish_time__exists=True)
            else:
                evs = [m.Event.objects.get(event_id=options.ev)]
            for ev in evs:
                if not options.upd:
                    p.publish_event(ev)
                else:
                    p.publish_event(ev, upd=True, fields=options.flds.split(','))
        elif options.site and options.prod:
            m = get_site_module(options.site)
            if options.prod == 'all':
                if not options.upd:
                    print "operation not supported"
                    sys.exit()
                prods = m.Product.objects(publish_time__exists=True)
            else:
                prods = [m.Product.objects.get(key=options.prod)]
            for prod in prods:
                if not options.upd:
                    p.publish_product(prod)
                else:
                    p.publish_product(prod, upd=True, fields=options.flds.split(','))

    elif options.mget:
        from pprint import pprint
        if options.site and options.ev:
            pprint(p.mget_event(options.site, options.ev))
        elif options.site and options.prod:
            pprint(p.mget_product(options.site, options.prod))
    elif options.dbget:
        if options.site and options.ev:
            m = get_site_module(options.site)
            ev = m.Event.objects.get(event_id=options.ev)
            dump_obj_in_db(ev)
        elif options.site and options.prod:
            m = get_site_module(options.site)        
            prod = m.Product.objects.get(key=options.prod)
            dump_obj_in_db(prod)
    else:
        parser.print_help()

