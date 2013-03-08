import requests
import lxml.html
import re

from server import req, fetch_product_page


class CheckServer(object):
    def __init__(self):
        self.s = requests.session()
        self.headers = {}
    
    def check_onsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nnomorerack {0}, {1}\n\n'.format(id, url)
            return
        cont = fetch_product_page(url)
        if isinstance(cont, int):
            return
        tree = lxml.html.fromstring(cont)
        node = tree.cssselect('div#content div#front div#primary div#products_view div.right')[0]
        title = node.cssselect('div h2')[0].text_content()
        price = node.cssselect('')
        


    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass

    def get_product_abstract_by_url(self, url):
        content = self.s.get(url, headers=self.headers).content
        product_id = re.compile(r'/view/(\d+)').search(url).group(1)
        t = lxml.html.fromstring(content)
        title = t.xpath('//*[@id="products_view"]//h2')[0].text.encode('utf-8')
        description = []
        for desc in t.xpath('//*[@id="products_view"]//*[@class="description"]'):
            description.append(desc.text_content().encode('utf-8'))
        description = '\n'.join(description)
        return 'nomorerack_'+product_id, title+'_'+description

if __name__ == '__main__':
    CheckServer()
