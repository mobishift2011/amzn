# -*- coding: utf-8 -*-
from backends.matching.mechanic_classifier import classify_product_department
from powers.configs import BRAND_EXTRACT
import re, htmlentitydefs
from titlecase import titlecase
from collections import Counter
from datetime import datetime

from helpers.log import getlogger
logger = getlogger('pipelines', filename='/tmp/deals.log')


def parse_price(price):
    if not price:
        return 0.

    amount = 0.
    pattern = re.compile(r'^[^\d]*(\d+(,\d{3})*(\.\d+)?)')
    match = pattern.search(price)
    if match:
        amount = (match.groups()[0]).replace(',', '')
    return float(amount)


# Removes HTML or XML character references and entities from a text string.
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


class ProductPipeline(object):
    def __init__(self, site, product):
        self.site = site
        self.product = product