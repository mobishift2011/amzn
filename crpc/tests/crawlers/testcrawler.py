from backends.monitor.models import Task, Schedule, fail
from backends.monitor.events import run_command
from datetime import datetime, timedelta
import sys, gevent
from log import test_error, test_alert, test_info

class TestCrawlerFixture:
    def __init__(self, crawler):
        self.crawler = crawler
        _temp = __import__('crawlers.%s.models'%(crawler,), globals(), locals(), ['Event', 'Product'], -1)
        globals()["Event"] = _temp.Event
        globals()["Product"] = _temp.Product
        
    def clear_db(self):
        Event.drop_collection()
        Product.drop_collection()
        
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
        
    def test_new_category(self):
        '''Basic test of new_category function. Run it twice in a row, checking the
        run stats with proper values.
        '''
        self.f.clear_db()
        test_info("running new_category")
        d,u,n,f = self.f.run_cmd_complete("new_category")
        test_info("done=%d,update=%d,new=%d,fail=%d" % (d,u,n,f))
        if u>0:
            test_error("update={0}, should be 0".format(u))
        if d>u+n:
            test_alert("done>update+new, there are unchanged entries")
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

        self.f.clear_db()
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
        # check why d and u differ by looking into DB $$
        
        test_info("running new_product")
        d3,u3,n3,f3 = self.f.run_cmd_complete("new_product")
        test_info("done=%d,update=%d,new=%d,fail=%d" % (d3,u3,n3,f3))
        if d3!=n2:
            test_error("update is not the same of new of previous new_listing.")
        if d3!=u3:
            test_error("done is not the same as update.")

if __name__ == '__main__':
    from optparse import OptionParser
    import sys, os
    
    parser = OptionParser(usage='usage: %prog [options]')
    # parameters
    parser.add_option('-c', '--crawler', dest='crawler', help='crawler', default='')
    parser.add_option('-f', '--function', dest='func', help='function to test', default='')    
    
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit()

    options, args = parser.parse_args(sys.argv[1:])
    if not options.crawler:
        parser.print_help()
        sys.exit()
        
    tc = TestCrawler(options.crawler)    
    if not options.func:
        tc.test_new_category()
    else:
        try:
            func = getattr(tc, options.func)
            func()
        except:
            print "no such function {}".format(options.func)
            
            
    
    