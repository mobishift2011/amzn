# -*- coding: utf-8 -*-
import esm
from models import Brand
from helpers.log import getlogger

logger = getlogger('brandapi', filename='/tmp/textserver.log')

class Extracter(object):
    def __init__(self):
        self.stopwords = ' \t\r\n,;.%0123456789\'"_-'
        logger.info('init brands index...')
        self.index = self.__build_index()

    def __build_index(self):
        brands = Brand.objects(is_delete = False).values_list('title', 'title_edit', 'alias')
        index = esm.Index()
        for brand_tuple in brands:
            title, title_edit, alias = brand_tuple
            brand = title_edit if title_edit else title
            for brand_key in alias:
                if brand_key == 'undefined':
                    continue
                index.enter(brand_key.lower().encode('utf-8'), brand)
            index.enter(brand.lower().encode('utf-8'), brand)
        index.fix()
        logger.info('total brands index count:{0}'.format(brands.count()))
        return index

    def rebuild_index(self):
        logger.info('rebulid brands index...')
        self.index = self.__build_index()

    def extract(self, brand):
        ret = ''
        brand = brand.lower().encode('utf-8') if brand else ''
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
