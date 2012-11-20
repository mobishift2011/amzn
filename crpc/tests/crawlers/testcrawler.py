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
        '''test new_category function'''
        self.f.clear_db()
        test_info("running new_category")
        task = self.f.run_cmd("new_category")
        status = self.f.wait_task_finish(task)
        t,u,n,f = self.f.get_run_stats(task)
        test_info("total=%d,update=%d,new=%d,fail=%d" % (t,u,n,f))
        if u>0:
            test_error("update={0}, should be 0".format(u))
        if t>u+n+f:
            test_alert("total>update+new+fail, there are unchanged entries")
        if f>0:
            test_alert("fail={0}, not 0. Please check.".format(f))
        # 2nd pass
        test_info("running 2nd new_category")
        task = self.f.run_cmd("new_category")
        status = self.f.wait_task_finish(task)
        t,u,n,f = self.f.get_run_stats(task)
        test_info("total=%d,update=%d,new=%d,fail=%d" % (t,u,n,f))
        if u>0:
            test_error("update={0}, should be 0".format(u))
        if n>0:
            test_error("new={0}, should be 0".format(n))
        if f>0:
            test_alert("fail={0}, not 0. Please check.".format(f))
            
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
        
    tc = TestCrawler('zulily')    
    if not options.func:
        tc.test_new_category()
    
    