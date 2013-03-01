import requests
import lxml.html
import re
from datetime import datetime
from models import Product


class Onekingslane(object):
    def __init__(self):
        self.s = requests.session()
        self.headers = {
        }
    
    def check_product_right(self):
        utcnow = datetime.utcnow()
        obj = Product.objects(products_end__gt=utcnow).timeout(False)
        print 'Onekingslane have {0} products.'.format(obj.count())

        for prd in obj:
            ret = self.s.get(prd.combine_url, headers=self.headers)
            tree = lxml.html.fromstring(ret.content)
            title = tree.cssselect('#productOverview h1.serif')[0].text_content()
            price = tree.cssselect('p#oklPriceLabel')[0].text_content()
            listprice = tree.cssselect('p#msrpLabel')[0].text_content().replace('Retail', '').strip()
            soldout = True if tree.cssselect('.sold-out') else False
            if prd.title.lower() != title.lower:
                print 'onekingslane product[{0}] title error: [{1}, {2}]'.format(prd.combine_url, title, prd.title)
            if price != prd.price:
                print 'onekingslane product[{0}] price error: {1} vs {2}'.format(prd.combine_url, price, prd.price)
            if listprice != prd.listprice:
                print 'onekingslane product[{0}] listprice error: {1} vs {2}'.format(prd.combine_url, listprice, prd.listprice)
            if soldout !=  prd.soldout:
                print 'onekingslane product[{0}] soldout error: {1} vs {2}'.format(prd.combine_url, soldout, prd.soldout)


    def get_product_abstract_by_url(self, url):
        product_id = re.compile(r'/product/\d+/(\d+)').search(url).group(1)
        content = self.s.get(url, headers=self.headers).content
        t = lxml.html.fromstring(content)
        title = t.xpath('//html/head/title')[0].text.encode('utf-8')
        description = t.xpath('//*[@id="description"]/p')[0].text.encode('utf-8')
        return 'onekingslane_'+product_id, title+'_'+description

if __name__ == '__main__':
    Onekingslane().get_product_abstract_by_url(test_url)
