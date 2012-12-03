import requests
import re
import json

test_url = 'http://www.gilt.com/sale/women/kate-spade-new-york-handbags-5860/product/168155147-kate-spade-new-york-signature-spade-leather-roxanns-satchel'
test_url = 'http://www.gilt.com/home/sale/kate-spade-5571/143776857-kate-spade-new-york-bedding-piedmont-park-flat-sheet'

class Gilt(object):
    def __init__(self):
        self.headers = {
            'Cookie': 'optimizelyEndUserId=oeu1351495981434r0.0753983361646533; sid=z_20121121_020756_116.231.107.183_63_32_94; csrf=npatkkwelh72vzlm3apmylxnmhxg4zlv3ey7hh3l; JSESSIONID=1xcr2rh2fsk4p1ma3q33xiqkkh; guid=4b5a82d59566f78b2f7b5a45e690e73b34094d1842e31e3463628e3cd4b551bc_f2fc40a5-afb9-4dc6-90ea-986bcf1cf7c1; ca=3a4b38cc87d1aa9aa19cc63ca796b459c82442bdc6ce44f014210c9e56efd6c1_m.0.1.; gender=f; cp=428; test_bucket=996; test_bucket_id=753501140521019148; optimizelySegments=%7B%7D; optimizelyBuckets=%7B%22137351109%22%3A%22137342151%22%2C%22138556151%22%3A%22138479831%22%2C%22141164996%22%3A%22141243248%22%7D; store=home; __utma=170966838.1464646229.1351495984.1354499825.1354520369.10; __utmb=170966838.2.8.1354523121878; __utmc=170966838; __utmz=170966838.1354334621.7.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=170966838.|1=GUID=f2fc40a5-afb9-4dc6-90ea-986bcf1cf7c1=1^2=Partition=428=1^9=gender=female=1^12=Variant=login_reg_regwall%3Dmosaic%7Clogin_reg_modal%3Dinternational%7Cloyalty_test%3DUNKNOWN%2Ffalse%2Ffalse=1^24=Visitor%20ID=v_20121029_153303_76_81_38=1; NRAGENT=tk=fbd7760aefe06ca4'}
        self.s = requests.session()

    def get_product_abstract_by_url(self, url):
        content = self.s.get(url, headers=self.headers).content
        product_id = re.compile(r'/(\d+)-').search(url).group(1)
        try:
            product_info = re.compile(r'product.init\((.*?)[\)]+;').search(content).group(1) 
        except:
            product_info = re.compile(r'new Gilt.Product\((.*?)[\)]+;').search(content).group(1) 
        product_info = json.loads(product_info)
        title = product_info['name'].encode('utf-8')
        description = product_info['description'].replace('<br>','\n').encode('utf-8')
        return 'gilt_'+product_id, title+'\n'+description

if __name__ == '__main__':
    print Gilt().get_product_abstract_by_url(test_url)
