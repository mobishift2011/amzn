from zerorpc import Client
from zerorpc.exceptions import RemoteError, TimeoutExpired
from settings import *
from fabric.api import *
import time

def monitor_zerorpc(peers):
    for p in peers:
        print p['host_string'][p['host_string'].index('@')+1:], p['port'],
        c = Client('tcp://{hostname}:{port}'.format(hostname=p['host_string'][p['host_string'].index('@')+1:],
                                                    port=p['port']), timeout=60, heartbeat=None)
        try:
            c.test('test')
        except RemoteError:
            print 'passed'
        except TimeoutExpired:
            with settings(host_string=p['host_string'], warn_only=True):
                run('kill $(sudo lsof -t -i:{0})'.format(p['port']))

def monitor_fd():
    from sh import lsof, wc, ls, pkill, service
    try:
        mongodb_pid = lsof('-t', '-i:27017', '-sTCP:LISTEN').split('\n')[0]
        num_fd = int(wc(lsof('-p', '{0}'.format(mongodb_pid)), '-l').strip())
        print 'num_fd:',  num_fd
        if num_fd >= 4096:
            #service('mongodb', 'restart')
            pkill('-f', 'run.py')
            for p in chain(CRAWLER_PEERS, POWER_PEERS, TEXT_PEERS):
                with settings(host_string=p['host_string'], warn_only=True):
                    run('kill $(sudo lsof -t -i:{0})'.format(p['port']))
    except Exception:
        import traceback
        traceback.print_exc()

def monitor_publisher_size():
    #ps aux | grep publish | awk '{print $6}'
    from sh import ps, grep, pkill
    try:
        psinfo = grep(ps('aux'), 'publish')
        mem_used = int(psinfo.strip().split()[5])
        print 'mem_publish:', mem_used
        if mem_used >= 1 * 1024 * 1024: #(1G = 1*1024*1024K)
            pkill('-f', 'publish.py')
    except Exception:
        import traceback
        traceback.print_exc()

def main():
    while True:
        monitor_zerorpc(CRAWLER_PEERS)
        monitor_zerorpc(POWER_PEERS)
        monitor_zerorpc(TEXT_PEERS)
        monitor_fd()
        monitor_publisher_size()
        print 'sleeping 60 seconds...'
        time.sleep(60)

if __name__ == '__main__':
    main()
