#!/usr/bin/env python
# -*- coding: utf-8 -*-
from helpers.signals import Signal

""" product_saved kwargs:

site        =   site         (amazon, newegg, ...)
key         =   key          
is_new      =   False
is_updated  =   False 

"""
product_saved = Signal("product_saved")


""" product_failed kwargs:

site    =   site         (amazon, newegg, ...)
key     =   key          
resaon  =   ...

"""
product_failed = Signal("product_failed")


""" product_deleted kwargs:

site    =   site         (amazon, newegg, ...)
key     =   key          
resaon  =   ...

"""
product_deleted = Signal("product_deleted")

<<<<<<< HEAD

category_saved = Signal("category_saved")
category_failed = Signal("category_failed")
category_deleted = Signal("category_deleted")
=======
product_analysis_failed = Signal("product_analysis_failed")

product_created = Signal("product_created")

page_parse_error = Signal("page_parse_error")

page_download_failed = Signal("page_download_failed")

debug_info =  Signal("debug_info")
>>>>>>> 556009a04c97d96af99147befc6fd611cf6a4c6a
