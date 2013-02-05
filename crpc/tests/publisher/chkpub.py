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
        unpublished_new = m.Event.objects(publish_time__exists=False, events_begin__gt=now)
        noimage_up = 0; nonleaf = 0; unknown_up = 0; unknown_evid = []
        for ev in unpublished_new:
            if not ev.image_path:
                noimage_up += 1
            elif ev.is_leaf==False:
                nonleaf += 1
            else:
                unknown_up += 1;
                if len(unknown_evid)<5: unknown_evid.append(ev.event_id)

        print "upcoming events unpublished:", unpublished_new.count()
        print "uncoming events unpublished, no image:", noimage_up
        print "uncoming events unpublished remaining, nonleaf:", nonleaf
        print "unknown:", unknown_up, "({})".format(",".join(unknown_evid))
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
            elif not ev.image_path:
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

        return [
            ('total_events', total),
            ('image not completed', image_incomplete),

            ('upcoming events', total_new),
            ('upcoming events unpublished', unpublished_new.count()),
            ('upcoming events unpublished, no image', noimage_up),
            ('upcoming events unpublished remaining, nonleaf', nonleaf),
            ('upcoming events unpublished, unknown', unknown_up),

            ('on-shelf events', onshelf),
            ('on-shelf and published events', published),
            ('on-shelf and no product events:', noprod),
            ('on-shelf and no ready product events', noreadyprod,),
            ('on-shelf remaining and no image events', noimage),
            ('on-shelf remaining and no propagation events', noprop),
            ('on-shelf remaining and unknown events', unknown),
        ]
        
    def check_product(self, site):
        m = get_site_module(site)
        total = m.Product.objects.count()
        total_noimage = m.Product.objects(image_path__exists=False).count()
        total_nodept = m.Product.objects(dept_complete=False).count()
        total_nobrand = m.Product.objects(brand_complete=False).count()
        total_notag = m.Product.objects(tag_complete=False).count()        
        print "total:", total
        print "no image:", total_noimage
        print "no department:", total_nodept
        print "no brand:", total_nobrand
        print "no tag:", total_notag
        print
        
        # analyze unpublished
        unpub = 0
        noimage = 0
        nodept = 0
        eventnotready = 0
        unknown = 0; unknown_keys = []
        for p in m.Product.objects(publish_time__exists=False):
            unpub += 1
            if not p.image_path:
                noimage += 1
            elif not p.dept_complete:
                nodept += 1
            elif not [ev for ev in [m.Event.objects.get(event_id=evid) for evid in p.event_id] if ev.publish_time]:
                eventnotready += 1
            else:
                unknown += 1
                if len(unknown_keys)<5: unknown_keys.append(p.key)

        print "unpublished:", unpub
        print "unpublished and image incomplete:", noimage
        print "unpublished remaining and no department:", nodept
        print "unpublished remaining and event not ready:", eventnotready
        print "unpublished remaining and unknown:", unknown, "({})".format(",".join(unknown_keys))
        print

        # analyze published
        pub = 0  # total publised
        standalone = 0  # not assoc with any event
        evpublished = 0  # assoc with events and one of events are published
        evunpublished = 0 # all associated events are not published
        for p in m.Product.objects(publish_time__exists=True):
            pub += 1
            if not p.event_id:
                standalone += 1
            else:
                done = False
                for evid in p.event_id:
                    ev = m.Event.objects.get(event_id=evid)
                    if ev.publish_time:
                        evpublished += 1; done=True; break
                if not done: 
                    evunpublished += 1
        print "published:", pub
        print "published and standalone", standalone
        print "published remaining and has a published event:", evpublished
        print "published remaining and not of its events published:", evunpublished
        print

        return [
            ('total', total),
            ('no image', total_noimage),
            ('no department', total_nodept),
            ('no brand', total_nobrand),
            ('no tag', total_notag),

            ('unpublished', unpub),
            ('unpublished and image incomplete', noimage),
            ('unpublished remaining and no department', nodept),
            ('unpublished remaining and event not ready', eventnotready),
            ('unpublished remaining and unknown', unknown,),

            ('published', pub),
            ('published and standalone', standalone),
            ('published remaining and has a published event', evpublished,),
            ('published remaining and not of its events published', evunpublished),
        ]

        
if __name__ == '__main__':
    from optparse import OptionParser
    import sys, os

    parser = OptionParser(usage='usage: %prog [options]')
    # parameters
    parser.add_option('-s', '--site', dest='site', help='site', default='all')
    parser.add_option('--event', dest='event', action="store_true", help='check event', default=False)
    parser.add_option('--product', dest='prod', action="store_true", help='check product', default=False)
    
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
    elif options.prod:
        for site in sites:
            print "Checking products in", site, "......"
            chk.check_product(site)
            print
            


