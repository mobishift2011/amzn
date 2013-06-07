import requests
import re
import json
import lxml.html

from models import Product
from server import giltLogin
""" gilt not need to login ,
    but the price is not right when we access it from China
"""

class CheckServer(object):
    def __init__(self):
        self.headers = {
            'Cookie': 'optimizelyEndUserId=oeu1351495981434r0.0753983361646533; sid=z_20121121_020756_116.231.107.183_63_32_94; csrf=npatkkwelh72vzlm3apmylxnmhxg4zlv3ey7hh3l; JSESSIONID=1xcr2rh2fsk4p1ma3q33xiqkkh; guid=4b5a82d59566f78b2f7b5a45e690e73b34094d1842e31e3463628e3cd4b551bc_f2fc40a5-afb9-4dc6-90ea-986bcf1cf7c1; ca=3a4b38cc87d1aa9aa19cc63ca796b459c82442bdc6ce44f014210c9e56efd6c1_m.0.1.; gender=f; cp=428; test_bucket=996; test_bucket_id=753501140521019148; optimizelySegments=%7B%7D; optimizelyBuckets=%7B%22137351109%22%3A%22137342151%22%2C%22138556151%22%3A%22138479831%22%2C%22141164996%22%3A%22141243248%22%7D; store=home; __utma=170966838.1464646229.1351495984.1354499825.1354520369.10; __utmb=170966838.2.8.1354523121878; __utmc=170966838; __utmz=170966838.1354334621.7.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=170966838.|1=GUID=f2fc40a5-afb9-4dc6-90ea-986bcf1cf7c1=1^2=Partition=428=1^9=gender=female=1^12=Variant=login_reg_regwall%3Dmosaic%7Clogin_reg_modal%3Dinternational%7Cloyalty_test%3DUNKNOWN%2Ffalse%2Ffalse=1^24=Visitor%20ID=v_20121029_153303_76_81_38=1; NRAGENT=tk=fbd7760aefe06ca4'}
        self.s = requests.session()

    def get_correct_tree(self, cont):
        """.. :py:method::
        :param cont: page content
        :rtype: right xml tree
        """
        end_html_position = cont.find('</html>')
        if len(cont) - end_html_position > 200:
            tree = lxml.html.fromstring(cont[:end_html_position] + cont[end_html_position+7:])
        else:
            tree = lxml.html.fromstring(cont)
        return tree

    def check_onsale_product(self, id, url):
#        prd = Product.objects(key=id).first()
#        if prd is None:
#            print '\n\ngilt {0}, {1}\n\n'.format(id, url)
#            return

        ret = self.s.get(url, headers=self.headers)
        tree = self.get_correct_tree(ret.content)
        if '/home/sale' in url or '/sale/home' in url: # home
            node = tree.cssselect('div.content-container div.positions div.elements-container article.product-full section.product-details')[0]
            brand = node.cssselect('h3.product-brand')[0].text_content()
            title = node.cssselect('h1.product-name')[0].text_content()
            soldout = True if node.cssselect('form.sku-selection div.actions p.secondary-action a') else False

            listprice = node.cssselect('div.product-price div.original-price')
            listprice = listprice[0].text_content().replace('$', '').replace(',', '').strip() if listprice else ''
            if listprice and \
                        ('-' in listprice or '-' in prd.listprice) and \
                        prd.listprice.replace('$', '').replace(',', '').strip() != listprice:

                print 'gilt product[{0}] listprice {1} vs {2}'.format(url, prd.listprice.replace('$', '').replace(',', '').strip(), listprice)
                prd.listprice = listprice
                prd.update_history.update({ 'listprice': datetime.utcnow() })
                prd.save()
            elif listprice and '-' not in listprice and \
                            '-' not in prd.listprice and \
                            float(prd.listprice.replace('$', '').replace(',', '').strip()) != float(listprice):
                print 'gilt product[{0}] listprice error: [{1}, {2}]'.format(url, prd.listprice.replace('$', '').replace(',', '').strip(), listprice)
                prd.listprice = listprice
                prd.update_history.update({ 'listprice': datetime.utcnow() })
                prd.save()

            price = node.cssselect('div.product-price div.gilt-price')[0].text_content().replace('$', '').replace('Gilt', '').replace(',', '').strip()
            if ('-' in price or '-' in prd.price) and \
                    prd.price.replace('$', '').replace('Gilt', '').replace(',', '').strip() != price:
                print 'gilt product[{0}] price {1} vs {2}'.format(url, prd.price.replace('$', '').replace('Gilt', '').replace(',', '').strip(), price)
                prd.price = price
                prd.update_history.update({ 'price': datetime.utcnow() })
                prd.save()
            elif '-' not in price and \
                    '-' not in prd.price and \
                    float(prd.price.replace('$', '').replace('Gilt', '').replace(',', '').strip()) != float(price):
                print 'gilt product[{0}] price error: [{1}, {2}]'.format(url, prd.price.replace('$', '').replace('Gilt', '').replace(',', '').strip(), price)
                prd.price = price
                prd.update_history.update({ 'price': datetime.utcnow() })
                prd.save()

            if prd.title.lower() != title.lower():
                print 'gilt product[{0}] title error: [{1}, {2}]'.format(url, prd.title.encode('utf-8').lower(), title.encode('utf-8').lower())
            if prd.soldout != soldout:
                print 'gilt product[{0}] soldout error: [{1}, {2}]'.format(url, prd.soldout, soldout)
                prd.soldout = soldout
                prd.update_history.update({ 'soldout': datetime.utcnow() })
                prd.save()

        else: # women, men, children
            node = tree.cssselect('section#details section.summary')[0]
            title = node.cssselect('header.overview h1.product-name')[0].text_content().strip()
            try:
                brand = node.cssselect('header.overview h2.brand-name .brand-name-text')[0].text_content().strip()
            except IndexError:
                print '\n\ngilt brand {0} \n\n'.format(url)

            listprice = node.cssselect('header.overview div.price div.original-price span.msrp')
            listprice = listprice[0].text_content().replace('$', '').replace(',', '').strip() if listprice else ''
            if listprice and \
                    ('-' in listprice or '-' in prd.listprice) and \
                    prd.listprice.replace('$', '').replace(',', '').strip() != listprice:
                print 'gilt product[{0}] listprice {1} vs {2}'.format(url, prd.listprice.replace('$', '').replace(',', '').strip(), listprice)
                prd.listprice = listprice
                prd.update_history.update({ 'listprice': datetime.utcnow() })
                prd.save()
            elif listprice and \
                    '-' not in listprice and \
                    '-' not in prd.listprice and \
                    float(prd.listprice.replace('$', '').replace(',', '').strip()) != float(listprice):
                print 'gilt product[{0}] listprice error: [{1}, {2}]'.format(url, prd.listprice.replace('$', '').replace(',', '').strip(), listprice)
                prd.listprice = listprice
                prd.update_history.update({ 'listprice': datetime.utcnow() })
                prd.save()

            price = node.cssselect('header.overview div.price div.sale-price span.nouveau-price')[0].text_content().replace('$', '').replace(',', '').strip()
            if ('-' in price or '-' in prd.price) and \
                    prd.price.replace('$', '').replace(',', '').strip() != price:
                print 'gilt product[{0}] price {1} vs {2}'.format(url, prd.price.replace('$', '').replace(',', '').strip(), price)
                prd.price = price
                prd.update_history.update({ 'price': datetime.utcnow() })
                prd.save()
            elif '-' not in price and \
                    '-' not in prd.price and \
                    float(prd.price.replace('$', '').replace(',', '').strip()) != float(price):
                print 'gilt product[{0}] price error: [{1}, {2}]'.format(url, prd.price.replace('$', '').replace(',', '').strip(), price)
                prd.price = price
                prd.update_history.update({ 'price': datetime.utcnow() })
                prd.save()

            if prd.title.lower() != title.lower():
                print 'gilt product[{0}] title error: [{1}, {2}]'.format(url, prd.title.encode('utf-8').lower(), title.encode('utf-8').lower())
#            if prd.soldout != soldout:
#                print 'gilt product[{0}] soldout error: [{1}, {2}]'.format(url, prd.soldout, soldout)
#                prd.soldout = soldout
#                prd.update_history.update({ 'soldout': datetime.utcnow() })
#                prd.save()



    def check_offsale_product(self, id, url):
        pass

    def check_onsale_event(self, id, url):
        pass

    def check_offsale_event(self, id, url):
        pass


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
    CheckServer().check_onsale_product('142260201-hiho-batik-mom-onesie-2-pack', 'http://www.gilt.com/brand/hiho-batik/product/142260201-hiho-batik-mom-onesie-2-pack')
