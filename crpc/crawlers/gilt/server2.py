#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
from datetime import datetime, timedelta

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
        self.extract_hero_image = re.compile('background:url\((.*)\)')

    def crawl_category(self, ctx=''):
        """.. :py:method::
        """
        self.net.check_signin()
        categories = ['women', 'men', 'children', ]
        for cat in categories:
            link = 'http://www.gilt.com/sale/{0}'.format(cat)
            tree = self.download_page_get_correct_tree(link, cat, 'download category error')
            self.parse_event(tree, cat, ctx)

            if cat != 'children':
                link = 'http://www.gilt.com/sale/{cat}/{cat}s-shop/ss'.format(cat=cat)
                tree = self.download_page_get_correct_tree(link, cat, 'download shop error')
                self.save_group_of_event('', tree, cat, ctx)

        self.crawl_category_home(ctx)


    def download_page_get_correct_tree(self, url, key, warning):
        """.. :py:method::
            women page, upcoming page, parent event page, shop page,
            They both have two </html>, 200 is random by me

        :param url: url of the page
        :param key: key of the event
        :param warning: if download error, warning raise
        """
        cont = self.net.fetch_page(url)
        if cont is None or isinstance(cont, int):
            common_failed.send(sender=ctx, key=key, url=url,
                    reason='{0}: {1}'.format(warning, cont))
            return

        end_html_position = cont.find('</html>')
        if len(cont) - end_html_position > 200:
            tree = lxml.html.fromstring(cont[:end_html_position] + cont[end_html_position+7:])
        else:
            tree = lxml.html.fromstring(cont)
        return tree


    def parse_event(self, tree, dept, ctx):
        """.. :py:method::
        """
        # hero event
        sale_title = tree.cssselect('div#sticky-nav > div.sticky-nav-container > ul.tabs > li.sales > div > div.bg_container > div.column_currentcol_height > ul > li > a')[0].text_content().strip()
        img = tree.cssselect('section#main > div.hero-container > section.hero')[0]
        image = self.extract_hero_image.search(img.get('style')).group(1)
        image = image if image.startswith('http:') else 'http:' + image
        link = img.cssselect('a.sale-header-link')[0].get('href')
        if link.rsplit('/', 1)[-1] == 'ss':
            event_id = link.rsplit('/', 2)[-2]
            is_leaf = False
        else:
            event_id = link.rsplit('/', 1)[-1]
            is_leaf = True
        if is_leaf is False:
            self.get_child_event(event_id, link, dept, ctx)
        event, is_new, is_updated = self.get_or_create_event(event_id, link, dept, sale_title, image, is_leaf)
        event.update_time = datetime.utcnow()
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event_id, url=link, is_new=is_new, is_updated=is_updated)


        # on sale events
        nodes = tree.cssselect('section#main > div.sales-container > section.new-sales > article.sale')
        for node in nodes:
            ret = self.parse_one_node(node, dept, ctx)
            if ret is None: continue
            event, is_new, is_updated = ret
            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)

        # ending soon
        nodes = tree.cssselect('section#main > div.sales-container > section.sales-ending-soon > article.sale')
        for node in nodes:
            ret = self.parse_one_node(node, dept, ctx)
            if ret is None: continue
            event, is_new, is_updated = ret
            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)

        # starting later. When today's upcoming on sale, this column disappear for a while
        nodes = tree.cssselect('section#main > div.sales-container > section.sales-starting-later > article.sale')
        for node in nodes:
            event, is_new, is_updated = self.parse_one_node(node, dept, ctx)

            begins = node.cssselect('header > hgroup > h3 > span')[0].get('data-gilt-date')
            event.events_begin = datetime.strptime(begins[:begins.index('+')], '%m/%d/%Y %H:%M ')
            if not event.sale_description:
                ret = self.get_picture_description(event.combine_url)
                if ret is not None: # starting later today, already on sale
                    image, sale_description, events_begin = ret
                    event.image_urls = image
                    event.sale_description = sale_description

            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)

        # upcoming
        nodes = tree.cssselect('section#main > div.sales-container > div.sales-promos > section.calendar-sales > div.tab_content > div.scroll-container > article.sale')
        for node in nodes:
            event, is_new, is_updated = self.parse_one_node(node, dept, ctx)
            if not event.sale_description:
                image, sale_description, events_begin = self.get_picture_description(event.combine_url)
                event.image_urls = image
                event.sale_description = sale_description
                event.events_begin = events_begin

            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)


    def parse_one_node(self, node, dept, ctx):
        """.. :py:method::
            parse one event node
        """
        link = node.xpath('./a')[0].get('href')
        link = link if link.startswith('http') else self.siteurl + link
        if self.siteurl not in link: # women have www.giltcity.com and www.jetsetter.com
            return
        sale_title = node.xpath('./a/img')[0].get('alt').strip()
        image = node.xpath('./a/img/@src')
        if image: # type lxml.etree._ElementStringResult
            image = str(image[0]) if image[0].startswith('http:') else 'http:' + image[0]
        if link.rsplit('/', 1)[-1] == 'ss':
            event_id = link.rsplit('/', 2)[-2]
            is_leaf = False
        else:
            event_id = link.rsplit('/', 1)[-1]
            is_leaf = True

        if is_leaf is False:
            self.get_child_event(event_id, link, dept, ctx)
        event, is_new, is_updated = self.get_or_create_event(event_id, link, dept, sale_title, image, is_leaf)
        event.update_time = datetime.utcnow()
        return event, is_new, is_updated


    def get_or_create_event(self, event_id, link, dept, sale_title, image, is_leaf):
        """.. :py:method::
            upcoming image > on sale image > ending soon image,
            so event image only add once when you first meet it
        :param event_id:
        :param link: event listing url
        :param dept: department
        :param sale_title: event title 
        :param image: str image or []
        :param is_leaf: whether it is a leaf event
        """
        is_new, is_updated = False, False
        event = Event.objects(event_id=event_id).first()
        if not event:
            is_new = True
            event = Event(event_id=event_id)
            event.urgent = True
            event.combine_url = link
            event.sale_title = sale_title
            if image:
                event.image_urls.append(image)
            event.is_leaf = is_leaf
            if '/sale/women' in link:
                event.dept = ['women']
            elif '/sale/men' in link:
                event.dept = ['men']
            elif '/sale/children' in link:
                event.dept = ['children']
            elif '/home/sale' in link:
                event.dept = ['home']
        return event, is_new, is_updated


    def get_picture_description(self, url):
        """.. :py:method::
        """
        tree = self.download_page_get_correct_tree(url, '', 'download upcoming page error')
        nav = tree.cssselect('section#main > article.sale-brand-summary')
        # kids event already on sale, but in men's starting later today
        if not nav: return
        image = nav[0].xpath('./img/@src')
        sale_description = nav[0].cssselect('section.copy > p.bio')[0].text_content().strip()

        data_gilt_time = tree.cssselect('span#shopInCountdown')[0].get('data-gilt-time')
        events_begin = self.gilt_time(data_gilt_time)
        return image, sale_description, events_begin


    def get_child_event(self, event_id, link, dept, ctx):
        """.. :py:method::
        :param event_id: this parent event id
        :param link: this event list link
        """
        tree = self.download_page_get_correct_tree(link, event_id, 'download parent event list error')
        self.save_group_of_event(event_id, tree, dept, ctx)


    def save_group_of_event(self, event_id, tree, dept, ctx):
        """.. :py:method::

        :param event_id: parent event id, if no event_id passed,
        :param tree: xml tree of event groups
        """
        groups = tree.cssselect('div#main div.ss-col-wrapper > div.ss-col-wide > div.row_group')
        for group in groups:
            group_title = group.cssselect('h2.row_group_title')[0].text_content().strip()
            nodes = group.cssselect('ul.sales > li.brand_square')
            for node in nodes:
                event, is_new, is_updated = self.parse_one_node(node, dept, ctx)
                if is_new:
                    if event_id: event.parent_id = event_id
                    if group_title: event.group_title = group_title
                event.save()
                common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)


    def gilt_time(self, data_gilt_time):
        """.. :py:method::
            data_gilt_time is the original time from gilt
            pricision: microsecond
        """
        _time = datetime.utcnow() + timedelta(seconds= int(data_gilt_time) // 1000)
        return _time.replace(second=0, microsecond=0)



    def crawl_category_home(self, ctx):
        dept = 'home'
        url = 'http://www.gilt.com/home/sale'
        tree = self.download_page_get_correct_tree(url, dept, 'download \'home\' error')

        nav = tree.cssselect('div.content-container > section.content > div > div.position')[0]
        # hero 'div.elements-container > article.element'
        hero = nav.cssselect('section.module-full > div.elements-container > article.element-hero')[0]
        sale_title = hero.cssselect('div.hero-center-wrapper > div.hero-center-container > div.hero-editorial > header.element-header > hgroup > .headline')[0].text_content().strip()
        event, is_new, is_updated = self.parse_one_home_node(hero, dept, ctx)
        event.sale_title = sale_title
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)


        # on sale
        nodes = nav.cssselect('section.module-sale-mosaic > div.elements-container > article.element')
        for node in nodes:
            event, is_new, is_updated = self.parse_one_home_node(node, dept, ctx)
            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)

        # start later today & ending soon
        for sale_small in nav.cssselect('section.module-additional-sale-mosaic'):
            if 'Starting Later Today' == sale_small.cssselect('module-header > hgroup h1.headline')[0].text_content().strip():
                nodes = sale_small.cssselect('div.elements-container > article.element')
                for node in nodes:
                    event, is_new, is_updated = self.parse_one_home_node(node, dept, ctx)
                    event.save()
                    common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)
                    # TODO Go to that page to see starting time
            elif 'Ending Soon' == sale_small.cssselect('module-header > hgroup h1.headline')[0].text_content().strip():
                nodes = sale_small.cssselect('div.elements-container > article.element')
                for node in nodes:
                    event, is_new, is_updated = self.parse_one_home_node(node, dept, ctx)
                    event.save()
                    common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)

        # upcoming
        nav.cssselect('section.module-sidebar-mosaic > div.elements-container > article.element-cms-default > ul.nav > li.nav-item > div.nav-dropdown > section.nav-section')
        tree = self.download_page_get_correct_tree(url, dept, 'download upcoming \'home\' error')
        timer = tree.cssselect('div.page-container > div.content-container > section.page-details > div.layout-background > div.layout-wrapper > div.layout-container > section.sale-details > div.sale-time')
        _begin = timer.get('data-timer-start')
        datetime.utcfromtimestamp(float(_begin[:10]))
        _end = timer.get('data-timer-end') # 1356714000000
        datetime.utcfromtimestamp(float(_end[:10]))



    def parse_one_home_node(self, node, dept, ctx):
        """.. :py:method::
        """
        bottom_node = node.cssselect('figure.element-image > span.media > a')[0]
        link = bottom_node.get('href')
        link = link if link.startswith('http') else self.siteurl + link
        if self.siteurl in link: # have www.giltcity.com and www.jetsetter.com
            image = bottom_node.cssselect('img')[0].get('src')
            image = image if image.startswith('http:') else 'http:' + image
            sale_title = bottom_node.cssselect('img')[0].get('alt')

            event, is_new, is_updated = self.get_or_create_event(link.rsplit('/', 1)[-1], link, dept, sale_title, image, is_leaf=True)
            event.update_time = datetime.utcnow()
            return event, is_new, is_updated


    def crawl_listing(self, url, ctx=''):
        """ http://www.gilt.com/home/sale/almost-gone-bedding-3351?layout=f&grid-variant=new-grid&
        """
        pass

    def crawl_product(self, url, ctx=''):
        pass

if __name__ == '__main__':
    Server().crawl_category()
