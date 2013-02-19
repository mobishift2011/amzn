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
        mongodb_pid = lsof('-t', '-i:27017').split('\n')[0]
        num_fd = int(wc(ls('/proc/{0}/fd'.format(mongodb_pid), '-l'), '-l').strip())
        print 'num_fd:',  num_fd
        if num_fd >= 20000:
            service('mongodb', 'restart')
            pkill('-f', 'run.py')
            for p in chain(CRAWLER_PEERS, POWER_PEERS, TEXT_PEERS):
                with settings(host_string=p['host_string'], warn_only=True):
                    run('kill $(sudo lsof -t -i:{0})'.format(p['port']))
    except Exception:
        import traceback
        traceback.print_exc()

def main():
    while True:
        monitor_zerorpc(CRAWLER_PEERS)
        monitor_zerorpc(POWER_PEERS)
        monitor_zerorpc(TEXT_PEERS)
        monitor_fd()
        print 'sleeping 60 seconds...'
        time.sleep(60)

if __name__ == '__main__':
    main()
