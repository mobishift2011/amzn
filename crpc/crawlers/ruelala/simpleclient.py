import requests
import lxml.html
import re

test_url = 'http://www.ruelala.com/event/product/61521/1111946014/0/DEFAULT'

class Ruelala(object):
    def __init__(self):
        self.s = requests.session()
        self.headers = {
            'Cooki': 'X-CCleaned=1; optimizelyEndUserId=oeu1349667187777r0.2759982226275626; optimizelyBuckets=%7B%7D; CoreID6=87382265939413496671878&ci=90210964; userEmail=huanzhu@favbuy.com; optimizelySegments=%7B%7D; symfony=k403lo7sq5qmbfg9t0nj4gips2; aid=1001; NSC_SVF_QPPM_BMM_OPDBDIF=ffffffff096c9d3e45525d5f4f58455e445a4a423660',
        }
    
    def get_product_abstract_by_url(self, url):
        content = self.s.get(url, headers=self.headers).content
        product_id = re.compile(r'/product/(\d+)').search(url).group(1)
        t = lxml.html.fromstring(content)
        title = t.xpath('//*[@id="productName"]')[0].text
        description = ''
        for li in t.xpath('//*[@id="info"]/ul/li'):
            description += li.text_content() + '\n'
        return 'ruelala_'+product_id, title+'_'+description

if __name__ == '__main__':
    print Ruelala().get_product_abstract_by_url(test_url)
