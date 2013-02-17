from zerorpc import Client
from zerorpc.exceptions import RemoteError, TimeoutExpired
from settings import *
from fabric.api import *
import time

def monitor(peers):
    for p in peers:
        print p['host_string'][p['host_string'].index('@')+1:], p['port'],
        c = Client('tcp://{hostname}:{port}'.format(hostname=p['host_string'][p['host_string'].index('@')+1:],
                                                    port=p['port']), timeout=60, heartbeat=None)
        try:
            c.test('test')
        except RemoteError:
            print 'passed'
        except TimeoutExpired:
            with settings(host_string=p['host_string']):
                run('kill -9 `pgrep -f {0}`'.format(p['port']))

def main():
    while True:
        monitor(CRAWLER_PEERS)
        monitor(POWER_PEERS)
        monitor(TEXT_PEERS)
        print 'sleeping 60 seconds...'
        time.sleep(60)

if __name__ == '__main__':
    main()
