import requests
import lxml.html
import re
from datetime import datetime
from models import Event, Product

from requests.packages.urllib3.connectionpool import *
import ssl
def connect_vnew(self):
    # Add certificate verification
    sock = socket.create_connection((self.host, self.port), self.timeout)

    # Wrap socket using verification with the root certs in
    # trusted_root_certs
    self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file,
                                cert_reqs=self.cert_reqs,
                                ca_certs=self.ca_certs,
                                ssl_version=ssl.PROTOCOL_TLSv1)
    if self.ca_certs:
        match_hostname(self.sock.getpeercert(), self.host)

VerifiedHTTPSConnection.connect = connect_vnew


class Onekingslane(object):
    def __init__(self):
        self.s = requests.session()
        self.headers = {
        }
    
    def check_product_right(self):
        utcnow = datetime.utcnow()
        obj = Product.objects(products_end__gt=utcnow).timeout(False)
        print 'Onekingslane have {0} products.'.format(obj.count())

        end_count = 0
        for prd in obj:
            ret = self.s.get(prd.combine_url, headers=self.headers)
            tree = lxml.html.fromstring(ret.content)
            already_end = True if tree.cssselect('#productOverview div.expired') else False
            if already_end:
                end_count += 1
                continue
            try:
                title = tree.cssselect('#productOverview h1.serif')[0].text_content().strip()
                if prd.title.lower() != title.lower():
                    print 'onekingslane product[{0}] title error: [{1}, {2}]'.format(prd.combine_url, title.encode('utf-8'), prd.title.encode('utf-8'))
            except IndexError:
                print '\n\nonekingslane product[{0}] title label can not get it.\n\n'.format(prd.combine_url)
            except AttributeError:
                print '\n\nonekingslane product[{0}] title None not get it.\n\n'.format(prd.combine_url)

            price = tree.cssselect('p#oklPriceLabel')[0].text_content().replace('Our Price', '').strip()
            listprice = tree.cssselect('p#msrpLabel')[0].text_content().replace('Retail', '').replace('Estimated Market Value', '').strip()
            if '-' not in price:
                if float( price.replace('$', '').replace(',', '') ) != float( prd.price.replace('Our Price', '').replace('$', '').replace(',', '') ):
                    print 'onekingslane product[{0}] price error: {1} vs {2}'.format(prd.combine_url, price, prd.price)
            if '-' not in listprice:
                if float( listprice.replace('$', '').replace(',', '') ) != float( prd.listprice.replace('$', '').replace(',', '') ):
                    print 'onekingslane product[{0}] listprice error: {1} vs {2}'.format(prd.combine_url, listprice, prd.listprice)

            soldout = True if tree.cssselect('.sold-out') else False
            if soldout !=  prd.soldout:
                print 'onekingslane product[{0}] soldout error: {1} vs {2}'.format(prd.combine_url, soldout, prd.soldout)
        print 'onekingslane have {0} products end.'.format(end_count)

    def check_end_product_still_on(self):
        utcnow = datetime.utcnow()
        obj = Product.objects(products_end__lt=utcnow).timeout(False)
        print 'Onekingslane have {0} products end.'.format(obj.count())

        stillon_count = 0
        for prd in obj:
            ret = self.s.get(prd.combine_url, headers=self.headers)
            tree = lxml.html.fromstring(ret.content)
            already_end = True if tree.cssselect('#productOverview div.expired') else False
            if not already_end:
                stillon_count += 1
        print 'onekingslane have {0} products still on.'.format(stillon_count)


    def check_end_event_still_on(self):
        utcnow = datetime.utcnow()
        obj = Product.objects(events_end__lt=utcnow).timeout(False)
        print 'Onekingslane have {0} events end.'.format(obj.count())

    def get_product_abstract_by_url(self, url):
        product_id = re.compile(r'/product/\d+/(\d+)').search(url).group(1)
        content = self.s.get(url, headers=self.headers).content
        t = lxml.html.fromstring(content)
        title = t.xpath('//html/head/title')[0].text.encode('utf-8')
        description = t.xpath('//*[@id="description"]/p')[0].text.encode('utf-8')
        return 'onekingslane_'+product_id, title+'_'+description

if __name__ == '__main__':
    Onekingslane().check_product_right()
    Onekingslane().check_end_product_still_on()
