#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
from datetime import datetime

from crawlers.common.stash import *
from models import *


class lot18Login(object):
    """.. :py:class:: lot18Login
        login, check whether login, fetch page.
    """
    def __init__(self):
        """.. :py:method::
            variables need to be used
        """
        self.login_url = 'http://www.lot18.com/login'
        self.data = {
            'email': login_email,
            'password': login_passwd,
        }

        self._signin = False

    def login_account(self):
        """.. :py:method::
            use post method to login
        """
        request.get(self.login_url)
        request.post(self.login_url, self.data)
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
        ret = request.get(url)

        if 'http://www.lot18.com/login' in ret.url:
            self.login_account()
            ret = request.get(url)
        if ret.ok: return ret.content

        return ret.status_code


class Server(object):
    def __init__(self):
        self.net = lot18Login()

    def crawl_category(self, ctx=''):
        is_new, is_updated = False, False
        category = Category.objects(sale_title='lot18').first()
        if not category:
            is_new = True
            category = Category(sale_title='lot18')
            category.is_leaf = True
            category.cats = ['wine']
        category.update_time = datetime.utcnow()
        category.save()
        common_saved.send(sender=ctx, obj_type='Category', key='', url='', is_new=is_new, is_updated=is_updated)


    def crawl_listing(self, url, ctx=''):
        return
        tree = lxml.html.fromstring(content)
        nodes = tree.cssselect('div#page > div.container-content > div.product-wrapper div.product')

    def crawl_product(self, url, ctx=''):
        pass
