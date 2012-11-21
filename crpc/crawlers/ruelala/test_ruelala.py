#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

from crawlers.common.stash import *
headers = {
    'Host': 'www.ruelala.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0',
    'Referer': 'http://www.ruelala.com/event',
    'Cookie': 'X-CCleaned=1; optimizelyEndUserId=oeu1349667187777r0.2759982226275626; optimizelyBuckets=%7B%7D; CoreID6=87382265939413496671878&ci=90210964; userEmail=huanzhu@favbuy.com; optimizelySegments=%7B%7D; symfony=r81cu3qbbjn7nc63g60i0nap34; Liberty.QuickBuy.canQuickBuy=0; 90210964_clogin=l=1353388560&v=1&e=1353390811310; cmTPSet=Y; pgts=1353390708; NSC_SVF_QPPM_BMM=ffffffff096c9d3a45525d5f4f58455e445a4a423660; Liberty.QuickBuy.eventId=59006; Liberty.QuickBuy.styleNum=3030858912; aid=1001; urk=bfb8a96cc255d42649093b974d212aaf8e65848b; urkm=fcac147b49ab4bb16bd30d2e5d1eb378e9a88acd; uid=9471446; rusersign=pM7Qg9lgkbwXKJPogkVGFZhYlxK24aB5VG2HZqFs5c7gnbMTPD8UnzYFPE2XNVPPHYWwV1ggSb%2BY%0D%0AxiGhHijdA%2BoGACCoVFx6E3gXyWE1%2BGEeaj2By3%2F037JRnKetYPhGZzCL8a94TkR0vahredOnZEvG%0D%0Ah%2F9KsgIT6lFXzqJZlfeZpIW8aBOK%2BR0eD%2FXHTODsFmDkwrERuEFnz6v5ooQrYGCJ1VVM2gUursgz%0D%0AtXYeleOLaVtU8Yy7BrMFBHnJqi3rw0NCZ8h%2B5jil1%2Fv1zzfZgolqoYseZRgySn%2BzI2%2FdmXFc%2BhL5%0D%0ApIWw6vJc32madG277NVZbAqiSOUTRBxGM4MMZw%3D%3D; ruserbase=eyJpZCI6W3siaWQiOjk0NzE0NDYsInR5cGUiOiJydWVsYWxhIn1dLCJ0cmFja2luZyI6W3sibmFt%0D%0AZSI6InJlZmVycmVySWQiLCJ2YWx1ZSI6Ik9UUTNNVFEwTmc9PSJ9LHsibmFtZSI6ImVLZXkiLCJ2%0D%0AYWx1ZSI6ImFIVmhibnBvZFVCbVlYWmlkWGt1WTI5dCJ9XX0%3D; ssids=59504; uhv=8e4314db871b3222e41a856ffe55a0a332ba2635055bf4e597fed31ef6052bf6; siteid=full; stid=aHVhbnpodUBmYXZidXkuY29tOjEzNjg5NDI3MzI6NFovUHJDMHd2RGcwb1ViWi9QUVpXZDM3Y3dRQ3Y1R0ljMkFZSG5CajFYOD0='
}

req = requests.Session(prefetch=True, timeout=30, config=config, headers=headers)

class ruelalaLogin(object):
    """.. :py:class:: ruelalaLogin
        login, check whether login, fetch page.
    """
    def __init__(self):
        """.. :py:method::
            variables need to be used
        """
        self.login_url = 'http://www.ruelala.com/access/gate'
        self.data = {
            'email': login_email,
            'password': login_passwd,
            'loginType': 'gate',
            'rememberMe': 1,
        }
        self._signin = False

    def login_account(self):
        """.. :py:method::
            use post method to login
        """
        req.post(self.login_url, data=self.data)
        self._signin = True

    def check_signin(self):
        """.. :py:method::
            check whether the account is login
        """
        if not self._signin:
            self.login_account()

    def fetch_page(self, url):
        """.. :py:method::
            fetch page.
            check whether the account is login, if not, login and fetch again
        """
        ret = req.get(url)

        if ret.status_code == 401: # need to authentication
            self.login_account()
            ret = req.get(url)
        if ret.ok: return ret.content
        return ret.status_code

if __name__ == '__main__':
    login = ruelalaLogin()
    print login.fetch_page('http://www.ruelala.com/category/kids')

