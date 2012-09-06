#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Handles rpc calls 

rpc messages/responses are all msgpacked 

{"op":"all_status"}     ->    tell me about all the worker status of this server
{"op":"add_worker","worker_name":"name"}   ->  add name.py to workers
{"op":"stop_worker","uuid":"asdfasdfasdf"} ->  stop worker
"""
import configs
import logging
import os

logger = logging.getLogger("rpc")

from gevent.server import StreamServer
from api import Controller

controller = Controller()

def handle(socket, address):
    logger.debug('New connection from {0}:{1}'.format(*address))
    fileobj = socket.makefile()
    while True:
        line = fileobj.readline()
        logger.debug(line)

        if not line:
            logger.debug("Client {0}:{1} disconnected".format(*address))
            break

        # pass calls to controller
        # returns a string to response
        response = controller.request(line)

        fileobj.write(response)
        fileobj.flush()

def serve_forever():
    controller.start_workers()
    server = StreamServer(('0.0.0.0', configs.ROOT_PORT), handle)
    logger.info('Starting echo server on port {0}'.format(configs.ROOT_PORT))
    server.serve_forever()

if __name__ == '__main__':
    serve_forever()
