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
        print
        
        # upcoming events
        total_new = m.Event.objects(events_begin__gt=now).count()
        print "upcoming events:", total_new
        published = m.Event.objects(publish_time__exists=True).count()
        unpublished_new = m.Event.objects(publish_time__exists=False, events_begin__gt=now).count()
        print "upcoming events unpublished:", unpublished_new
        print

        # analyze on-shelf event
        onshelf = 0  # on-shelf events
        published= 0  # published
        noprod = 0   # no product underneath
        noreadyprod = 0  # no ready-product underneath
        notready = 0   # itself not ready
        noimage = 0   # no image
        noprop = 0; noprop_evid=[]  # propagation incomplete
        unknown = 0; unknown_evid = []
        for ev in m.Event.objects(Q(events_begin__exists=False) | Q(events_begin__lt=now)):
            onshelf += 1
            if ev.publish_time:
                published += 1
            elif m.Product.objects(event_id=ev.event_id).count()==0:
                noprod += 1
            elif m.Product.objects(event_id=ev.event_id, image_complete=True, dept_complete=True).count()==0:
                noreadyprod += 1
            elif not ev.image_complete:
                noimage +=1 
            elif not ev.propagation_complete:
                noprop += 1
                noprop_evid.append(ev.event_id)
            else:
                unknown += 1
                unknown_evid.append(ev.event_id)
        print "on-shelf events:", onshelf
        print "on-shelf and published events:", published
        print "on-shelf and no product events:", noprod
        print "on-shelf and no ready product events:", noreadyprod
        print "on-shelf remaining and no image events:", noimage
        print "on-shelf remaining and no propagation events:", noprop, "({})".format(",".join(noprop_evid))
        print "on-shelf remaining and unknown events:", unknown, "({})".format(",".join(unknown_evid))

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


