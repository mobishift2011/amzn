#from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from amzn.items import ProductItem
from scrapy.http import Request
import pymongo

class AmazonCatSpider(BaseSpider):
    name = "amazon-cat"
    allowed_domains = ["www.amazon.com"]
    start_urls = [
        'http://www.amazon.com/s/ref=lp_165993011_ex_n_1?rh=n%3A165793011&bbn=165793011&ie=UTF8&qid=1344224775',
    ]

    mgdb_conn = pymongo.Connection('localhost')
    mgdb_coll = mgdb_conn['amazon']['cats']
    root_cat = "Toys & Games"
    
    def parse(self, response):
        cat_prefix = response.request.meta.get('cd',[self.root_cat])
        hxs = HtmlXPathSelector(response)
#        items = hxs.select('//div[@id="leftNavContainer"]/*/ul[1]//span[@class="refinementLink"]')  # text node for the subcategory
        items = hxs.select('//div[@id="leftNavContainer"]//ul[@data-typeid="n"]//span[@class="refinementLink"]')
        if not items:
            self.set_cats_leaf(cat_prefix)
        reqs = []
        for item in items:
            url = item.select("parent::*/@href").extract()[0]
            cat = item.select('text()').extract()[0].strip()
            num = item.select('following-sibling::span/text()').re('\((.*)\)')
            if cat_prefix[-1] == cat: # trap "Household Insulation": http://www.amazon.com/s/ref=sr_ex_n_1?rh=n%3A228013%2Cn%3A!468240%2Cn%3A551240%2Cn%3A495346&bbn=495346&ie=UTF8&qid=1344909516
                continue
            cats = cat_prefix+[cat]
            if self.cats_seen(cats):
                print cats, "seen"
                continue

            req = Request("http://www.amazon.com"+url)
            req.meta['cd'] = cats
            reqs.append(req)
            print "URL ==>", url
            print "Category ==>", " > ".join(req.meta['cd'])
            print "Number ==>", num
            self.save_cats(url, cats, num)
        return reqs

    def cats_seen(self, cats):
        cats_str = " > ".join(cats)
        return self.mgdb_coll.find_one({'catstr':cats_str})

    def save_cats(self, url, cats, num):
        cats_str = " > ".join(cats)
        self.mgdb_coll.insert({'url':url, 'cats':cats, 'catstr': cats_str, 'num': num})
        
    def set_cats_leaf(self, cats):
        '''set the category node as leaf node'''
        cats_str = " > ".join(cats)
        row = self.mgdb_coll.find_one({'catstr':cats_str})
        if row:
            row['leaf'] = 1
            self.mgdb_coll.save(row)
        
