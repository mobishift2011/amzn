import traceback
from zerorpc import Client
from settings import *

def test(peers, port):
    for p in peers:
        username, hostname = p.split('@')
        print 'testing', hostname
        c = Client('tcp://{hostname}:{port}'.format(hostname=hostname, port=port))
        try:
            c.image('test')
        except:
            traceback.print_exc()


if __name__ == '__main__':
    test(CRAWLER_PEERS, CRAWLER_PORT)
    test(POWER_PEERS, POWER_PORT)
    
