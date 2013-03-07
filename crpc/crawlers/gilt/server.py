#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import lxml.html
import time
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
            'email': login_email[DB],
            'password': login_passwd,
            'remember_me': 'on',
        }    

        self.current_email = login_email[DB]
        self._signin = {}

    def login_account(self):
        """.. :py:method::
            use post method to login
        """
        self.data['email'] = self.current_email
        _now = int(time.time())
        _before = _now - 11
        auth_url = 'https://www.gilt.com/login/auth?callback=jQuery17206991992753464729_{0}&email={1}&password={2}&remember_me=on&_={3}'.format(_before*1000 + 450, self.data['email'], self.data['password'], _now*1000 + 739)
        req.get(auth_url)

        req.post('https://www.gilt.com/login/redirect', data=self.data)
        self._signin[self.current_email] = True

    def check_signin(self, username=''):
        """.. :py:method::
            check whether the account is login
        """
        if username == '':
            self.login_account()
        elif username not in self._signin:
            self.current_email = username
            self.login_account()
        else:
            self.current_email = username

    def fetch_page(self, url):
        """.. :py:method::
            fetch page.
        """
        ret = req.get(url)

        if ret.ok: return ret.content
        return ret.status_code

    def fetch_listing_page(self, url):
        """.. :py:method::
            fetch listing page.
        """
        ret = req.get(url)
        if ret.url == 'http://www.gilt.com/':
            return -302
        if ret.url == 'http://www.gilt.com/sale/women' or ret.url == 'http://www.gilt.com/sale/men' or 'http://www.gilt.com/brand/' in ret.url or 'http://www.gilt.com/apps/iphone' in ret.url:
            return -302
        if ret.ok: return ret.content
        return ret.status_code


    def fetch_product_page(self, url):
        """.. :py:method::
            fetch product page.
            women will redirect to this product's brand page if it is off sale
        """
        ret = req.get(url)
        if 'http://www.gilt.com/brand/' in ret.url or 'http://www.gilt.com/style/' in ret.url:
            return -302
        if ret.ok: return ret.content
        return ret.status_code

class Server(object):
    def __init__(self):
        self.siteurl = 'http://www.gilt.com'
        self.net = giltLogin()
        self.extract_hero_image = re.compile('background:url\((.*)\)')

    def crawl_category(self, ctx='', **kwargs):
        """.. :py:method::
        """
        if kwargs.get('login_email'): self.net.check_signin( kwargs.get('login_email') )
        else: self.net.check_signin()

        categories = ['women', 'men', 'children', ]
        for cat in categories:
            link = 'http://www.gilt.com/sale/{0}'.format(cat)
            tree = self.download_page_get_correct_tree(link, cat, 'download category error', ctx)
            self.parse_event(tree, cat, ctx)

            if cat != 'children':
                link = 'http://www.gilt.com/sale/{cat}/{cat}s-shop/ss'.format(cat=cat)
                tree = self.download_page_get_correct_tree(link, cat, 'download shop error', ctx)
                self.save_group_of_event('', tree, cat, ctx)

        self.crawl_category_home(ctx)


    def download_page_get_correct_tree(self, url, key, warning, ctx):
        """.. :py:method::
            women page, upcoming page, parent event page, shop page,
            They both have two </html>, 200 is random by me

        :param url: url of the page
        :param key: key of the event
        :param warning: if download error, warning raise
        """
        cont = self.net.fetch_page(url)
        if cont is None or isinstance(cont, int):
            cont = self.net.fetch_page(url)
            if cont is None or isinstance(cont, int):
                common_failed.send(sender=ctx, key=key, url=url,
                        reason='{0}: {1}'.format(warning, cont))
                return
        return self.get_correct_tree(cont)

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


    def parse_event(self, tree, dept, ctx):
        """.. :py:method::
        """
        # hero event
        # sale_title = tree.cssselect('div#sticky-nav > div.sticky-nav-container > ul.tabs > li.sales > div > div.bg_container > div.column > ul > li > a')[0].text_content().strip()
        img = tree.cssselect('section#main > div.hero-container > section.hero')[0]
        image = self.extract_hero_image.search(img.get('style')).group(1)
        image = image if image.startswith('http:') else 'http:' + image
        link = img.cssselect('a.sale-header-link')[0]
        sale_title = link.text_content()
        link = link.get('href')
        link = link if link.startswith('http') else self.siteurl + link
        if link.rsplit('/', 1)[-1] == 'ss':
            event_id = link.rsplit('/', 2)[-2]
            is_leaf = False
        else:
            event_id = link.rsplit('/', 1)[-1]
            is_leaf = True
        if is_leaf is False:
            self.get_child_event(event_id, link, dept, ctx)
        event, is_new, is_updated = self.get_or_create_event(event_id, link, dept, sale_title, image, is_leaf)
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
        # this label not exist anymore, instead of starting tomorrow
        nodes = tree.cssselect('section#main > div.sales-container > section.sales-starting-later > article.sale')
        for node in nodes:
            ret = self.parse_one_node(node, dept, ctx, upcoming=True)
            if ret is None: continue
            event, is_new, is_updated = ret

            begins = node.cssselect('header > hgroup > h3 > span')[0].get('data-gilt-date')
            events_begin = datetime.strptime(begins[:begins.index('+')], '%m/%d/%Y %H:%M ')
            if event.events_begin != events_begin:
                event.events_begin = events_begin
                event.update_history.update({ 'events_begin': datetime.utcnow() })
            if event.events_end != None:
                event.events_end = None
                event.update_history.update({ 'events_end': datetime.utcnow() })
            if event.product_ids != []:
                event.product_ids = []
                event.update_history.update({ 'product_ids': datetime.utcnow() })
            if not event.sale_description:
                ret = self.get_picture_description(event.combine_url, ctx)
                if ret is not None: # starting later today, already on sale
                    image, sale_title, sale_description, events_begin = ret
                    event.image_urls = image
                    event.sale_description = sale_description

            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)

        # starting tomorrow
        nodes = tree.cssselect('section#main > div.bottom-calendar-sales-container > section.calendar-sales > div.calendar-sales-container > div.calendar-sales > article.sale')
        for node in nodes:
            ret = self.parse_one_node(node, dept, ctx, upcoming=True)
            if ret is None: continue
            event, is_new, is_updated = ret
            image, sale_title, sale_description, events_begin = self.get_picture_description(event.combine_url, ctx)
            if not event.sale_description:
                event.image_urls = image
                event.sale_title = sale_title # some sale_title is too long to be omit by ...
                event.sale_description = sale_description
            if event.events_begin != events_begin:
                event.events_begin = events_begin
                event.update_history.update({ 'events_begin': datetime.utcnow() })
            if event.events_end != None:
                event.events_end = None
                event.update_history.update({ 'events_end': datetime.utcnow() })
            if event.product_ids != []:
                event.product_ids = []
                event.update_history.update({ 'product_ids': datetime.utcnow() })

            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)

        # upcoming
        nodes = tree.cssselect('section#main > div.sales-container > div.sales-promos > section.calendar-sales > div.tab_content > div.scroll-container > article.sale')
        for node in nodes:
            event, is_new, is_updated = self.parse_one_node(node, dept, ctx, upcoming=True)
            image, sale_title, sale_description, events_begin = self.get_picture_description(event.combine_url, ctx)
            if not event.sale_description:
                event.image_urls = image
                # some sale_title is too long to be omit by ...
                event.sale_title = sale_title
                event.sale_description = sale_description
            if event.events_begin != events_begin:
                event.events_begin = events_begin
                event.update_history.update({ 'events_begin': datetime.utcnow() })
            if event.events_end != None:
                event.events_end = None
                event.update_history.update({ 'events_end': datetime.utcnow() })
            if event.product_ids != []:
                event.product_ids = []
                event.update_history.update({ 'product_ids': datetime.utcnow() })

            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)


    def parse_one_node(self, node, dept, ctx, upcoming=False):
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

        if is_leaf is False and upcoming is False:
            self.get_child_event(event_id, link, dept, ctx)
        event, is_new, is_updated = self.get_or_create_event(event_id, link, dept, sale_title, image, is_leaf)
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
            elif '/home/sale' in link or '/sale/home' in link:
                event.dept = ['home']
        event.update_time = datetime.utcnow()
        return event, is_new, is_updated


    def get_picture_description(self, url, ctx):
        """.. :py:method::
        """
        tree = self.download_page_get_correct_tree(url, '', 'download upcoming page error', ctx)
        nav = tree.cssselect('section#main > article.sale-brand-summary')
        # kids event already on sale, but in men's starting later today
        if not nav: return
        image = nav[0].xpath('./img/@src')
        sale_title = nav[0].cssselect('section.copy > header.header')[0].text_content().strip()
        sale_description = nav[0].cssselect('section.copy > p.bio')[0].text_content().strip().encode('utf-8')

        data_gilt_time = tree.cssselect('span#shopInCountdown')[0].get('data-gilt-time')
        events_begin = self.gilt_time(data_gilt_time)
        return image, sale_title, sale_description, events_begin


    def get_child_event(self, event_id, link, dept, ctx):
        """.. :py:method::
        :param event_id: this parent event id
        :param link: this event list link
        """
        tree = self.download_page_get_correct_tree(link, event_id, 'download shops parent/child event list error', ctx)
        if tree is None: return
        self.save_group_of_event(event_id, tree, dept, ctx)


    def save_group_of_event(self, event_id, tree, dept, ctx):
        """.. :py:method::
            save the shops page of events

        :param event_id: parent event id, if no event_id passed,
        :param tree: xml tree of event groups
        """
        groups = tree.cssselect('div#main div.ss-col-wrapper > div.ss-col-wide > div.row_group')
        for group in groups:
            group_title = group.cssselect('h2.row_group_title')[0].text_content().strip()
            nodes = group.cssselect('ul.sales > li.brand_square')
            for node in nodes:
                ret = self.parse_one_node(node, dept, ctx)
                if ret is None: continue
                event, is_new, is_updated = ret
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
        """.. :py:method::
            crawl home, because home is different from 'women', 'men', 'children'
        """
        dept = 'home'
        url = 'http://www.gilt.com/home/sale'
        tree = self.download_page_get_correct_tree(url, dept, 'download \'home\' error', ctx)

        nav = tree.cssselect('div.content-container > section.content > div.holds-position-2 > div.position')[0]
        # hero 'div.elements-container > article.element'
        hero = nav.cssselect('section.module-full > div.elements-container > article.element-hero')[0]
        event, is_new, is_updated = self.parse_one_home_node(hero, dept, ctx)
        sale_title = hero.cssselect('div.hero-center-wrapper > div.hero-center-container > div.hero-editorial > header.element-header > hgroup > .headline')[0].text_content().strip()
        event.sale_title = sale_title
        event.save()
        common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)

        # on sale
        nodes = nav.cssselect('section.module-sale-mosaic > div.elements-container > article.element')
        for node in nodes:
            ret = self.parse_one_home_node(node, dept, ctx)
            if ret is not None:
                event, is_new, is_updated = ret
                event.save()
                common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)

        # start later today & ending soon, sometimes ending soon is disappeared
        for sale_small in nav.cssselect('section.module-additional-sale-mosaic'):
            headline = sale_small.cssselect('header.module-header > hgroup h1.headline')[0].text_content().strip()
            if 'Starting Later Today' == headline:
                nodes = sale_small.cssselect('div.elements-container > article.element')
                for node in nodes:
                    ret = self.parse_one_home_node(node, dept, ctx)
                    if ret is not None:
                        event, is_new, is_updated = ret
                    else: continue

                    if not event.sale_description:
                        events_begin, events_end, image, sale_description = self.get_home_future_events_begin_end(event.combine_url, event.event_id, ctx)
                        if event.events_begin != events_begin:
                            event.events_begin = events_begin
                            event.update_history.update({ 'events_begin': datetime.utcnow() })
                        if event.events_end != events_end:
                            event.events_end = events_end
                            event.update_history.update({ 'events_end': datetime.utcnow() })
                        event.image_urls = [image]
                        event.sale_description = sale_description
                    event.save()
                    common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)
            elif 'Ending Soon' == headline:
                nodes = sale_small.cssselect('div.elements-container > article.element')
                for node in nodes:
                    ret = self.parse_one_home_node(node, dept, ctx)
                    if ret is not None:
                        event, is_new, is_updated = ret
                        event.save()
                        common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)

        # upcoming
        nodes = nav.cssselect('section.module-sidebar-mosaic > div.elements-container > article.element-cms-default > ul.nav > li.nav-item > div.nav-dropdown > section.nav-section > ul > li.nav-topic')
        for node in nodes:
            self.parse_one_home_upcoming_node(node, dept, ctx)


    def parse_one_home_node(self, node, dept, ctx):
        """.. :py:method::
        """
        bottom_node = node.cssselect('figure > span > a')[0]
        link = bottom_node.get('href')
        link = link if link.startswith('http') else self.siteurl + link
        if self.siteurl in link: # have www.giltcity.com and www.jetsetter.com
            image = bottom_node.cssselect('img')[0].get('src')
            image = image if image.startswith('http:') else 'http:' + image
            sale_title = bottom_node.cssselect('img')[0].get('alt')

            event, is_new, is_updated = self.get_or_create_event(link.rsplit('/', 1)[-1], link, dept, sale_title, image, is_leaf=True)
            return event, is_new, is_updated


    def parse_one_home_upcoming_node(self, node, dept, ctx):
        """.. :py:method::
        """
        link = node.cssselect('span.topic-label > a')[0].get('href')
        link = link if link.startswith('http') else self.siteurl + link
        if self.siteurl in link: # have www.giltcity.com and www.jetsetter.com
            # image = node.cssselect('figure.element-media > a > img')[0].get('src')
            # image = image if image.startswith('http:') else 'http:' + image
            sale_title = node.cssselect('span.topic-label > a')[0].text_content()
            event, is_new, is_updated = self.get_or_create_event(link.rsplit('/', 1)[-1], link, dept, sale_title, image='', is_leaf=True)

            if not event.sale_description:
                events_begin, events_end, image, sale_description = self.get_home_future_events_begin_end(link, link.rsplit('/', 1)[-1], ctx)
                if event.events_begin != events_begin:
                    event.events_begin = events_begin
                    event.update_history.update({ 'events_begin': datetime.utcnow() })
                if event.events_end != events_end:
                    event.events_end = events_end
                    event.update_history.update({ 'events_end': datetime.utcnow() })
                event.image_urls = image if isinstance(image, list) else [image]
                event.sale_description = sale_description
            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event.event_id, url=event.combine_url, is_new=is_new, is_updated=is_updated)


    def get_home_future_events_begin_end(self, link, key, ctx):
        """.. :py:method::
        :param link: link to upcoming page
        :param key: event id or department
        """
        if '/sale/children' in link or '/sale/women' in link or '/sale/men' in link:
            image, sale_title, sale_description, events_begin = self.get_picture_description(link, ctx)
            return events_begin, None, image, sale_description

        tree = self.download_page_get_correct_tree(link, key, 'download \'home\' upcoming event page error', ctx)
        timer = tree.cssselect('div.page-container > div.content-container > section.page-details > div.layout-background > div.layout-wrapper > div.layout-container > section.sale-details > div.sale-time')[0]
        _begin = timer.get('data-timer-start')
        events_begin = datetime.utcfromtimestamp(float(_begin[:10]))
        _end = timer.get('data-timer-end') # 1356714000000
        events_end = datetime.utcfromtimestamp(float(_end[:10]))
        bottom_node = timer = tree.cssselect('div.page-container > div.content-container > section.content > div > div.position > section.module > div.elements-container > article.element')[0]
        image = bottom_node.cssselect('figure > span > img')[0].get('src')
        image = image if image.startswith('http:') else 'http:' + image
        sale_description = bottom_node.cssselect('div.sharable-editorial > header.element-header > div.element-content')[0].text_content().strip()
        return events_begin, events_end, image, sale_description


#####################################################

    def crawl_listing(self, url, ctx='', **kwargs):
        """.. :py:method::
            crawl women, men, children listing page
            crawl home listing page
        """
        if kwargs.get('login_email'): self.net.check_signin( kwargs.get('login_email') )
        else: self.net.check_signin()

        product_ids = []
        event_id = url.rsplit('/', 1)[-1]
        tree = self.download_listing_page_get_correct_tree(url, event_id, 'download listing page error', ctx)
        if tree is None: return

        if '/home/sale' in url or '/sale/home' in url: # home
            timer = tree.cssselect('div.page-container > div.content-container > section.page-details > div.layout-background > div.layout-wrapper > div.layout-container > section.sale-details > div.sale-time')[0]
            _begin = timer.get('data-timer-start')
            events_begin = datetime.utcfromtimestamp(float(_begin[:10]))
            _end = timer.get('data-timer-end')
            events_end = datetime.utcfromtimestamp(float(_end[:10]))
            bottom_node = tree.cssselect('div.page-container > div.content-container > div.content-area-wrapper > section.content > div.position > section.module > div.elements-container > article.element')[0]
            image = bottom_node.cssselect('figure.element-media > span.media > img')[0].get('src')
            image = image if image.startswith('http:') else 'http:' + image
            sale_description = bottom_node.cssselect('div.promo-content-wrapper > header.element-header > div.element-content')[0].text_content().strip()

            product_ids = self.detect_rest_home_product(url, '', ctx)
        else: # women, men, children
            events_begin, image, sale_description = None, None, None
            try:
                _end = tree.cssselect('section#main > div > section.page-header-container  section.page-head-top  > div.clearfix > section.sale-countdown > time.sale-end-time')[0].get('datetime')
            except IndexError:
                data_gilt_time = tree.cssselect('span#shopInCountdown')[0].get('data-gilt-time')
                events_begin = self.gilt_time(data_gilt_time)
                event = Event.objects(event_id=event_id).first()
                if event.events_begin != events_begin:
                    event.update_history.update({ 'events_begin': datetime.utcnow() })
                    event.events_begin = events_begin
                    event.product_ids = []
                    event.save()
                return
            events_end = datetime.strptime(_end, '%Y-%m-%dT%XZ') # 2012-12-26T05:00:00Z

            nodes = tree.cssselect('section#main > div > section#product-listing > div.elements-container > article[id^="look-"]')
            for node in nodes:
                look_id, brand, link, title, price, listprice, soldout = self.parse_listing_one_product_node(node)
                self.get_or_create_product(ctx, event_id, link.rsplit('/', 1)[-1], link, title, listprice, price, brand, soldout)
                product_ids.append(link.rsplit('/', 1)[-1])

            ret = self.detect_rest_product(url, look_id, ctx)
            if ret: product_ids.extend( ret )

        event = Event.objects(event_id=event_id).first()
        if not event: event = Event(event_id=event_id)
        if events_begin:
            if event.events_begin != events_begin:
                event.update_history.update({ 'events_begin': datetime.utcnow() })
                event.events_begin = events_begin
        if event.events_end != events_end:
            event.update_history.update({ 'events_end': datetime.utcnow() })
            event.events_end = events_end
        if '/home/sale' in url or '/sale/home' in url: # home
            if not event.sale_description:
                event.sale_description = sale_description
            event.image_urls = [image]
        event.product_ids = product_ids
        event.save()
        if event.urgent == True:
            event.urgent = False
            event.update_time = datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, obj_type='Event', key=event_id, is_new=False, is_updated=False, ready=True)

    def download_listing_page_get_correct_tree(self, url, key, warning, ctx):
        """.. :py:method::
            women page will redirect to 'http://www.gilt.com/sale/women'
            They both have two </html>, 200 is random by me

        :param url: url of the page
        :param key: key of the event
        :param warning: if download error, warning raise
        """
        cont = self.net.fetch_listing_page(url)
        if cont is None or isinstance(cont, int):
            common_failed.send(sender=ctx, key=key, url=url,
                    reason='{0}: {1}'.format(warning, cont))
            return
        return self.get_correct_tree(cont)

    def get_or_create_product(self, ctx, event_id, key, link, title, listprice, price, brand, soldout, color='', sizes=[]):
        """.. :py:method::
        """
        is_new, is_updated = False, False
        product = Product.objects(key=key).first()
        if not product:
            is_new = True
            product = Product(key=key)
            product.combine_url = link
            product.updated = False
            product.title = title
            if listprice: product.listprice = listprice
            product.price = price
            product.brand = brand
            product.soldout = soldout
            if color: product.color = color
            if sizes: product.sizes = sizes
        else:
            if soldout != product.soldout:
                product.soldout = soldout
                is_updated = True
                product.update_history.update({ 'soldout': datetime.utcnow() })
            if product.combine_url != link:
                product.combine_url = link
                product.update_history.update({ 'combine_url': datetime.utcnow() })
            if product.price != price:
                product.price = price
                product.update_history.update({ 'price': datetime.utcnow() })
            if listprice and product.listprice != listprice:
                product.listprice = listprice
                product.update_history.update({ 'listprice': datetime.utcnow() })
        if event_id not in product.event_id: product.event_id.append(event_id)
        product.list_update_time = datetime.utcnow()
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=key, url=link, is_new=is_new, is_updated=is_updated)


    def parse_listing_one_product_node(self, node):
        """.. :py:method::
        """
        garbage, look_id = node.get('id').split('-')
        brand = node.cssselect('header.overview > hgroup.look-name > h2.brand-name > div.primary > div.favorite-tooltip-link > button.favorite-star-button')[0].get('data-gilt-brand-name').encode('utf-8')
        product_name = node.cssselect('header.overview > hgroup.look-name > h1.product-name > a')[0]
        link = product_name.get('href')
        link = link if link.startswith('http') else self.siteurl + link
        title = ' '.join( product_name.xpath('.//text()') )
        price = node.cssselect('header.overview > div.price > div.sale-price > span.nouveau-price')[0].text_content().replace('$', '').strip()
        listprice = node.cssselect('header.overview > div.price > div.original-price > span')
        listprice = listprice[0].text_content().replace('$', '').replace(',', '').strip() if listprice else ''
        soldout = True if 'Sold Out' == node.cssselect('section.inventory-status > h1.inventory-state')[0].text_content().strip() else False
        return look_id, brand, link, title, price, listprice, soldout


    def detect_rest_product(self, url, look_id, ctx):
        """.. :py:method::
            recursively detect whether there is still some products
        """
        cont = self.net.fetch_page('{0}?layout=f&angle=0&&ending_element_id={1}'.format(url, look_id))
        if cont is None or isinstance(cont, int):
            common_failed.send(sender=ctx, key=look_id, url=url,
                    reason='Download rest product of url error: {1}'.format(cont))
            return
        # The position is 111, if no more products get
        if cont.find('registerLooks') < 200:
            return

        product_ids = []
        tree = lxml.html.fromstring(cont)
        nodes = tree.cssselect('div.elements-container > article')
        for node in nodes:
            look_id, brand, link, title, price, listprice, soldout = self.parse_listing_one_product_node(node)
            self.get_or_create_product(ctx, url.rsplit('/', 1)[-1], link.rsplit('/', 1)[-1], link, title, listprice, price, brand, soldout)
            product_ids.append(link.rsplit('/', 1)[-1])


        ret = self.detect_rest_product(url, look_id, ctx)
        if ret: product_ids.extend(ret)
        return product_ids

    def detect_rest_home_product(self, url, look_id, ctx):
        """.. :py:method::
            recursively detect whether home listing page still have some products
        """
        if not look_id: # first time to get the listing product, there is no ending element
            link = '{0}?layout=f&grid-variant=new-grid&'.format(url)
        else:
            link = '{0}?layout=f&grid-variant=new-grid&&ending_element_id={1}'.format(url, look_id)
        cont = self.net.fetch_page(link)
        if cont is None or isinstance(cont, int):
            common_failed.send(sender=ctx, key=look_id, url=url,
                    reason='Download rest home product of url error: {0}'.format(cont))
            return
        # The position is 39, if no more products get
        if cont.find('requireModules') < 100:
            return

        product_ids = []
        tree = lxml.html.fromstring(cont)
        # "product-on-sale" is the only difference between two right pattern.
        # nodes = tree.cssselect('article.product-on-sale')
        nodes = tree.cssselect('article.in-flash-sale') # 'element-product' can have giltcity
        for node in nodes:
            look_id = node.get('data-home-look-id')
            text = node.cssselect('section.product-details > header > hgroup')[0]
            brand = text.cssselect('h3.product-brand')[0].text_content().strip()
            link = text.cssselect('h1.product-name > a')[0].get('href')
            link = link if link.startswith('http') else self.siteurl + link
            title = text.cssselect('h1.product-name > a')[0].text_content()
            listprice = node.cssselect('div.product-price > div.original-price')
            listprice = listprice[0].text_content().replace('$', '').replace(',', '').strip() if listprice else ''
            price = node.cssselect('div.product-price > div.gilt-price')[0].text_content().replace('$', '').replace('Gilt', '').strip()
            status = node.cssselect('section.product-details > section.inventory-status')
            soldout = True if status and 'Sold Out' in status[0].text_content() else False
            attribute = node.cssselect('div.quickadd-wrapper > section.quickadd > form.sku-selection')[0]
            attribute_color = attribute.cssselect('div[data-gilt-attribute-name=Color]')
            color = attribute_color[0].cssselect('ul.sku-attribute-values > li[data-gilt-value-name]')[0].get('data-gilt-value-name') if attribute_color else ''
            attribute_size = attribute.cssselect('div[data-gilt-attribute-name=Size]')
            sizes = []
            if attribute_size:
                for size in attribute_size[0].cssselect('ul.sku-attribute-values > li[data-gilt-value-name]'):
                    sizes.append( size.get('data-gilt-value-name') )

            self.get_or_create_product(ctx, url.rsplit('/', 1)[-1], link.rsplit('/', 1)[-1], link, title, listprice, price, brand, soldout, color, sizes)
            product_ids.append(link.rsplit('/', 1)[-1])
        ret = self.detect_rest_home_product(url, look_id, ctx)
        if ret: product_ids.extend(ret)
        return product_ids


#####################################################

    def crawl_product(self, url, ctx='', **kwargs):
        """.. :py:method::
        """
        if kwargs.get('login_email'): self.net.check_signin( kwargs.get('login_email') )
        else: self.net.check_signin()

        key = url.rsplit('/', 1)[-1]
        tree = self.download_product_page_get_correct_tree(url, url.rsplit('/', 1)[-1], 'download product page error', ctx)
        if tree is None:
            tree = self.download_product_page_get_correct_tree(url, url.rsplit('/', 1)[-1], 'download product page twice error', ctx)
        if tree is None: return

        if '/home/sale' in url or '/sale/home' in url: # home
            nav = tree.cssselect('div.page-container > div.content-container > section.content > div.layout-container > div.positions > div.position-2 > section.module > div.elements-container > article.element-product')[0]
            text = nav.cssselect('section.product-details')[0]
            shipping = 'Extended Delivery Timeline: ' + text.cssselect('div.delivery-estimate')[0].text_content().strip().replace('\n', ' ')
            returned = text.cssselect('div.return-policy')[0].text_content().strip()
            list_info = []
            detail = text.cssselect('section.product-description > div#PRODUCT_DETAILS')[0]
            lis = detail.xpath('.//li')
            if not lis: # make sure not miss 'ul'
                for i in detail.iterchildren():
                    list_info.append(i.text_content())
            else: # use 'li' and 'p' to fill list_info
                for i in lis:
                    list_info.append(i.text_content())
                for i in detail.xpath('p'):
                    list_info.append(i.text_content())
            use_care = text.cssselect('section.product-description > div#USE_AND_CARE')
            if use_care:
                list_info.append( use_care[0].text_content().strip() )

            image_urls = []
            for img in nav.cssselect('section.product-image > ul.photo-selection > li.photo > img'):
                image = img.get('src').rsplit('/', 1)[0] + '/lg.jpg'
                image = image if image.startswith('http:') else 'http:' + image
                image_urls.append(image)
            color, sizes = None, None
        else: # women, men, children
            nav = tree.cssselect('section#main > section#product-detail > article.product')[0]
            text = nav.cssselect('div.summary')[0]
            shipping = text.cssselect('div.details > dl.delivery > dd.delivery-window')
            shipping = 'Estimated Delivery: ' + shipping[0].text_content().strip().replace('\n', ' ') if shipping else ''
            returned = text.cssselect('div.details > dl.return-policy > dd')
            returned = returned[0].text_content().strip() if returned else ''
            list_info = []
            for desc in text.cssselect('div.structured-description > section.fragment'):
                desc_title = desc.cssselect('header.structure-title > h1')[0].text_content()
                if desc_title == 'Description':
                    for i in desc.cssselect('header.structure-title')[0].xpath('./following-sibling::*'):
                        list_info.append( i.text_content() )
                elif desc_title == 'Use and Care':
                    list_info.append( desc.text_content().replace('Use and Care', '').strip() )
                # elif desc_title == 'At a Glance':
                #     desc.text_content().replace('At a Glance', '').strip()
                # elif desc_title == 'Designer':
                #     desc.text_content().replace('Designer', '').strip()
            sizes = []
            for i in text.cssselect('form.sku-selection > div[data-gilt-attribute-name=Size] > ul.sku-attribute-values > li[data-gilt-value-name]'):
                sizes.append(i.get('data-gilt-value-name'))
            color = text.cssselect('form.sku-selection > div[data-gilt-attribute-name=Color] > dl.attribute-label > dd.selected-attribute-value')
            color = color[0].text_content().strip() if color else ''

            image_urls = []
            for img in nav.cssselect('div.photos > ul.photo-selection > li.photo > img'):
                image = img.get('src').rsplit('/', 1)[0] + '/lg.jpg'
                image = image if image.startswith('http:') else 'http:' + image
                image_urls.append(image)

        is_new, is_updated = False, False
        product = Product.objects(key=key).first()
        if not product:
            is_new = True
            product = Product(key=key)
        product.shipping = shipping
        product.returned = returned
        product.list_info = list_info
        if sizes: product.sizes = sizes
        if color: product.color = color
        product.image_urls = image_urls
        product.full_update_time = datetime.utcnow()

        if product.updated == False:
            product.updated = True
            ready = True
        else: ready = False
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=key, url=url, is_new=is_new, is_updated=is_updated, ready=ready)


    def download_product_page_get_correct_tree(self, url, key, warning, ctx):
        """.. :py:method::
            product page will redirect to its brand page 'http://www.gilt.com/brand/xxx'
            They both have two </html>, 200 is random by me

        :param url: url of the page
        :param key: key of the event
        :param warning: if download error, warning raise
        """
        cont = self.net.fetch_product_page(url)
        if cont is None or isinstance(cont, int):
            cont = self.net.fetch_product_page(url)
            if cont is None or isinstance(cont, int):
                common_failed.send(sender=ctx, key=key, url=url,
                        reason='{0}: {1}'.format(warning, cont))
                return
        return self.get_correct_tree(cont)


if __name__ == '__main__':
    server = Server()
    server.crawl_listing('http://www.gilt.com/home/sale/candle-blowout-7052')
