import requests
import lxml.html
import re
import slumber
from datetime import datetime

from settings import MASTIFF_HOST
from models import Product

api = slumber.API(MASTIFF_HOST)

class CheckServer(object):
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
    
    def offsale_update(self, muri):
        _id = muri.rsplit('/', 2)[-2]
        utcnow = datetime.utcnow()
        var = api.product(_id).get()
        if 'ends_at' in var and var['ends_at'] > utcnow.isoformat():
            api.product(_id).patch({ 'ends_at': utcnow.isoformat() })
        if 'ends_at' not in var:
            api.product(_id).patch({ 'ends_at': utcnow.isoformat() })

    def check_onsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nruelala {0}, {1}\n\n'.format(id, url)
            return

        ret = self.s.get(url)
        if ret.url == 'http://www.ruelala.com/event':
            if prd.muri:
                self.offsale_update(prd.muri)
            if not prd.products_end or prd.products_end > datetime.utcnow():
                prd.products_end = datetime.utcnow()
                prd.update_history.update({ 'products_end': datetime.utcnow() })
                prd.save()
            return -302
        if ret.url == 'http://www.ruelala.com/common/errorGeneral':
            if prd.muri:
                self.offsale_update(prd.muri)
            if not prd.products_end or prd.products_end > datetime.utcnow():
                prd.products_end = datetime.utcnow()
                prd.update_history.update({ 'products_end': datetime.utcnow() })
                prd.save()
            return -302
        cont = ret.content
        tree = lxml.html.fromstring(cont)
        try:
            title = tree.cssselect('h2#productName')[0].text_content().strip()
            if title.lower() != prd.title.lower():
                print 'ruelala product[{0}] title error: [{1}, {2}]'.format(prd.combine_url, prd.title.encode('utf-8'), title.encode('utf-8'))
        except IndexError:
            print '\n\n ruelala product[{0}] title not extract right. return url: {1}\n\n'.format(prd.combine_url, ret.url)

        try:
            listprice = tree.cssselect('span#strikePrice')[0].text_content().strip()
            if listprice != prd.listprice:
                print 'ruelala product[{0}] listprice error: [{1}, {2}]'.format(prd.combine_url, prd.listprice, listprice)
        except IndexError:
            print '\n\n ruelala product[{0}] listprice error. {1}'.format(prd.combine_url, ret.url)
        price = tree.cssselect('span#salePrice')[0].text_content().strip()
        soldout = tree.cssselect('span#inventoryAvailable')
        if price != prd.price:
            print 'ruelala product[{0}] price error: [{1}, {2}]'.format(prd.combine_url, prd.price, price)

    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

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
    CheckServer().check_onsale_product()
