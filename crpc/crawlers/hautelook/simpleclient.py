
import requests
import json
import lxml.html
import re
from models import *
from datetime import datetime


class Hautelook(object):
    def __init__(self):
        self.s = requests.session()
        self.headers = {
    'Accept': 'application/json',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,en-US;q=0.8,en;q=0.6',
    'Auth': 'HWS a5a4d56c84b8d8cd0e0a0920edb8994c',
    'Connection': 'keep-alive',
    'Content-encoding': 'gzip,deflate',
    'Content-type': 'application/json',
    'Cookie': 'optimizelyEndUserId=oeu1350285726316r0.5169918085448444; __qca=P0-1890885822-1350285726392; __cmbU=ABJeb18pexM6zxLcBNYFAG2RtVmsY0OJJ1X30i1K3_w0XcFchGbjG21B-RCIPImbtplSyNQe2elLJ9Fv7P7bvqId-MoIKwl-EQ; hlo[mType]=Member; __ar_v4=%7CNZUMLDQBFJBCDJO5RYMUQ4%3A20130006%3A1%7C5KKAPNHCHZEFVNM564VIHM%3A20130006%3A1%7C5OCYHSCF4FFDXA7XMFQMH3%3A20130006%3A1; RETURN_URL=/product/6766649; PHPSESSID=abq8qdf4hs0epurl1dq5fc3fp3; hlmt=50cee9b736e9a; hlma=d74fdfcc5968fdc58a5f8348b11cdc19; HLMEMBER=1; gaCamp[member_id]=11147317; gaCamp[sid]=100; __cmbDomTm=0; __cmbTpvTm=790; __cmbCk={"tp":22443}|{"tp":5525}; optimizelySegments=%7B%7D; optimizelyBuckets=%7B%7D; optimizelyPendingLogEvents=%5B%5D; __utma=116900255.704923198.1350285726.1355737613.1355743800.16; __utmb=116900255.5.10.1355743800; __utmc=116900255; __utmz=116900255.1354947514.14.9.utmcsr=localhost:1321|utmccn=(referral)|utmcmd=referral|utmcct=/validate/; __utmv=116900255.|5=User%20ID=11147317=1; s_sess=%20s_cc%3Dtrue%3B%20s_sq%3D%3B; s_vi=[CS]v1|283DDCBC851D1261-40000129C018C5EF[CE]; hauteLookMember=%7B%22member_id%22%3A11147317%2C%22first_name%22%3A%22helena%22%2C%22last_name%22%3A%22rak%22%2C%22invitation_code%22%3A%22hrak981%22%2C%22role%22%3A1%2C%22gender%22%3A%22F%22%2C%22email%22%3A%222012luxurygoods@gmail.com%22%2C%22msa%22%3A%22New%20York-Northern%20New%20Jersey-Long%20Island%20NY-NJ-PA%22%2C%22credits%22%3A%220.00%22%2C%22cart_count%22%3A0%2C%22category_order%22%3A%5B%5D%2C%22join_date%22%3A%222012-12-07T00%3A49%3A56-08%3A00%22%2C%22meta%22%3A%7B%22promos%22%3A%5B%5D%7D%2C%22timezone%22%3A%22PST%22%2C%22cart%22%3A0%7D; og=F; cartStamp=nRR0Zf9; stop_mobi=yes',
    'Host': 'www.hautelook.com',
    'Referer': 'http://www.hautelook.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Ubuntu/12.10 Chromium/22.0.1229.94 Chrome/22.0.1229.94 Safari/537.4',
    'X-Requested-With': 'XMLHttpRequest',
        }
    
    def check_product_right(self):
        utcnow = datetime.utcnow()
        obj = Product.objects(products_end__gt=utcnow).timeout(False)
        print 'Hautelook have {0} products.'.format(obj.count())

        for prd in obj:
            ret = self.s.get('http://www.hautelook.com/v2/product/{0}'.format(prd.key), headers=self.headers)
            try:
                js = json.loads(ret.content)
            except ValueError:
                print 'hautelook request return error[{0}]'.format(prd.combine_url)
                continue
            if not prd.title:
                print 'hautelook product[{0}] title not exist'.format(prd.combine_url)
            elif prd.title.lower() != js['data']['title'].lower():
                print 'hautelook product[{0}] title error: {1} vs {2}'.format(prd.combine_url, js['data']['title'], prd.title)
            if js['data']['event_display_brand_name']:
                if js['data']['event_title'] != js['data']['brand_name']:
                    if prd.brand != js['data']['brand_name']:
                        print 'hautelook product[{0}] brand error: {1} vs {2}'.format(prd.combine_url, js['data']['brand_name'], prd.brand)

            data = js['data']
            color, price, listprice = '', '', ''
            # same product with different colors, all in the same product id
            price_flage = True
            for color_str,v in data['prices'].iteritems():
                if not price_flage: break
                if isinstance(v, list):
                    for val in v:
                        if prd.key == str(val['inventory_id']):
                            price = str(val['sale_price'])
                            listprice = str(val['retail_price'])
                            price_flage = False
                            color = color_str
                            break
                    else:
                        price = str(val['sale_price'])
                        listprice = str(val['retail_price'])
                elif isinstance(v, dict):
                    for size, val in v.iteritems():
                        if prd.key == str(val['inventory_id']):
                            price = str(val['sale_price'])
                            listprice = str(val['retail_price'])
                            price_flage = False
                            color = color_str
                            break
                    else:
                        price = str(val['sale_price'])
                        listprice = str(val['retail_price'])

            if price:
                if price != prd.price:
                    print 'hautelook product[{0}] price error: {1} vs {2}'.format(prd.combine_url, price, prd.price)
            if listprice:
                if listprice != prd.listprice:
                    print 'hautelook product[{0}] listprice error: {1} vs {2}'.format(prd.combine_url, listprice, prd.listprice)


    def get_product_abstract_by_url(self, url):
        product_id = re.compile(r'/product/(\d+)').search(url).group(1)
        url = 'http://www.hautelook.com/v2/product/' + product_id
        j = self.s.get(url, headers=self.headers).json
        title = j['data']['title'].encode('utf-8')
        description = re.sub(r'<[^>]+>', '', j['data']['copy']).encode('utf-8')
        return 'hautelook_'+product_id, title+'_'+description

if __name__ == '__main__':
    Hautelook().check_product_right()
