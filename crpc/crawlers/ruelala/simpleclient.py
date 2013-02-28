import requests
import lxml.html
import re
from datetime import datetime
from models import Product


class Ruelala(object):
    def __init__(self):
        self.s = requests.session()
        self.login_url = 'http://www.ruelala.com/access/gate'
        self.s.get(self.login_url)
        self.s.post('http://www.ruelala.com/access/formSetup', data={'userEmail':'','CmsPage':'/access/gate','formType':'signin'})
        self.data = {
            'email': '2012luxurygoods@gmail.com',
            'password': 'abcd1234',
            'loginType': 'gate',
            'rememberMe': 1, 
        }       
        self.s.post('https://www.ruelala.com/registration/login', data=self.data)
    
    def check_product_right(self):
        utcnow = datetime.utcnow()
        obj = Product.objects(products_end__gt=utcnow).timeout(False)
        print 'Ruelala have {0} products.'.format(obj.count())

        for prd in obj:
            cont = self.s.get(prd.combine_url).content
            tree = lxml.html.fromstring(cont)
            title = tree.cssselect('h2#productName')[0].text_content().strip()
            listprice = tree.cssselect('span#strikePrice')[0].text_content().strip()
            price = tree.cssselect('span#salePrice')[0].text_content().strip()
            soldout = tree.cssselect('span#inventoryAvailable')
            if title != prd.title:
                print 'ruelala product[{0}] title error: [{1}, {2}]'.format(prd.combine_url, title, prd.title)
            if listprice != prd.listprice:
                print 'ruelala product[{0}] listprice error: [{1}, {2}]'.format(prd.combine_url, listprice, prd.listprice)
            if price != prd.price:
                print 'ruelala product[{0}] price error: [{1}, {2}]'.format(prd.combine_url, price, prd.price)


    def get_product_abstract_by_url(self, url):
        content = self.s.get(url).content
        product_id = re.compile(r'/product/(\d+)').search(url).group(1)
        t = lxml.html.fromstring(content)
        title = t.xpath('//*[@id="productName"]')[0].text
        description = ''
        for li in t.xpath('//*[@id="info"]/ul/li'):
            description += li.text_content() + '\n'
        return 'ruelala_'+product_id, title+'_'+description

if __name__ == '__main__':
    Ruelala().check_product_right()
