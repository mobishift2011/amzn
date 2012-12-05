#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

"""
crawlers.ideeli.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.
"""
import urllib
import lxml.html

from models import *
from crawlers.common.events import common_saved, common_failed
from crawlers.common.stash import *

headers = { 
    'Host': 'www.ideeli.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0',
}

req = requests.Session(prefetch=True, timeout=30, config=config, headers=headers)

class ideeliLogin(object):
    """.. :py:class:: beyondtherackLogin
        login, check whether login, fetch page.
    """
    def __init__(self):
        """.. :py:method::
            variables need to be used
        """
        self.login_url = 'https://www.ideeli.com/login'
        self.data = { 
            'login': login_email,
            'password': login_passwd,
            'x': 64,
            'y': 20,
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

        if 'https://www.ideeli.com/login' == ret.url: #login
            self.login_account()
            ret = req.get(url)
        if ret.ok: return ret.content

        return ret.status_code



class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.ideeli.com'
        self.homepage = 'http://www.ideeli.com/events/latest'
        self.event_img_prefix = 'http://lp-img-production.ideeli.com'
        self.net = ideeliLogin()

    def crawl_category(self, ctx=''):
        depts = ['women', 'men', 'home', 'holiday',]
        for dept in depts:
            self.crawl_one_dept(dept, ctx)

    def crawl_one_dept(self, dept, ctx):
        """.. :py:method::

        :param dept: department
        """
        url = urllib.basejoin(self.homepage, dept)
        content = self.net.fetch_page( url )
        if content is None or isinstance(content, int):
            common_failed.send(sender=ctx, key=dept, url=url,
                    reason='download this department failed: {0}'.format(content))
        tree = lxml.html.fromstring(content)
        nav = tree.cssselect('div#container > div#content > div#on_sale_today > div#women_channel')[0]
        nodes = nav.cssselect('div > div#on_sale_left_col > div#on_sale_today_channel > div#latest_events_container > div.event_unit > a[href]')
        for node in nodes:
            node.get('href')
            img = node.cssselect('img[data-src]')[0].get('data-src')
            img = img if img.startswith('http') else urllib.basejoin(self.event_img_prefix, img)
            node.cssselect('')
        # nav.cssselect('div#ending_soon_tabs')


if __name__ == '__main__':
    import zerorpc
    from settings import CRAWLER_PORT
    server = zerorpc.Server(Server())
    server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
    server.run()
