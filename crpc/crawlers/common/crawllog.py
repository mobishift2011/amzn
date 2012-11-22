#!/usr/bin/env python
# -*- coding: utf-8 -*-
from events import *
from helpers.log import getlogger

logger = getlogger("crawlerlog")


@pre_general_update.bind
def pre_hook_debug(sender,**kwargs):
    print '>>pre_hook_debug:', sender, kwargs.items()

@debug_info.bind
def debug_info_print(sender, **kwargs):
    logger.debug('<{0}> -- {1}'.format(sender, kwargs.items()))

@warning_info.bind
def warning_info_print(sender, **kwargs):
    logger.warning('<{0}> -- {1}'.format(sender, kwargs.items()))

@category_saved.bind
def on_category_saved(sender, **kwargs):
    logger.error('category{0}'.format(kwargs.items()))

@product_saved.bind
def on_product_save(sender, **kwargs):
    logger.error('product{0}'.format(kwargs.items()))

@category_failed.bind
def on_category_failed(sender, **kwargs):
    logger.error('{0}'.format(kwargs.items()))

@product_failed.bind
def on_product_failed(sender, **kwargs):
    logger.error('{0}'.format(kwargs.items()))

@common_saved.bind
def common_saved_print(sender, **kwargs):
    logger.info('<{0}> -- {1}'.format(sender, kwargs.items()))

@common_failed.bind
def common_failed_print(sender, **kwargs):
    logger.error('<{0}> -- {1}'.format(sender, kwargs.items()))

@post_general_update.bind
def post_hook_print(sender, **kwargs):
    logger.error('<{0}> -- {1}'.format(sender, kwargs.items()))
