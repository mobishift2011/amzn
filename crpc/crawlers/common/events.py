#!/usr/bin/env python
# -*- coding: utf-8 -*-
from helpers.signals import Signal

""" site, method """
pre_general_update = Signal("pre_general_update")

""" site, method, complete, reason """
post_general_update = Signal("post_general_update")

""" key, url, is_new, is_updated"""
common_saved = Signal("common_saved")

""" key, url, reason"""
common_failed = Signal("common_failed")


product_saved = Signal("product_saved")
product_failed = Signal("product_failed")
product_deleted = Signal("product_deleted")

category_saved = Signal("category_saved")
category_failed = Signal("category_failed")
category_deleted = Signal("category_deleted")

################
# Logging Events 
################

debug_info = Signal("debug_info")
warning_info = Signal("warning_info")
