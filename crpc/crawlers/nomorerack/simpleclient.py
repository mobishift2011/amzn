import requests
import lxml.html
import re

test_url = 'http://www.nomorerack.com/daily_deals/view/169709-burberry_brit_eau_de_parfum_for_women'

class Nomorerack(object):
    def __init__(self):
        self.s = requests.session()
        self.headers = {}
    
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
    print Nomorerack().get_product_abstract_by_url(test_url)
