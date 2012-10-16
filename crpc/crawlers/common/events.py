#!/usr/bin/env python
# -*- coding: utf-8 -*-
from helpers.signals import Signal

""" pre_general_update kwargs:

site        =   site
method      =   method

"""
pre_general_update = Signal("pre_general_update")

""" post_general_update kwargs:

site        =   site
method      =   method
complete    =   True
reason      =   ...

"""
post_general_update = Signal("post_general_update")

""" product_saved kwargs:

site        =   site         (amazon, newegg, ...)
key         =   key          
is_new      =   False
is_updated  =   False 

"""
product_saved = Signal("product_saved")


""" product_failed kwargs:

site    =   site         (amazon, newegg, ...)
url     =   url        
resaon  =   ...

"""
product_failed = Signal("product_failed")


""" product_deleted kwargs:

site    =   site         (amazon, newegg, ...)
key     =   key          
resaon  =   ...

"""
product_deleted = Signal("product_deleted")

category_saved = Signal("category_saved")
category_failed = Signal("category_failed")
category_deleted = Signal("category_deleted")

################
# Logging Events 
################

debug_info = Signal("debug_info")
warning_info = Signal("warning_info")
