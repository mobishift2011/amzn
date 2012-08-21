#from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from amzn.items import ProductItem
from scrapy.http import Request
import pymongo, re, time

# try to implement a spider that does both listing and detail pages

class AmazonSpider(BaseSpider):
    name = "amazon"
    allowed_domains = ["www.amazon.com"]
    #start_urls = ['http://www.amazon.com/s/ref=sr_nr_n_5?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A2242348011&bbn=493964&ie=UTF8&qid=1342426287&rnid=493964']
    max_detail_pages = 1000
    
    mgdb_conn = pymongo.Connection('localhost')
    cats = mgdb_conn['amazon']['cats']
    products = mgdb_conn['amazon']['products']
    products.ensure_index('asin', unique=True)
    
    def parse(self, response):
        page = response.request.meta.get('page', 'listing')
        if page == 'listing':
            return self.parse_listing(response)
        else:
            return self.parse_detail(response)
            
    def parse_listing(self, response):
        hxs = HtmlXPathSelector(response)
        items = hxs.select('//div[@id="btfResults"]//div[@class="data"]//a[@class="title"]')
        items.extend(hxs.select('//div[@id="atfResults"]//div[@class="data"]//a[@class="title"]'))
#        items = hxs.select('//div[@id="atfResults"]//div[@class="productTitle"]/a | //div[@id="btfResults"]//div[@class="productTitle"]/a') # When using scrapy shell, this one works fine.
        reqs = []; cnt = response.request.meta.get('count',0)
        cat = response.request.meta.get('catstr','')  #Electronics Warranties')
        
        for item in items:
            cnt += 1
            if cnt > self.max_detail_pages:
                break
            url =  item.select('@href').extract()[0]
            url = self.normalize_detail_url(url)
            if self.check_seen(url):
                continue
            print "URL ==>", url
            print "Proudct ==>", item.select('text()').extract()
            print "cnt=", cnt
            req = Request(url)
            req.meta['page'] = 'detail'
            req.meta['catstr'] = cat
            reqs.append(req); 
            
        if cnt < self.max_detail_pages:
            next_page = hxs.select('//a[@id="pagnNextLink"]/@href').extract()
            if next_page:
                req = Request("http://www.amazon.com" + next_page[0])
                req.meta['page'] = 'listing'
                req.meta['count'] = cnt
                req.meta['catstr'] = cat
                reqs.append(req)
            else:
                self.mark_complete(cat)
        else:
            self.mark_complete(cat)
        return reqs

    def parse_detail(self, response):
        url = response.request.url
        asin = url.split('/')[-1]
        catstr = response.request.meta['catstr']
        hxs = HtmlXPathSelector(response)
        try:
            title = hxs.select('//span[@id="btAsinTitle"]/text()').extract()[0]
        except:
            # title = '' is unnecessary, because of this exception
            with open('/home/favbuy/indexerror.txt', 'a') as fd:
                fd.write('\nOne response url: ' + response.url + '\n')
                fd.write(response.body + '\n\n')
        try:
            vartitle = hxs.select('//span[@id="variationProductTitle"]/text()').extract()[0]
        except:
            vartitle = ""
        try:
            price = hxs.select('//span[@id="actualPriceValue"]/b/text()').extract()[0]
        except:
            price = "unknown"
        summary = hxs.select('//td[@class="bucket"]//div[@class="content"]//ul[1]')
        if summary:
            model = summary[0].select('li[contains(b, "Item model number")]/text()').extract()
            model = model[0] if model else ""
            rank = summary[0].select('li[@id="SalesRank"]//text()').extract()
            if rank:
                rank = ''.join(rank).replace('\n', '').split(':', 1)[1]
                rank = re.sub('\(.*(}|\))', '', rank).strip()
            else:
                rank = ""
        else:
            model = ""
            rank = ""
        summary = summary.extract()[0] if summary else ""
        print "title:", title
        print "vartitle:", vartitle
        print "price:", price
        print "model:", model
        print "asin:", asin
        print 'rank', rank
        self.products.insert({"url":url, "title":title, "vartitle":vartitle, "price":price, "model":model, "asin":asin, "summary":summary, 'catstr':catstr, 'rank':rank})
        return None
        
    def normalize_detail_url(self, url):
        return re.sub('(.*/dp/[^/]*)/(.*)', r'\1', url)
        
    def check_seen(self, url):
        '''check if the product url has been seen before.
        '''
        asin = url.split('/')[-1]
        return self.products.find_one({'asin':asin})
    
    def mark_complete(self, cat):
        '''mark no more urls to include for downloading'''
        print "mark", cat, "complete"
        row = self.cats.find_one({'catstr': cat})
        if row:
            row['complete'] = 1
            row['complete_time'] = int(time.time())
            self.cats.save(row)
        
