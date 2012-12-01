import requests
import lxml.html
import re

test_url = 'http://www.ruelala.com/event/product/61521/1111946014/0/DEFAULT'

class Ruelala(object):
    def __init__(self):
        self.s = requests.session()
        self.headers = {
            'Cookie':'symfony=m0ecn71apqi5p7tbsbfr7sqat2; X-CCleaned=1; optimizelyEndUserId=oeu1350984411091r0.8540810437407345; cmTPSet=Y; CoreID6=51506981224513509844111&ci=90210964; stid=aHVhbnpodUBmYXZidXkuY29tOjEzNjc2NTcxMjQ6N2U2V09jUkdFRDc3VTJ3dzd1U3dyd1FFb0ZaODZrLzc2MDV5V1gwbi93TT0=; stos=-93967; currentAlias=4pmygcbb; NSC_SVF_QPPM_BMM=ffffffff096c9d3c45525d5f4f58455e445a4a423660; mastHeadInfo=%7B%22mhi%22%3A%5B%7B%22cc%22%3A0%2C%22cb%22%3A0%2C%22fn%22%3A%22stephanie%22%2C%22fset%22%3A0%2C%22uid%22%3A9471446%2C%22lrid%22%3A1%2C%22rpm%22%3A0%2C%22ts%22%3A1353904216750%2C%22fseta%22%3Afalse%7D%5D%7D; optimizelySegments=%7B%7D; optimizelyBuckets=%7B%2285231564%22%3A%22105195277%22%7D; eventPageScrollPosition=0%7C0%7C57701; aid=1001; userEmail=huanzhu@favbuy.com; uid=9471446; rusersign=pM7Qg9lgkbwXKJPogkVGFZhYlxK24aB5VG2HZqFs5c7gnbMTPD8UnzYFPE2XNVPPHYWwV1ggSb%2BY%0D%0AxiGhHijdA%2BoGACCoVFx6E3gXyWE1%2BGEeaj2By3%2F037JRnKetYPhGZzCL8a94TkR0vahredOnZEvG%0D%0Ah%2F9KsgIT6lFXzqJZlfeZpIW8aBOK%2BR0eD%2FXHTODsFmDkwrERuEFnz6v5ooQrYGCJ1VVM2gUursgz%0D%0AtXYeleOLaVtU8Yy7BrMFBHnJqi3rw0NCZ8h%2B5jil1%2Fv1zzfZgolqoYseZRgySn%2BzI2%2FdmXFc%2BhL5%0D%0ApIWw6vJc32madG277NVZbAqiSOUTRBxGM4MMZw%3D%3D; ruserbase=eyJpZCI6W3siaWQiOjk0NzE0NDYsInR5cGUiOiJydWVsYWxhIn1dLCJ0cmFja2luZyI6W3sibmFt%0D%0AZSI6InJlZmVycmVySWQiLCJ2YWx1ZSI6Ik9UUTNNVFEwTmc9PSJ9LHsibmFtZSI6ImVLZXkiLCJ2%0D%0AYWx1ZSI6ImFIVmhibnBvZFVCbVlYWmlkWGt1WTI5dCJ9XX0%3D; ssids=61178; uhv=8e4314db871b3222e41a856ffe55a0a332ba2635055bf4e597fed31ef6052bf6; Liberty.QuickBuy.canQuickBuy=0; siteid=full; Liberty.QuickBuy.eventId=61521; Liberty.QuickBuy.styleNum=1111946014; urk=ff1dab286940ef31d3d004de63cb14d9c9356330; urkm=ffb19afa9b8a4dac3ea45efc82334d061b4c6a35; pgts=1354346828; 90210964_clogin=l=1354346970&v=1&e=1354348852871'
        }
    
    def get_product_abstract_by_url(self, url):
        content = self.s.get(url, headers=self.headers).content
        product_id = re.compile(r'/product/(\d+)').search(url).group(1)
        t = lxml.html.fromstring(content)
        title = t.xpath('//*[@id="productName"]')[0].text
        description = ''
        for li in t.xpath('//*[@id="info"]/ul/li'):
            description += li.text_content() + '\n'
        return title.replace(' ','_')+'_'+product_id, title+'_'+description

if __name__ == '__main__':
    print Ruelala().get_product_abstract_by_url(test_url)
