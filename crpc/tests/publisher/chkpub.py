from gevent import monkey; monkey.patch_all()
from crawlers.common.routine import get_site_module
from datetime import datetime
from mongoengine import Q

class PubChecker:
    def __init__(self):
        pass
        
    def check_event(self, site):
        m = get_site_module(site)
        if not hasattr(m, 'Event'):
            print "No events available"
            return

        now = datetime.utcnow()

        total = m.Event.objects.count()
        published = m.Event.objects(publish_time__exists=True).count()
        print "total events:", total
        print "unpublished events:", total-published

        noproduct = 0
        for ev in m.Event.objects(publish_time__exists=False):
            if m.Product.objects(event_id=ev.event_id).count()==0: noproduct+=1
        print "unpublished_events that has no product", noproduct

        image_complete = m.Event.objects(image_complete=True).count()
        propagation_incomplete = m.Event.objects(propagation_complete=False).count()
        propagation_incomplete_onshelf = m.Event.objects(Q(propagation_complete=False)&(Q(events_begin__exists=False)|Q(events_begin__lt=now))).count()
        print "image not completed:", total - image_complete
        print "propagation not complete(onshelf/total): {}/{}".format(propagation_incomplete_onshelf, propagation_incomplete)
        
        unpublished_new = m.Event.objects(publish_time__exists=False, events_begin__gt=now).count()
        total_new = m.Event.objects(events_begin__gt=now).count()
        print "unpublished upcoming/total upcoming: {}/{}".format(unpublished_new, total_new)
        
if __name__ == '__main__':
    from optparse import OptionParser
    import sys, os

    parser = OptionParser(usage='usage: %prog [options]')
    # parameters
    parser.add_option('-s', '--site', dest='site', help='site', default='all')
    parser.add_option('--event', dest='event', action="store_true", help='reset crawler database', default=False)
    parser.add_option('--chkdb', dest='chkdb', action="store_true", help='check crawler database', default=False)    

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit()

    options, args = parser.parse_args(sys.argv[1:])
    if not options.site:
        parser.print_help()
        sys.exit()

    if options.site=='all':
        sites = ['beyondtherack', 'bluefly', 'gilt', 'hautelook', 'ideeli', 'myhabit', 'nomorerack', 'onekingslane', 'ruelala', 'venteprivee', 'zulily']
    elif ',' in options.site:
        sites = options.site.split(',')
    else:
        sites = [options.site]
    chk = PubChecker()
    if options.event:
        for site in sites:
            print "Checking events in", site, "........."
            chk.check_event(site)
            print


