from crawlers.common.routine import get_site_module
from datetime import datetime

class PubChecker:
    def __init__(self):
        pass
        
    def check_event(self, site):
        m = get_site_module(site)
        total = m.Event.objects.count()
        published = m.Event.objects(publish_time__exists=True).count()
        print "total events:", total
        print "unpublished events:", total-published

        image_complete = m.Event.objects(image_complete=True)
        propagation_complete = m.Event.objects(propagation_complete=True)
        print "image not completed:", total - image_complete
        print "propagation not complete:", total - propagation_complete
        
        now = datetime.utcnow()
        unpublished_new = m.Event.objects(publish_time__exists=False, events_begin>now).count()
        print "unpublished upcoming:", unpublished_new
        
if __name__ == '__main__':
    from optparse import OptionParser
    import sys, os

    parser = OptionParser(usage='usage: %prog [options]')
    # parameters
    parser.add_option('-s', '--site', dest='site', help='site', default='')
    parser.add_option('--event', dest='event', action="store_true", help='reset crawler database', default=False)
    parser.add_option('--chkdb', dest='chkdb', action="store_true", help='check crawler database', default=False)    

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit()

    options, args = parser.parse_args(sys.argv[1:])
    if not options.crawler:
        parser.print_help()
        sys.exit()

    chk = PubChecker()
    if options.event:
        chk.check_event(options.site)
