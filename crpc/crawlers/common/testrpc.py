import zerorpc
from settings import PEERS, RPC_PORT
from routine import update_listing

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
    update_listing('amazon', rpc, concurrency=5)
