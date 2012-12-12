#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
log
~~~

This module customize the logging handler so that we can acheive a colorful output

Usage:

>>> import log
>>> logger = log.getlogger("TestLogger")
>>> logger.info("this is some information")
[time]<TestLogger>INFO:this is some  information

"""
import logging
from ansistrm import ColorizingStreamHandler

handler = ColorizingStreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s]<%(name)s>%(levelname)s:%(message)s", None))
handler.setLevel(logging.DEBUG)

root = logging.getLogger()
root.addHandler(handler)

from os.path import dirname, join
import logging.handlers

current_path = dirname(__file__)

def getlogger(name, filename=join(current_path, '../logs/general.log'), level=logging.DEBUG):
    logger = logging.getLogger(name)
    handler = logging.handlers.RotatingFileHandler(filename, maxBytes=2**20, backupCount=10)
    handler.setFormatter(logging.Formatter("[%(asctime)s]<%(name)s>%(levelname)s:%(message)s", None))
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger
