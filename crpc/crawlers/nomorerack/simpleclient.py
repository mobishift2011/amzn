import requests
import lxml.html
import re

from crawlers.common.stash import time_convert
from models import Product, Event
from server import req, fetch_product_page


class CheckServer(object):
    def __init__(self):
        self.s = requests.session()
        self.headers = {}
    
    def parse_time(self, tree):
        ends = tree.cssselect('div#wrapper > div#content > div#front > div.ribbon > div.ribbon-center h4')
        if not ends:
            ends = tree.cssselect('div#wrapper > div#content > div#front > div.top > div.ribbon-center > p')
            end = ends[0].text_content()
            if not end:
                end = ends[-1].text_content()
            ends = end 
        else:
            ends = ends[0].text_content()
        ends = ends.split('until')[-1].strip().replace('st', '').replace('nd', '').replace('rd', '').replace('th', '') 
        time_str, time_zone = ends.rsplit(' ', 1)

        if len(time_str.split(' ')) == 3:
            time_format = '%B %d %I:%M%p%Y'
        elif len(time_str.split(' ')) == 4:
            time_format = '%B %d %I:%M %p%Y'

        try:
            products_end = time_convert(time_str, time_format, time_zone)
        except ValueError:
            if len(time_str.split(' ')) == 3:
                a, b, c = time_str.split(' ')
                if c[:2] == '00' and c[5] == 'A':
                    products_end = time_convert(time_str.replace('AM', ' '), '%B %d %H:%M %Y', time_zone)
                elif int(c[:2]) >=13 and c[5] == 'P':
                    products_end = time_convert(time_str.replace('PM', ' '), '%B %d %H:%M %Y', time_zone)
            elif len(time_str.split(' ')) == 4:
                a, b, c, d = time_str.split(' ')
                if c[:2] == '00' and d[0] == 'A':
                    products_end = time_convert(time_str.replace('AM', ''), '%B %d %H:%M %Y', time_zone)
                elif int(c[:2]) >=13 and d[0] == 'P':
                    products_end = time_convert(time_str.replace('PM', ''), '%B %d %H:%M %Y', time_zone)
        return datetime(products_end.year, products_end.month, products_end.day, products_end.hour, products_end.minute)


    def check_onsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nnomorerack {0}, {1}\n\n'.format(id, url)
            return
        cont = fetch_product_page(url)
        if isinstance(cont, int):
            print '\nnomorerack on sale page[{0}] return: {1}\n'.format(url, cont)
            return
        tree = lxml.html.fromstring(cont)
        node = tree.cssselect('div#content div#front div#primary div#products_view div.right')[0]
        title = node.cssselect('div h2')[0].text_content()
        price_node = node.cssselect('div.add_to_cart div.offer_method div.standard')[0]
        
        try:
            price = price_node.cssselect('h3 span[data-issw-price-value]')[0].text_content().replace('$', '').replace(',', '').strip()
        except:
            return
        listprice = price_node.cssselect('p del')[0].text_content().replace('$', '').replace(',', '').replace('Retail', '').strip()
        soldout = node.cssselect('div.add_to_cart div#add_to_cart div.error_message')
        soldout = 'out' in soldout[0].text_content() if soldout else False
        products_end = self.parse_time(tree)

        if prd.title.lower() != title.lower():
            print 'nomorerack product[{0}] title error: [{1} vs {2}]'.format(url, prd.title.encode('utf-8'), title.encode('utf-8'))
        if float(prd.price.replace('$', '').replace(',', '').strip()) != float(price):
            print 'nomorerack product[{0}] price error: [{1} vs {2}]'.format(url, prd.price, price)
        if float(prd.listprice.replace('$', '').replace(',', '').replace('Retail', '').strip()) != float(listprice):
            print 'nomorerack product[{0}] listprice error: [{1} vs {2}]'.format(url, prd.listprice, listprice)
        if prd.products_end != products_end:
            print 'nomorerack product[{0}] products_end error: [{1} vs {2}]'.format(url, prd.products_end, products_end)
        


    def check_offsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print '\n\nnomorerack {0}, {1}\n\n'.format(id, url)
            return

        cont = fetch_product_page(url)
        if isinstance(cont, int):
            print '\nnomorerack off sale page[{0}] return: {1}\n'.format(url, cont)
            return
        tree = lxml.html.fromstring(cont)
        offsale = tree.cssselect('div#content div#front div#primary div#products_view div.right div.add_to_cart div#add_to_cart div.error_message')[0].text_content()
        offsale = 'not available' in offsale
        products_end = self.parse_time(tree)
        if prd.products_end != products_end:
            print 'nomorerack product[{0}] products_end error: [{1} vs {2}]'.format(url, prd.products_end, products_end)


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
