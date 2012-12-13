# -*- coding: utf-8 -*-
import esm
from models import Brand
from helpers.log import getlogger

logger = getlogger('textserver', filename='/tmp/textserver.log')

logger.info('init brands index...')
brands = Brand.objects(is_delete = False).values_list('title', 'title_edit')
index = esm.Index()
for brand_tuple in brands:
    title, title_edit = brand_tuple
    brand = title_edit if title_edit else title
    index.enter(brand.lower().encode('utf-8'), brand)
index.fix()
logger.info('total brands index count:{0}'.format(len(brands)))

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