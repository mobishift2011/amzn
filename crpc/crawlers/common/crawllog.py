#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from events import *
from helpers.log import getlogger

logger = getlogger("crawlerlog")

@debug_info.bind
def debug_info_print(sender, **kwargs):
    logger.debug('<{0}> -- {1}'.format(sender, kwargs.items()))

@warning_info.bind
def warning_info_print(sender, **kwargs):
    logger.warning('<{0}> -- {1}'.format(sender, kwargs.items()))
