import traceback
from zerorpc import Client
from settings import *

def dotest(peers):
    for p in peers:
        print p['host_string'][p['host_string'].index('@')+1:], p['port']
        c = Client('tcp://{hostname}:{port}'.format(hostname=p['host_string'][p['host_string'].index('@')+1:],
                                                    port=p['port']), timeout=None, heartbeat=None)
        try:
            c.test('test')
        except:
            traceback.print_exc()


if __name__ == '__main__':
    dotest(CRAWLER_PEERS)
    dotest(POWER_PEERS)
    dotest(TEXT_PEERS)
    
