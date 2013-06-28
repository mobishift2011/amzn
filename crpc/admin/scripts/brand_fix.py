from settings import MASTIFF_HOST
from crawlers.common.routine import get_site_module
from crawlers.common.stash import picked_crawlers
from powers.brandapi import Extracter
from collections import Counter
import slumber
import sys

api = slumber.API(MASTIFF_HOST)

def update_mastiff(instance):
    instance_type = instance.__class__.__name__.lower()
    if instance_type == 'product':
        param_key = 'brand'
    elif instance_type == 'event':
        param_key = 'brands'
    if instance.muri:
        getattr(api, instance_type)(instance.muri.split('/')[-2]).patch({param_key: instance.favbuy_brand})


def main(brand):
    counter = Counter()
    brand_extracter = Extracter()
    for site in picked_crawlers:
        print 'site:', site
        m = get_site_module(site)
        products = m.Product.objects(favbuy_brand=brand)
        for product in products:
            favbuy_brand = brand_extracter.extract(product.brand) \
                or brand_extracter.extract(product.title)
            if not favbuy_brand:
                counter[product.favbuy_brand+'___'+(product.brand or '')] += 1 
                print product.brand
                print product.title
                print product.combine_url; print
                continue
            counter[favbuy_brand] += 1
            if brand.lower() in favbuy_brand.lower():
                product.favbuy_brand = favbuy_brand
                update_mastiff(product)
                product.save()
    print counter


if __name__ == '__main__':
    main(sys.argv[1])
    #5076
