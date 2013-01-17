#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

"""
crawlers.belleandclive.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.
"""
import re
import lxml.html

from models import *
from crawlers.common.events import common_saved, common_failed
from crawlers.common.stash import *

header = { 
    'Host': 'www.belleandclive.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0',
}

req = requests.Session(prefetch=True, timeout=30, config=config, headers=header)

class belleandcliveLogin(object):
    """.. :py:class:: belleandcliveLogin
        login, check whether login, fetch page.
    """
    def __init__(self):
        """.. :py:method::
            variables need to be used
        """
        self.login_url = 'http://www.belleandclive.com/account/login.jsp'
        self.data = { 
            '_dyncharset': 'ISO-8859-1',
            '_dynSessConf': '-5253286180443458341',
            'action': 'login',
            'email': login_email,
            '_D:email': '',
            'pwd': login_passwd,
            '_D:pwd': '',
            '/atg/userprofiling/B2CProfileFormHandler.login': '',
            '_D:/atg/userprofiling/B2CProfileFormHandler.login': '',
            '/atg/userprofiling/B2CProfileFormHandler.loginErrorURL': '/account/login.jsp',
            '_D:/atg/userprofiling/B2CProfileFormHandler.loginErrorURL': '', 
            '/atg/userprofiling/B2CProfileFormHandler.loginSuccessURL': '/browse/sales/current.jsp',
            '_D:/atg/userprofiling/B2CProfileFormHandler.loginSuccessURL': '', 
            '/atg/userprofiling/B2CProfileFormHandler.logoutSuccessURL': '/index.jsp',
            '_D:/atg/userprofiling/B2CProfileFormHandler.logoutSuccessURL': '',
            '_DARGS': '/account/login/login_or_request.jsp.member-form',
        }   

        self._signin = False

    def login_account(self):
        """.. :py:method::
            use post method to login
        """
        login_post = 'https://www.belleandclive.com/index.jsp?_DARGS=/account/login/login_or_request.jsp.member-form'
        req.get(self.login_url)
        req.post(login_post, data=self.data)
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

        if 'http://www.belleandclive.com/member' in ret.url: #login
            self.login_account()
            ret = req.get(url)
        if ret.ok: return ret.content

        return ret.status_code


class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.belleandclive.com'
        self.net = belleandcliveLogin()
        self.extract_large_image = re.compile("(.+&outputx=)(\d+)(&outputy=)(\d+)(.+)")

    def crawl_category(self, ctx=''):
        # self.net.check_signin()
        depts = ['women', 'men']
        for dept in depts:
            url = 'http://www.belleandclive.com/browse/sales/current.jsp?shop={0}'.format(dept)
            self.crawl_one_dept(dept, url, ctx)

    def crawl_one_dept(self, dept, url, ctx):
        """.. :py:method::

        :param dept: department
        :param url: department's url
        """
        tree = self.download_page_ret_tree('', url, 'download department[{0}] failed:'.format(dept), ctx)
        if tree is None: return
        nodes = tree.cssselect('div#page-wrapper > div#content > div.sales > div.sale > ul#sliding-content > li')
        for node in nodes:
            self.parse_one_event_node(dept, node, ctx)

        if dept == 'men':
            link = tree.cssselect('div#page-wrapper > div#header > div#header-content > div#nav > ul#main-nav > li > a#header-navigation-vintage')[0].get('href')
            link = link if link.startswith('http') else self.siteurl + link
            self.crawl_vintage_info('vintage', link, ctx)

    def download_page_ret_tree(self, key, url, reason, ctx):
        """.. :py:method::
        """
        content = self.net.fetch_page( url )
        if content is None or isinstance(content, int):
            common_failed.send(sender=ctx, key=key, url=url,
                    reason='{0} {1}'.format(reason, content))
            return
        tree = lxml.html.fromstring(content)
        return tree

    def parse_one_event_node(self, dept, node, ctx):
        """.. :py:method::

        :param dept: department
        :param node: xpath node
        """
        link = node.cssselect('div.sale-image > a')[0]
        img = link.cssselect('img')[0].get('src')
        img = img if img.startswith('http') else self.siteurl + img
        sale_title = link.cssselect('img')[0].get('alt')
        link = link.get('href')
        event_id = link.rsplit('cat', 1)[-1]
        link = link if link.startswith('http') else self.siteurl + link

        end = node.cssselect('div.sale-image > div.sale-countdown > p.countdown')[0].get('data-countdown')
        events_end = datetime.utcfromtimestamp( float(end[:10]) )
        sale_description = node.cssselect('div.sale-info > p.collection-description')[0].text_content().strip()
        cat = node.cssselect('div.sale-info div.sale-title-wrapper > p.sale-cat')[0].text_content().strip()
        if not cat.lower().startswith(dept):
            dept = "{0}'s {1}".format(dept.capitalize(), cat)
        self.get_or_create_event(dept, event_id, link, img, sale_title, sale_description, events_end, ctx)

    def crawl_vintage_info(self, dept, url, ctx):
        """.. :py:method::
        """
        tree = self.download_page_ret_tree('', url, 'download department[{0}] failed:'.format(dept), ctx)
        if tree is None: return
        nav = tree.cssselect('div#page-wrapper > div#content > div#sales-wrapper > div.top-sale')[0]
        img = nav.cssselect('img.sale-image')[0].get('src')
        img = img if img.startswith('http') else self.siteurl + img
        sale_title = nav.cssselect('img.sale-image')[0].get('alt')
        end = nav.cssselect('div.description > p.countdown')[0].get('data-countdown')
        events_end = datetime.utcfromtimestamp( float(end[:10]) )
        sale_description = nav.cssselect('div.description > p.desc')[0].text_content()
        event_id = url.rsplit('cat', 1)[-1]
        self.get_or_create_event(dept, event_id, url, img, sale_title, sale_description, events_end, ctx)


    def get_or_create_event(self, dept, event_id, link, img, sale_title, sale_description, events_end, ctx):
        """.. :py:method::
        """
        is_new, is_updated = False, False
        event = Event.objects(event_id=event_id).first()
        if not event:
            is_new = True
            event = Event(event_id=event_id)
            event.urgent = True
            event.combine_url = link
            event.image_urls = [img]
            event.sale_title = sale_title
            event.sale_description = sale_description
        event.events_end = events_end
        event.dept = [dept] # belleandclive's dept will change to be right, so I need to keep it right.
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=link, is_new=is_new, is_updated=is_updated)


    def crawl_listing(self, url, ctx=''):
        event_id = url.rsplit('cat', 1)[-1]
        tree = self.download_page_ret_tree(event_id, url, 'download listing page failed:', ctx)
        if tree is None: return
        nodes = tree.cssselect('div#page-wrapper > div#content > div#sales-wrapper > div#sales > div.sale')
        for node in nodes:
            link = node.cssselect('div.sale-description > a[href]')[0].get('href')
            key = link.rsplit('id', 1)[-1]
            link = link if link.startswith('http') else self.siteurl + link
            brand = node.cssselect('div.sale-description > p.collection')[0].text_content().strip(':')
            title = node.cssselect('div.sale-description > a[href] > p.title')[0].text_content().strip(':')
            sizes = [size.text_content() for size in node.cssselect('div.sale-description > div.size-collection > b.indiv-size')]
            listprice = node.cssselect('div.price-wrapper > p.price > span.linethrough')
            listprice = listprice[0].text_content().strip() if listprice else ''
            price = node.cssselect('div.price-wrapper > p.price')[0].text_content().replace('Retail:', '').replace(listprice, '').strip()
            soldout = True if node.cssselect('div.soldout-wrapper') else False

            is_new, is_updated = False, False
            product = Product.objects(key=key).first()
            if not product:
                is_new = True
                product = Product(key=key)
                product.updated = False
                product.combine_url = link
                product.brand = brand
                product.title = title
                product.sizes = sizes
                product.listprice = listprice
                product.price = price
                product.soldout = soldout
            else:
                if soldout and product.soldout != True:
                    product.soldout = True
                    is_updated = True
                    product.update_history.update({ 'soldout': datetime.utcnow() })
            if event_id not in product.event_id: product.event_id.append(event_id)
            product.list_update_time = datetime.utcnow()
            product.save()
            common_saved.send(sender=ctx, obj_type='Product', key=key, url=link, is_new=is_new, is_updated=is_updated)

        event = Event.objects(event_id=event_id).first()
        if not event: event = Event(event_id=event_id)
        if event.urgent == True:
            event.urgent = False
            event.update_time = datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event_id, is_new=False, is_updated=False, ready=True)

        
    def crawl_product(self, url, ctx=''):
        key = url.rsplit('id', 1)[-1]
        tree = self.download_page_ret_tree(key, url, 'download product page failed:'.format(dept), ctx)
        color = tree.cssselect('div#colors span#color-label')
        color = color[0].text_content() if color else ''
        shipping = tree.cssselect('div#international-shipping-message > a#international-shipping-link')
        shipping =  shipping[0].text_content() if shipping else ''
        shipping_normal = tree.cssselect('h4#shipping-returns')#.replace('', '')
        shipping = shipping_normal[0].text_content() + ' ' + shipping if shipping_normal else shipping
        returned = tree.cssselect('div#retrun-policy-box > p')[0].text_content().strip()
        desc = tree.cssselect('div#description-box')
        summary = desc.xpath('./p')[0].text_content().strip()
        list_info = [li.text_content().strip() for li in desc.xpath('./ul > li')]

        image_urls = []
        for image in tree.cssselect('div#thumbnails > img.thumbnail'):
            aa, outx, bb, outy, cc = self.extract_large_image.search( image.get('relsmall') ).groups()
            image_urls.append( '{0}{1}{2}{3}{4}'.format(aa, int(outx)*2, bb, int(outy)*2, cc) )

        is_new, is_updated = False, False
        product = Product.objects(key=key).first()
        if not product:
            is_new = True
            product = Product(key=key)
        if color: product.color = color
        product.shipping = shipping
        product.returned = returned
        product.summary = summary
        product.list_info = list_info
        [product.image_urls.append(img) for img in image_urls if img not in product.image_urls]
        product.full_update_time = datetime.utcnow()
        if product.updated == False:
            product.updated = True
            ready = True
        else: ready = False
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=key, url=url, is_new=is_new, is_updated=is_updated, ready=ready)


if __name__ == '__main__':
    import zerorpc
    from settings import CRAWLER_PORT
    server = zerorpc.Server(Server())
    server.bind('tcp://0.0.0.0:{0}'.format(CRAWLER_PORT))
    server.run()
