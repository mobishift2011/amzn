# -*- coding: utf-8 -*-
import requests
import json
import re
import os
import esm

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djCatalog.djCatalog.settings")
from djCatalog.catalogs.models import Brand
from configs import SITES


print 'brand index init'
brands = Brand.objects().values_list('title')
print 'brands total count:%s' % len(brands)
index = esm.Index()
for brand in brands:
    index.enter(brand.lower().encode('utf-8'), brand)
index.fix()

class Extracter(object):
    def __init__(self):
        self.stopwords = ' \t\r\n,;.%0123456789\'"_-'
        self._rebuild_index()

    def _rebuild_index(self):
        self.index = index

    def extract(self, brand):
        ret = ''
        brand = brand.lower()
        matches = self.index.query(brand)

        for match in matches:
            startPos = match[0][0]
            endPos = match[0][1]
            pattern_brand = match[1]

            if (startPos == 0 or brand[startPos-1] in self.stopwords) and \
                (endPos == len(brand) or brand[endPos] in self.stopwords) \
                    and len(pattern_brand) > len(ret) :
                        ret = pattern_brand

        return ret


if __name__ == '__main__':
	pass