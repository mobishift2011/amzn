import requests
import lxml.html
import re
import slumber
from datetime import datetime

from settings import MASTIFF_HOST
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

api = slumber.API(MASTIFF_HOST)

class CheckServer(object):
    def __init__(self):
        self.s = requests.session()
        self.headers = {
        }
    
    def check_onsale_product(self, id, url):
        prd = Product.objects(key=id).first()
        if prd is None:
            print id, url
            return
        ret = self.s.get(url, headers=self.headers)
        if ret.url == u'https://www.onekingslane.com/':
            return -302
        tree = lxml.html.fromstring(ret.content)
        already_end = True if tree.cssselect('#productOverview div.expired') else False
        if already_end:
            # api.product(umi).patch({'ends_at': datetime.utcnow()})
            return False
        try:
            title = tree.cssselect('#productOverview h1.serif')[0].text_content().strip()
            if prd.title.lower() != title.lower():
                print 'onekingslane product[{0}] title error: [{1}, {2}]'.format(prd.combine_url, title.encode('utf-8'), prd.title.encode('utf-8'))
            if not prd.title:
                prd.title = title
                prd.update_history.update({ 'title': datetime.utcnow() })
                prd.save()
        except IndexError:
            print '\n\nonekingslane product[{0}] title label can not get it.\n\n'.format(url)
        except AttributeError:
            print '\n\nonekingslane product[{0}] title None not get it.\n\n'.format(url)

        img = tree.cssselect('div#productDescription > div#altImages')
        if img:
            for i in img[0].cssselect('img.altImage'):
                img_url = i.get('data-altimgbaseurl') + '?$fullzoom$'
                if img_url not in prd.image_urls:
                    prd.image_urls.append(img_url)
                    prd.update_history.update({ 'image_urls': datetime.utcnow() })
            prd.save()

        try:
            price = tree.cssselect('p#oklPriceLabel')[0].text_content().replace('Our Price', '').strip()
        except IndexError:
            print '\n\nonekingslane product[{0}] price label can not get.\n\n'.format(url)

        listprice = tree.cssselect('p#msrpLabel')[0].text_content().replace('Retail', '').replace('Estimated Market Value', '').strip()
        if '-' not in price:
            if float( price.replace('$', '').replace(',', '') ) != float( prd.price.replace('Our Price', '').replace('$', '').replace(',', '') ):
                print 'onekingslane product[{0}] price error: {1} vs {2}'.format(prd.combine_url, price, prd.price)
        if '-' not in listprice and listprice:
            if float( listprice.replace('$', '').replace(',', '') ) != float( prd.listprice.replace('$', '').replace(',', '') ):
                print 'onekingslane product[{0}] listprice error: {1} vs {2}'.format(prd.combine_url, listprice, prd.listprice)

        soldout = True if tree.cssselect('.sold-out') else False
        if soldout !=  prd.soldout:
            print 'onekingslane product[{0}] soldout error: {1} vs {2}'.format(prd.combine_url, soldout, prd.soldout)

        return True



    def check_offsale_product(self, url, id):
        ret = self.s.get(url, headers=self.headers)
        tree = lxml.html.fromstring(ret.content)
        already_end = True if tree.cssselect('#productOverview div.expired') else False
        if already_end:
            return True
        else:
            return False


    def check_offsale_event(self, url, id):
        ret = self.s.get(url, headers=self.headers)
        tree = lxml.html.fromstring(ret.content)
        text = tree.cssselect('div#okl-content div.sales-event')[0].get('class')
        if 'ended' in text:
            return True
        if 'started' in text:
            return False


    def test_product(self, testurl):
        ret = self.s.get(testurl, headers=self.headers)
        tree = lxml.html.fromstring(ret.content)
        title = tree.cssselect('#productOverview h1.serif')[0].text_content().strip()
        print title

    def test_event(self, testurl):
        ret = self.s.get(testurl, headers=self.headers)
        tree = lxml.html.fromstring(ret.content)
        text = tree.cssselect('div#okl-content div.sales-event')[0].get('class')
        print text


    def get_product_abstract_by_url(self, url):
        product_id = re.compile(r'/product/\d+/(\d+)').search(url).group(1)
        content = self.s.get(url, headers=self.headers).content
        t = lxml.html.fromstring(content)
        title = t.xpath('//html/head/title')[0].text.encode('utf-8')
        description = t.xpath('//*[@id="description"]/p')[0].text.encode('utf-8')
        return 'onekingslane_'+product_id, title+'_'+description

if __name__ == '__main__':
    import sys
    from optparse import OptionParser

    parser = OptionParser(usage='usage: %prog [options]')
    parser.add_option('-e', '--event', dest='event', action='store_true', help='check event off sale whether still on', default=False)
    parser.add_option('-p', '--product', dest='product', action='store_true', help='check product off sale whether still on', default=False)
    parser.add_option('-c', '--check', dest='check', action='store_true', help='check on sale product whether off sale', default=False)
    parser.add_option('-d', '--daemon', dest='daemon', action='store_true', help='run as a rpc server', default=False)

    if len(sys.argv) == 1:
        parser.print_help()
        exit()

    onekingslane = CheckServer()
    options, args = parser.parse_args(sys.argv[1:])
    if options.daemon:
        pass
    elif options.event:
        onekingslane.check_offsale_event()
    elif options.product:
        onekingslane.check_offsale_product()
    elif options.check:
        onekingslane.check_onsale_product()
    else:
        parser.print_help()
