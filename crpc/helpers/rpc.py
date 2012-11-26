#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import CRAWLER_PEERS, CRAWLER_PORT
import zerorpc

def get_rpcs(peers=CRAWLER_PEERS, port=CRAWLER_PORT):
    """
        On one hand, we build a zerorpc client object,
            if the program keep going, the open file handler resource is still hold,
            so we can not build a zerorpc client every time, and need to keep the zerorpc client objects.
        On the other hand, we need to detect PEERS change in settings,
            so we need to keep PEERS in the function, and compare old and new PEERS.
    """
    if not hasattr(get_rpcs, '_cached_peers'):
        setattr(get_rpcs, '_cached_peers', [])

    if get_rpcs._cached_peers != peers:
        for c in get_rpcs._cached_rpcs:
            c.close()

        setattr(get_rpcs, '_cached_peers', peers)

        rpcs = []
        for peer in peers:
            host = peer[peer.find('@')+1:]
            client_string = 'tcp://{0}:{1}'.format(host, port)
            print 'connecting to...', client_string
            c = zerorpc.Client(client_string, timeout=None)
            if c:
               rpcs.append(c)

        setattr(get_rpcs, '_cached_rpcs', rpcs)

    return get_rpcs._cached_rpcs

