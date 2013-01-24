'''
a utility script to restore publish_time in mongodb from the information in mastiff where due to mis-operation
lost such information.
'''
from gevent import monkey; monkey.patch_all()
from mysettings import MASTIFF_ENDPOINT
from crawlers.common.routine import get_site_module
import slumber
import re
from os import listdir
from os.path import join, isdir
from settings import CRPC_ROOT
from crawlers.common.stash import exclude_crawlers
import dateutil.parser

class DupeFixer:
    def __init__(self):
        self.mapi = slumber.API(MASTIFF_ENDPOINT)
        self.m = {}

        for name in listdir(join(CRPC_ROOT, "crawlers")):
            path = join(CRPC_ROOT, "crawlers", name)
            if name not in exclude_crawlers and isdir(path):
                self.m[name] = get_site_module(name)

    def get_module(self, site):
        return self.m[site]
    
    def fix_product(self, site, key, dryrun=False):
        m = self.get_module(site)
        result = self.mapi.product.get(site_key=site+"_"+key)
        for prod in result['objects']:
            try:
                print "id={} updated_at={}, uri={}".format(prod['id'], prod['updated_at'], prod['resource_uri'])
                if dryrun: continue
                prodobj = m.Product.objects.get(key=key)
                prodobj.publish_time = dateutil.parser.parse(prod['updated_at'])
                prodobj.muri = prod['resource_uri']
                prodobj.save()
                print "site:{}, product:{} publish_time restored".format(site, key)
            except Exception as e:
                print "exception:", e
                print "site:{}, product:{} publish_time restore failed".format(site, key)
    
    def fix_event(self, site, key, dryrun=False):
        m = self.get_module(site)
        result = self.mapi.event.get(site_key=site+"_"+key)
        for ev in result['objects']:
            try:
                print "id={} updated_at={}, uri={}".format(ev['id'], ev['updated_at'], ev['resource_uri'])
                evobj = m.Event.objects.get(event_id=key)
                evobj.publish_time = dateutil.parser.parse(ev['updated_at'])
                evobj.muri = ev['resource_uri']
                evobj.save()
                print "site:{}, event:{} publish_time restored".format(site, key)
            except Exception as e:
                print "exception:", e
                print "site:{}, event:{} publish_time restore failed".format(site, key)

    def fix_products_in_file(self, filename):
        pattern = re.compile('publishing product (?P<site>[a-zA-Z0-9_\-]\w+):(?P<key>[a-zA-Z0-9_\-]+) failed')
        with open(filename) as f:
            for line in f:
                m = pattern.search(line)
                if m:
                    self.fix_product(m.group('site'), m.group('key'))

    def fix_events_in_file(self, filename):
        pattern = re.compile('publishing event (?P<site>[a-zA-Z0-9_\-]\w+):(?P<key>[a-zA-Z0-9_\-]+) failed')
        with open(filename) as f:
            for line in f:
                m = pattern.search(line)
                if m:
                    self.fix_event(m.group('site'), m.group('key'))
    
    def fix_events_in_db(self, site):
        print "fixing events in site:", site
        m = self.get_modules(site)
        for ev in m.Event.objects(publish_time__exists=False):
            self.fix_event(site, ev.event_id)
    
    def fix_products_in_db(self, site):
        print "fixing products in site:", site
        m = self.get_modules(site)
        for prod in m.Product.objects(publish_time__exists=False):
            self.product(site, prod.key)
        
    def fix_all_events_in_db(self):
        for site in self.m.keys():
            self.fix_events_in_db(site)
            
    def fix_all_products_in_db(self):
        for site in self.m.keys():
            self.fix_products_in_db(site)
        
if __name__ == '__main__':
    from optparse import OptionParser
    import sys

    parser = OptionParser(usage='usage: %prog [options]')
    # parameters
    parser.add_option('-f', '--file', dest='file', help='file to scan error condition', default='')
    parser.add_option('-s', '--site', dest='site', help='site info', default='')
    parser.add_option('-e', '--ev', dest='ev', help='event id', default='')
    parser.add_option('-p', '--prod', dest='prod', help='product id', default='')
    parser.add_option('-d', '--dryrun', dest='dryrun', action="store_true", help='dryrun', default=False)
    parser.add_option('--db', dest='db', action="store_true", help='scan the database', default=False)
    
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit()

    options, args = parser.parse_args(sys.argv[1:])
    fixer = DupeFixer()
    if options.file:
        fixer.fix_products_in_file(options.file)
        fixer.fix_events_in_file(options.file)
    elif options.site and options.prod:
        fixer.fix_product(options.site, options.prod, options.dryrun)
    elif options.site and options.ev:
        fixer.fix_event(options.site, options.ev, options.dryrun)
    elif options.db:
        if options.site:
            fixer.fix_events_in_db(options.site)
            fixer.fix_products_in_db(options.site)
        else:
            fixer.fix_all_events_in_db()
            fixer.fix_all_products_in_db()
