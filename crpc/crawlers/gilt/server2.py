#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html

from crawlers.common.stash import *
from crawlers.common.events import common_saved, common_failed
from models import *

req = requests.Session(prefetch=True, timeout=30, config=config, headers=headers)

class giltLogin(object):
    """.. :py:class:: giltLogin
        login, check whether login, fetch page.
    """
    def __init__(self):
        """.. :py:method::
            variables need to be used
        """
        self.login_url = 'https://www.gilt.com/login'
        self.data = { 
            'email': login_email,
            'password': login_passwd,
            'remember_me': 'on',
        }    

        self._signin = False

    def login_account(self):
        """.. :py:method::
            use post method to login
        """
        req.get(self.login_url)
        req.post('https://www.gilt.com/login/redirect', data=self.data)
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

        if ret.ok: return ret.content
        return ret.status_code

class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.gilt.com'
        self.net = giltLogin()

    def crawl_category(self, ctx=''):
        """.. :py:method::
        """
        self.net.check_signin()
        categories = ['women', 'men', 'children', ]
        for cat in categories:
            link = 'http://www.gilt.com/sale/{0}'.format(cat)
            cont = self.net.fetch_page(link)
            if cont is None or isinstance(cont, int):
                common_failed.send(sender=ctx, key=cat, url=link,
                        reason='download category error: {0}'.format(cont))
            tree = lxml.html.fromstring(cont)
            self.parse_event(tree)

        link = 'http://www.gilt.com/home/sale'

    def parse_event(self, tree):
        nodes = tree.cssselect('section#main > div.sales-container > section.new-sales > article.sale')
        for node in nodes:
            link = node.xpath('./a/@href')
            link = link if link.startswith('http') else self.siteurl + link
            title = node.xpath('./a/img/@alt').strip()
            image = node.xpath('./a/img/@src')
            if link.rsplit('/', 1)[-1] == 'ss':
                print title, title, image

    def crawl_listing(self, url, ctx=''):
        pass

    def crawl_product(self, url, ctx=''):
        pass

if __name__ == '__main__':
    Server().crawl_category()
