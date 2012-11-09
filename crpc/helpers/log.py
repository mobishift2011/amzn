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

root = logging.getLogger()
root.setLevel(logging.INFO)
root.addHandler(handler)

def getlogger(name):
    return logging.getLogger(name)
