#!/usr/bin/env python
# -*- coding: utf-8 -*-
from settings import CRAWLER_PEERS
import zerorpc
import re

def get_rpcs(peers=CRAWLER_PEERS):
    """
        On one hand, we build a zerorpc client object,
            if the program keep going, the open file handler resource is still hold,
            so we can not build a zerorpc client every time, and need to keep the zerorpc client objects.
        On the other hand, we need to detect PEERS change in settings,
            so we need to keep PEERS in the function, and compare old and new PEERS.
    """
    if not hasattr(get_rpcs, '_cached_rpcs'):
        setattr(get_rpcs, '_cached_rpcs', {})

    peers_key = repr(peers)
    if peers_key not in get_rpcs._cached_rpcs:
        rpcs = []
        for peer in peers:
            host = peer['host_string'][peer['host_string'].index('@')+1:]
            port = peer['port']
            client_string = 'tcp://{0}:{1}'.format(host, port)
            c = zerorpc.Client(client_string, timeout=120, heartbeat=None)
            if c:
               rpcs.append(c)

        get_rpcs._cached_rpcs[peers_key] = rpcs

    return get_rpcs._cached_rpcs[peers_key]

if __name__ == '__main__':
    get_rpcs()
