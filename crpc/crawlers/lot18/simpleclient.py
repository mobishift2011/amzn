import requests
import lxml.html
import re

test_url = 'http://www.lot18.com/product/3455/2006-caraccioli-brut-cuvee-sparkling-wine-half-case'

class Lot18(object):
    def __init__(self):
        self.s = requests.session()
        self.headers = {}
    
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
    print Lot18().get_product_abstract_by_url(test_url)
