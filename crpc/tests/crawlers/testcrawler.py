from backends.monitor.models import Task, Schedule, fail
from backends.monitor.events import run_command
from datetime import datetime, timedelta
import sys, gevent
from log import test_error, test_alert, test_info
from mongoengine import Q

class TestCrawlerFixture:
    def __init__(self, crawler):
        self.crawler = crawler
        _temp = __import__('crawlers.%s.models'%(crawler,), globals(), locals(), ['Event', 'Product'], -1)
        globals()["Event"] = _temp.Event
        globals()["Product"] = _temp.Product
        try:
            _temp = __import__('crawlers.%s.models'%(crawler,), globals(), locals(), ['Category'], -1)        
            globals()["Category"] = _temp.Category
            self.has_category = True
        except:
            self.has_category = False
            
    def run_cmd(self, command):
        ts = datetime.utcnow() #-timedelta(seconds=1)
        run_command.send('webui', site=self.crawler, method=command)
        gevent.sleep(1) # add a small delay in case task object has not been created
        task = Task.objects(started_at__gte=ts)[0]
        return task
    
    def run_cmd_complete(self, command):
        '''a complete run of a command till finish and return run stats.
        '''
        tsk = self.run_cmd(command)
        self.wait_task_finish(tsk)
        stats = self.get_run_stats(tsk)
        return stats
        
    def run_status(self, task):
        #t = Task.objects(id=task.id)[0]  # need this reload
        task.reload()
        return task.status 
    
    def get_run_stats(self, task):
        #t = Task.objects(id=task.id)[0]
        task.reload()
        stats = task.num_finish, task.num_update, task.num_new, task.num_fails
        return stats
    
    def wait_task_finish(self, task):
        while self.run_status(task) != 105:
            sys.stdout.write('.'); sys.stdout.flush()
            gevent.sleep(1)
        print

class TestCrawler:
    def __init__(self, crawler):
        self.crawler = crawler
        self.f = TestCrawlerFixture(crawler)
    
    def clear_db(self):
        Event.drop_collection()
        Product.drop_collection()
        
    def check_events(self):
        print "Checking events ..."
        total = Event.objects.count()
        now = datetime.utcnow()
        total_incomplete = Event.objects(Q(urgent=True) & (Q(events_begin__lte=now)|Q(events_begin__exists=False)) & \
                                         (Q(events_end__gt=now)|Q(events_end__exists=False))).count()
        title_missing = Event.objects(Q(urgent=False) & Q(sale_title__exists=False)).count()
        url_missing = Event.objects(Q(urgent=False) & Q(combine_url__exists=False)).count()
        id_missing = Event.objects(Q(urgent=False) & Q(event_id__exists=False)).count()
        image_url_missing = Event.objects(Q(urgent=False) & Q(image_urls__size=0)).count()
        description_missing = Event.objects(Q(urgent=False) & Q(sale_description__exists=False)).count()    
        print "\tTotal events(all/incomplete): {}/{}".format(total,total_incomplete)
        print "\tTitles missing: {}".format(title_missing)
        print "\tURL missing: {}".format(url_missing)
        print "\tImage url missing: {}".format(image_url_missing)
        print "\tDescription missing: {}".format(description_missing)
        if self.f.has_category:
            total_cat = Category.objects.count()
            leaf_cat = Category.objects(is_leaf=True)
            print "Total Category(all/leaf): {}/{}".format(total_cat, leaf_cat)
            
    def check_products(self):
        print "Checking products ..."
        total = Product.objects.count()
        total_incomplete = Product.objects(updated=False).count()
        total_event = Event.objects(urgent=False).count()
        title_missing = Product.objects(Q(updated=True) & Q(title__exists=False)).count()
        url_missing = Product.objects(Q(updated=True) & Q(combine_url__exists=False)).count()
        image_url_missing = Product.objects(Q(updated=True) & Q(image_urls__size=0)).count()
        listinfo_missing = Product.objects(Q(updated=True) & Q(list_info__exists=False)).count()            
        summary_missing = Product.objects(Q(updated=True) & Q(summary__exists=False)).count()
        print "\tTotal/incomplete products: {}/{}".format(total, total_incomplete)
        print "\tAverage product per event: {}".format(total/total_event)
        print "\tTitles missing: {}".format(title_missing)
        print "\tUrl missing: {}".format(url_missing)
        print "\tImage url missing: {}".format(image_url_missing)
        print "\tSummary missing: {}".format(summary_missing)
        print "\tListInfo missing: {}".format(listinfo_missing)        
        
    def check_db(self):
        self.check_events()
        self.check_products()
        
    def test_new_category(self):
        '''Basic test of new_category function. Run it twice in a row, checking the
        run stats with proper values.
        '''
        self.clear_db()
        test_info("running new_category")
        d,u,n,f = self.f.run_cmd_complete("new_category")
        test_info("done=%d,update=%d,new=%d,fail=%d" % (d,u,n,f))
        if u>0:
            test_error("update={0}, should be 0".format(u))
        if d>u+n:
            test_alert("done>update+new, there are unchanged entries?")
        if f>0:
            test_alert("fail={0}, not 0. Please check.".format(f))
        # 2nd pass
        test_info("running 2nd new_category")
        d,u,n,f = self.f.run_cmd_complete("new_category")
        test_info("done=%d,update=%d,new=%d,fail=%d" % (d,u,n,f))
        if u>0:
            test_error("update={0}, should be 0".format(u))
        if n>0:
            test_error("new={0}, should be 0".format(n))
        if f>0:
            test_alert("fail={0}, not 0. Please check.".format(f))
            
    def test_new_funcs(self):
        '''test new functions. Run new_category,new_listing, new_product in a row,
        checking basic stats.
        '''
        self.clear_db()
        test_info("running new_category")
        d,u,n,f = self.f.run_cmd_complete("new_category")
        test_info("done=%d,update=%d,new=%d,fail=%d" % (d,u,n,f))
        
        test_info("running new_listing")
        d2,u2,n2,f2 = self.f.run_cmd_complete("new_listing")
        test_info("done=%d,update=%d,new=%d,fail=%d" % (d2,u2,n2,f2))
        if u2>0:
            test_error("update={0}, should be 0".format(u2))
        if f2>0:
            test_alert("fail={0}, not 0. Please check.".format(f2))
        if d2>u2+n2:
            test_alert("done>update+new, there are overlapped entries?")
        # check why d and u differ by looking into DB $$
        
        test_info("running new_product")
        d3,u3,n3,f3 = self.f.run_cmd_complete("new_product")
        test_info("done=%d,update=%d,new=%d,fail=%d" % (d3,u3,n3,f3))
        if f3>0:
            test_alert("fail={0}, not 0. Please check.".format(f3))
        if d3+f3!=n2:
            test_error("done+fail is not the same as previous new_listing.new.")
        if d3!=u3:
            test_error("done is not the same as update.")
            
        self.check_db()

    def test_new_update_listing(self):
        '''test new_listing and followed by update_listing.
        '''
        self.clear_db()
        test_info("running new_category")
        d,u,n,f = self.f.run_cmd_complete("new_category")
        test_info("done=%d,update=%d,new=%d,fail=%d" % (d,u,n,f))
        
        test_info("running new_listing")
        d2,u2,n2,f2 = self.f.run_cmd_complete("new_listing")
        test_info("done=%d,update=%d,new=%d,fail=%d" % (d2,u2,n2,f2))
        if u2>0:
            test_error("update={0}, should be 0".format(u2))
        if f2>0:
            test_alert("fail={0}, not 0. Please check.".format(f2))
        if d2>u2+n2:
            test_alert("done>update+new, there are unchanged entries?")
        # check why d and u differ by looking into DB $$

        test_info("running update_listing")
        d3,u3,n3,f3 = self.f.run_cmd_complete("update_listing")
        test_info("done=%d,update=%d,new=%d,fail=%d" % (d3,u3,n3,f3))
        if n3>0:
            test_error("new={0}, should be 0".format(u2))
        if d3!=n2:
            test_alert("update_listing.done is not same as previous new_listing.new.".format(f2))

if __name__ == '__main__':
    from optparse import OptionParser
    import sys, os
    
    parser = OptionParser(usage='usage: %prog [options]')
    # parameters
    parser.add_option('-c', '--crawler', dest='crawler', help='crawler', default='')
    parser.add_option('-f', '--function', dest='func', help='function to test', default='test_new_funcs')
    parser.add_option('--clrdb', dest='clrdb', action="store_true", help='reset crawler database', default=False)
    parser.add_option('--chkdb', dest='chkdb', action="store_true", help='check crawler database', default=False)    
        
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit()

    options, args = parser.parse_args(sys.argv[1:])
    if not options.crawler:
        parser.print_help()
        sys.exit()
        
    tc = TestCrawler(options.crawler)
    if options.clrdb:
        tc.clear_db()
    elif options.chkdb:
        tc.check_db()
    elif not options.func:
        tc.test_new_category()
    else:
        try:
            func = getattr(tc, options.func)
            func()
        except Exception, e:
            print "Exception: {}".format(e)

    