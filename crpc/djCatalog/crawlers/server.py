# -*- coding: utf-8 -*-
import os, sys
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )
os.environ['DJANGO_SETTINGS_MODULE'] = "djCatalog.settings"

from catalogs.models import *
from lxml import html
import requests
import time
from sites import sites


"""
When a new site's brands is to be crawled,
just do as the following step-by-step.
1) define the function as: def funcname()
2) add your site to the sites.py
3) the site name and the function name should be the same.
"""

class Crawler(object):
    def __init__(self, sites):
        self.__sites = []
        paths = []
        map(lambda x: self.__sites.append(x[0]) and paths.append(x[1]), sites)
        map(__import__, paths)
        map(self.regist, self.__sites)
    
    def regist(self, site):
        setattr(self, site, eval(site))
    
    def crawl(self):
        map(lambda x: getattr(self, x)() if hasattr(self, x) else None, self.__sites)
    
    def rmDuplicate(self):
        # TODO
        return


def saksfifthavenue():
    print '\nbegin to crawl saksfifthavenue'
    
    total_count = 0
    actual_count = 0
    url = 'http://www.saksfifthavenue.com/main/ShopByBrand.jsp'
    res = requests.get(url).text
    dom = html.fromstring(res)
    brands = dom.xpath("//div[@class='designer-list clearfix']/ul/li/a")
    # TODO catch A INDEX Brand
    for brand in brands:
        total_count += 1
        brand, is_new = Brand.objects.get_or_create(title=brand.text.strip())
        actual_count += 1 if is_new else 0
    
    print 'total brands:%s, actual crawling:%s' % (total_count, actual_count)
    print 'end to crawl saksfifthavenue\n'


def bloomingdales():
    print '\nbegin to crawl bloomingdales'
    
    base_url = 'http://www1.bloomingdales.com/buy/designer-'
    url_keys = (
        ('women?Action=designer&designer=Women', 'Women'),
        ('men?designer=Men&Action=designer', 'Men'),
        ('shoes?designer=Shoes&Action=designer', 'Shoes'),
        ('handbags?designer=Handbags&Action=designer', 'Handbags'),
        ('beauty?designer=Beauty&Action=designer', 'Beauty'),
        ('jewelry-accessories?designer=Jewelry+%26+Accessories&Action=designer', 'Jewelry and Accessories'),
        ('kids?designer=Kids&Action=designer', 'Kids'),
        ('home?designer=Home&Action=designer', 'Home'),
    )
    
    for url_key, dept in url_keys:
        print 'begin to crawl brand from dept: %s' % dept
        total_count = 0
        actual_count = 0
        url = base_url + url_key
        res = requests.get(url).text
        dom = html.fromstring(res)
        brands = dom.xpath('//li[@class="se_designerColumn"]/a')
        for brand in brands:
            total_count += 1
            brand, is_new = Brand.objects.get_or_create(title=brand.text.strip())
            actual_count += 1 if is_new else 0
            if dept not in brand.dept:
                brand.dept.append(dept)
                brand.save()
        print 'total brands:%s, actual crawling:%s' % (total_count, actual_count)
        time.sleep(3)
    
    print 'end to crawl bloomingdales\n'


def shopbop():
    print '\nbegin to crawl shopbop'
    total_count = 0
    actual_count = 0
    url = 'http://cn.shopbop.com/actions/designerindex/viewAlphabeticalDesigners.action'
    res = requests.get(url).text
    dom = html.fromstring(res)
    brands = dom.xpath('//div[@class="brandGrouping"]/a')
    for brand in brands:
        total_count += 1
        brand, is_new = Brand.objects.get_or_create(title=brand.text.strip())
        actual_count += 1 if is_new else 0
    
    print 'total brands:%s, actual crawling:%s' % (total_count, actual_count)
    print 'end to crawl shopbop\n'

def nordstrom():
    print '\nbegin to crawl nordstrom'
    total_count = 0
    actual_count = 0
    url = 'http://shop.nordstrom.com/c/brands-list'
    res = requests.get(url).text
    dom = html.fromstring(res)
    brands = dom.xpath('//div[@class="brand-section clearfix"]/ul/li/a')
    for brand in brands:
        total_count += 1
        brand, is_new = Brand.objects.get_or_create(title=brand.text.strip())
        actual_count += 1 if is_new else 0
    
    # TODO category info add
    
    print 'total brands:%s, actual crawling:%s' % (total_count, actual_count)
    print 'end to crawl nordstrom\n'

def amazon():
    print '\nbegin to crawl amazon'
    total_count = 0
    actual_count = 0
    url = 'http://www.amazon.com/b?ie=UTF8&node=2479929011'
    res = requests.get(url).text
    dom = html.fromstring(res)
    brands = dom.xpath('//div[@class="list"]/ul/li/a')
    for brand in brands:
        total_count += 1
        brand, is_new = Brand.objects.get_or_create(title=brand.text.strip())
        actual_count += 1 if is_new else 0
    
    # TODO category info add
    
    print 'total brands:%s, actual crawling:%s' % (total_count, actual_count)
    print 'end to crawl amazon\n'

def global_blue():
    print '\nbegin to crawl global_blue'
    total_count = 0
    actual_count = 0
    url = 'http://www.global-blue.com/brands/'
    res = requests.get(url).text
    dom = html.fromstring(res)
    brands = dom.xpath('//div[@class="columns"]/ul/li/a')
    for brand in brands:
        total_count += 1
        brand, is_new = Brand.objects.get_or_create(title=brand.text.strip())
        actual_count += 1 if is_new else 0
    
    print 'total brands:%s, actual crawling:%s' % (total_count, actual_count)
    print 'end to crawl global_blue\n'


def ashford():
    print '\nbegin to crawl ashford'
    total_count = 0
    actual_count = 0
    url = 'http://www.ashford.com/watches/cat5005.cid'
    dept = 'watches'
    res = requests.get(url).text
    dom = html.fromstring(res)
    brands = dom.xpath('//div[@class="catSubNavWrap"]/ul/li/a')
    for brand in brands:
        total_count += 1
        brand, is_new = Brand.objects.get_or_create(title=brand.text.strip())
        if dept not in brand.dept:
            brand.dept.append(dept)
            brand.save()
        actual_count += 1 if is_new else 0
        
    print 'total brands:%s, actual crawling:%s' % (total_count, actual_count)
    print 'end to crawl ashford\n'


def gilt():
    print '\nbegin to crawl gilt'
    total_count = 0
    actual_count = 0
    url = 'http://www.gilt.com/brands'
    res = requests.get(url).text
    dom = html.fromstring(res)
    brands = dom.xpath('//div[@class="favorite-tooltip-link"]/button/@data-gilt-brand-name')
    for brand in brands:
        total_count += 1
        brand, is_new = Brand.objects.get_or_create(title=brand.strip())
        actual_count += 1 if is_new else 0
    
    print 'total brands:%s, actual crawling:%s' % (total_count, actual_count)
    print 'end to crawl gilt\n'


if __name__ == '__main__':
#    Crawler(sites).crawl()
    for brand in Brand.objects():
        if not brand.dept:
            brand.dept.append('')