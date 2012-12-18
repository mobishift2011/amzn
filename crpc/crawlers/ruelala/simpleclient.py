import requests
import lxml.html
import re

test_url = 'http://www.ruelala.com/event/product/63747/1111937972/0/DEFAULT'

class Ruelala(object):
    def __init__(self):
        self.s = requests.session()
        self.login_url = 'http://www.ruelala.com/access/gate'
        self.s.get(self.login_url)
        self.s.post('http://www.ruelala.com/access/formSetup', data={'userEmail':'','CmsPage':'/access/gate','formType':'signin'})
        self.data = {
            'email': '2012luxurygoods@gmail.com',
            'password': 'abcd1234',
            'loginType': 'gate',
            'rememberMe': 1, 
        }       
        self.s.post('https://www.ruelala.com/registration/login', data=self.data)
    
    def get_product_abstract_by_url(self, url):
        content = self.s.get(url).content
        product_id = re.compile(r'/product/(\d+)').search(url).group(1)
        t = lxml.html.fromstring(content)
        title = t.xpath('//*[@id="productName"]')[0].text
        description = ''
        for li in t.xpath('//*[@id="info"]/ul/li'):
            description += li.text_content() + '\n'
        return 'ruelala_'+product_id, title+'_'+description

if __name__ == '__main__':
    print Ruelala().get_product_abstract_by_url(test_url)
