import traceback
from zerorpc import Client
from settings import PEERS

for p in PEERS:
    username, hostname = p.split('@')
    print 'testing', hostname
    c = Client('tcp://{hostname}:1234'.format(hostname=hostname))
    try:
        #c.call('test','123')
        c.image('test')
    except:
        traceback.print_exc()
