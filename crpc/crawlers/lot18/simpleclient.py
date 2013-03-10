import requests
import lxml.html
import re
from datetime import datetime

from server import lot18Login
from models import Product


class CheckServer(object):
    def __init__(self):
        self.s = requests.session()
        self.headers = {}
        self.net = lot18Login()
        self.net.check_signin()
        self.soldout = re.compile('<p class="main">.*Unfortunately,.*</p>')
        self.title = re.compile('<div class="product-info product-name">\s*<h1>(.*)</h1>\s*</div>')
    
    def check_onsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nlot18 {0}, {1}\n\n'.format(id, url)
            return

        ret = self.net.fetch_page(url)
        if isinstance(ret, int):
            ret = self.net.fetch_page(url)
            if isinstance(ret, int):
                return
        soldout = True if self.soldout.search(ret) else False
        if prd.soldout != soldout:
            print 'lot18 product[{0}] soldout error: {1} vs {2}'.format(url, prd.soldout, soldout)
            prd.soldout = soldout
            prd.update_history.update({ 'soldout': datetime.utcnow() })
            prd.save()

        if soldout: return
        title = self.title.search(ret).group(1)
        if prd.title.encode('utf-8').lower() != title.lower():
            print 'lot18 product[{0}] title error: [{1} vs {2}]'.format(url, prd.title.encode('utf-8'), title)
            prd.title = title
            prd.update_history.update({ 'title': datetime.utcnow() })
            prd.save()

        tree = lxml.html.fromstring(ret)
        price = tree.cssselect('div.container-content div.container-product-detail div.container-product-info span.product-total')
        if not price:
            print '\n\nlot18 product[{0}] price not found \n\n'.format(url)
            return
        price = price[0].text_content().replace('$', '').strip()
        if float(prd.price) != float(price):
            print 'lot18 product[{0}] price error: {1} vs {2}'.format(url, prd.price, price)
            prd.price = price
            prd.update_history.update({ 'price': datetime.utcnow() })
            prd.save()


    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

    def get_product_abstract_by_url(self, url):
        content = self.s.get(url, headers=self.headers).content
        product_id = re.compile(r'/product/(\d+)').search(url).group(1)
        t = lxml.html.fromstring(content)
        title = t.xpath('//h1')[0].text.encode('utf-8')
        description = []
        for desc in t.xpath('//div[contains(@class,"product-description")]'):
            description.append(desc.text_content().encode('utf-8'))
        description = '\n'.join(description)
        return 'lot18_'+product_id, title+'_'+description

if __name__ == '__main__':
    CheckServer()
