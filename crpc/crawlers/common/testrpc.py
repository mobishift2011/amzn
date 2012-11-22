import zerorpc
from settings import PEERS, RPC_PORT
from routine import *
#update_category, update_listing, update_product

def get_rpcs():
    rpcs = []
    for peer in PEERS:
        host = peer[peer.find('@')+1:]
        c = zerorpc.Client('tcp://{0}:{1}'.format(host, RPC_PORT), timeout=None)
        if c:
            rpcs.append(c)
    return rpcs

if __name__ == '__main__':
    rpc = get_rpcs()
    from crawllog import *
    update_category('zulily', rpc, concurrency=3)
    new_listing('zulily', rpc, concurrency=2)
    new_product('zulily', rpc, concurrency=2)
    #update_product('zulily', rpc, concurrency=30)
    #update_listing('zulily', rpc, concurrency=20)
    #update_product('myhabit', rpc, concurrency=30)

