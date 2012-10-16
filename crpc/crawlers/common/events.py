#!/usr/bin/env python
# -*- coding: utf-8 -*-
from helpers.signals import Signal

# usage:
# product_updated.send(sender="amazon.parsepage", product = product, updated_fields = ['title',... ])
product_updated = Signal("product_updated")

product_deleted = Signal("product_deleted")

product_analysis_failed = Signal("asdfasdfasdf")
