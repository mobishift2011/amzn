import requests
import re
import json

test_url = 'http://www.gilt.com/sale/women/kate-spade-new-york-handbags-5860/product/168155147-kate-spade-new-york-signature-spade-leather-roxanns-satchel'

class Gilt(object):
    def __init__(self):
        self.s = requests.session()

    def get_product_abstract_by_url(self, url):
        content = self.s.get(url).content
        product_id = re.compile(r'/(\d+)-').search(url).group(1)
        product_info = re.compile(r'new Gilt.Product\((.*?)[\)]+;').search(content).group(1) 
        product_info = json.loads(product_info)
        title = product_info['name'].encode('utf-8')
        description = product_info['description'].replace('<br>','\n').encode('utf-8')
        return title.replace(' ','_')+'_'+product_id, title+'\n'+description

if __name__ == '__main__':
    print Gilt().get_product_abstract_by_url(test_url)
        
        
