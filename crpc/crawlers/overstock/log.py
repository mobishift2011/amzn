#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Yuande <miraclecome (at) gmail.com>
# This code is under Creative Commons CC BY-NC-SA license
# http://creativecommons.org/licenses/by-nc-sa/3.0/

import logging

def init(log_name, log_file, level=logging.DEBUG, size=1024*1024, count=10):
    import logging.handlers

    logger = logging.getLogger(log_name)
    logger.setLevel(level)

    formatter = logging.Formatter("%(levelname)s [%(asctime)s]: %(message)s")

    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=size, backupCount = count)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger



def log_print(msg, logger=None, level=logging.DEBUG):
    if logger != None:
        logger.log(level, msg)
    else:
        print(msg)


def log_traceback(logger=None, msg=None):
    '''
    log exception traceback to logger
    a litter difference from log.exception
    '''
    import sys, traceback

    if msg != None:
        log_print(msg, logger, logging.ERROR)

    ei = sys.exc_info()
    lines = traceback.format_exception(ei[0], ei[1], ei[2])
    for line in lines[:-1]:
        elines = line.splitlines()
        for eline in elines:
            log_print(eline.rstrip(), logger, logging.ERROR)
    
    log_print(lines[-1], logger, logging.ERROR)

if __name__ == '__main__':
    try:
        1/0
    except:
        log_traceback()
