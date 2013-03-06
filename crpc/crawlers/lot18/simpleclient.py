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
        self.soldout = re.compile('<p class="main">.*sold out.*</p>')
        self.title = re.compile('<div class="product-info product-name">\s*<h1>(.*)</h1>\s*</div>')
    
    def check_onsale_product(self, id, url):
        ret = self.net.fetch_page(prd.combine_url)
        if isinstance(ret, int):
            ret = self.net.fetch_page(prd.combine_url)
            if isinstance(ret, int): continue
        soldout = True if self.soldout.search(ret) else False
        title = self.title.search(ret).group(1)


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
