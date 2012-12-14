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
        print "total events:", total
        image_incomplete = m.Event.objects(image_complete=False).count()
        print "image not completed:", image_incomplete
        #print "propagation not complete: {}".format(propagation_incomplete)

        published = m.Event.objects(publish_time__exists=True).count()
        unpublished_new = m.Event.objects(publish_time__exists=False, events_begin__gt=now).count()
        total_new = m.Event.objects(events_begin__gt=now).count()
        print "upcoming events(unpublished/total): {}/{}".format(unpublished_new, total_new)
        print

        # analyze on-shelf event
        onshelf = 0; noprod = 0; noreadyprod = 0; nodept = 0; nodept_evid=[]
        for ev in m.Event.objects(Q(events_begin__exists=False) | Q(events_begin__lt=now)):
            onshelf += 1
            if m.Product.objects(event_id=ev.event_id).count()==0:
                noprod += 1
            elif m.Product.objects(event_id=ev.event_id, image_complete=True, dept_complete=True).count()==0:
                noreadyprod += 1
            elif not ev.favbuy_dept:
                nodept += 1
                nodept_evid.append(ev.event_id)
            
        print "on-shelf events:", onshelf
        print "on-shelf and no product events:", noprod
        print "on-shelf and no ready product events:", noreadyprod
        print "on-shelf remaining and no department events:", nodept, "({})".format(nodept_evid)
        print

        # analyze unpublished events
        noprod = 0  # how many events have no product underneath
        noreadyprod = 0  # how many events have no ready products
        notready = 0 # how many events that have ready products but itself is not ready
        unknown = []
        for ev in m.Event.objects(publish_time__exists=False):
            if m.Product.objects(event_id=ev.event_id).count()==0: 
                noprod += 1
            elif m.Product.objects(event_id=ev.event_id, image_complete=True, dept_complete=True).count()==0:
                noreadyprod += 1
            elif not ev.image_complete or not ev.propagation_complete:
                notready += 1
            else:
                unknown.append(ev.event_id)
        print "unpublished events:", total-published
        print "unpublished_events that has no product:", noprod
        print "unpublished_events that has no readyproduct:", noreadyprod
        print "unpublished_events that has ready products but itself not ready:", notready
        print "unpublished (unknow reason) event:", ",".join(unknown)

if __name__ == '__main__':
    from optparse import OptionParser
    import sys, os

    parser = OptionParser(usage='usage: %prog [options]')
    # parameters
    parser.add_option('-s', '--site', dest='site', help='site', default='all')
    parser.add_option('--event', dest='event', action="store_true", help='reset crawler database', default=False)

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


