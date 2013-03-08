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
        price_node = node.cssselect('div.add_to_cart div.offer_method div.standard')[0]
        price = price_node.cssselect('h3 span.data-issw-price-value')[0].text_content().replace('$', '').replace(',', '')
        listprice = price_node.cssselect('p del')[0].text_content().replace('$', '').replace(',', '').replace('Retail', '')
        soldout = node.cssselect('div.add_to_cart div#add_to_cart div.error_message span')
        soldout = 'out' in soldout[0].text_content() if soldout else False

        if prd.title.lower() != title.lower():
            print 'nomorerack product[{0}] title error: [{1} vs {2}]'.format(url, prd.title.encode('utf-8'), title.encode('utf-8'))
        if float(prd.price) != float(price):
            print 'nomorerack product[{0}] price error: [{1} vs {2}]'.format(url, prd.price, price)
        if float(prd.listprice) != float(listprice):
            print 'nomorerack product[{0}] listprice error: [{1} vs {2}]'.format(url, prd.listprice, listprice)
        


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
