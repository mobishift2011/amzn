# -*- coding: utf-8 -*-
from settings import MASTIFF_HOST
from crawlers.common.stash import picked_crawlers
from powers.models import Brand
from mongoengine import Q
from helpers.log import getlogger
import slumber
import json
import requests
from datetime import datetime
import traceback


brands = Brand.objects()
brand_dict = {(brand.title_edit or brand.title): [] for brand in brands}
print 'total brands: ', len(brands), ' , ',  'dict size: ', len(brand_dict.items())


def sync2mastiff():
    pass


def main():
    for site in picked_crawlers:
        m = __import__("crawlers."+site+'.models', fromlist=['Product'])
        products = m.Product.objects( Q(products_end__gt=datetime.utcnow()) | Q(products_end__exists=False) )
        print 'site: {0}, products: {1}'.format(site, products.count())
        for product in products:
            tags = brand_dict.get(product.favbuy_brand)
            if tags:
                brand_dict[product.favbuy_brand] = list[set(product.favbuy_tag) | set(tags)]
    
    print 'now dict size: ', len(brand_dict.items())
    for k, v in brand_dict.iteritems():
        if v:
            print v


if __name__ == '__main__':
    main()