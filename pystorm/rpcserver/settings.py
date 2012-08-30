#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

PORT = 8144

import logging
from ansistrm import ColorizingStreamHandler
#logging.basicConfig(level=logging.DEBUG,
#                    format='[%(asctime)s]<%(name)s>%(levelname)s:%(message)s',
#                    )#filename='stormapi.log',
#                    #filemode='a')
handler = ColorizingStreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s]<%(name)s>%(levelname)s:%(message)s", None))
root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(handler)
