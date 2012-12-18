import requests
import lxml.html
import re

test_url = 'https://www.onekingslane.com/product/17994/1040115'

class Onekingslane(object):
    def __init__(self):
        self.s = requests.session()
        self.headers = {
        }
    
    def get_product_abstract_by_url(self, url):
        product_id = re.compile(r'/product/\d+/(\d+)').search(url).group(1)
        content = self.s.get(url, headers=self.headers).content
        t = lxml.html.fromstring(content)
        title = t.xpath('//html/head/title')[0].text.encode('utf-8')
        description = t.xpath('//*[@id="description"]/p')[0].text.encode('utf-8')
        return 'onekingslane_'+product_id, title+'_'+description

if __name__ == '__main__':
    print Onekingslane().get_product_abstract_by_url(test_url)
