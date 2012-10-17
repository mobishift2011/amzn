#!/usr/bin/env python
# -*- coding: utf-8 -*-
from helpers.signals import Signal

# usage:
# product_updated.send(sender="amazon.parsepage", product = product, updated_fields = ['title',... ])
product_updated = Signal("product_updated")

product_deleted = Signal("product_deleted")

product_analysis_failed = Signal("product_analysis_failed")

product_created = Signal("product_created")

page_parse_error = Signal("page_parse_error")

page_download_failed = Signal("page_download_failed")

debug_info =  Signal("debug_info")
