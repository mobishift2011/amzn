#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

crawlers.ruelala.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""
from gevent import monkey
monkey.patch_all()
import os
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support.ui import WebDriverWait
#selenium.webdriver.support.wait.POLL_FREQUENCY = 0.05

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *
from crawlers.common.events import common_saved, common_failed
import lxml.html
import datetime
import time
import urllib
import re

class Server:
    """.. :py:class:: Server
    
    This is zeroRPC server class for ec2 instance to crawl pages.

    """
    
    def __init__(self):
        self.siteurl = 'http://www.ruelala.com'
        self._signin = False

    def get_page(self,url):
        start = time.time()
        try:
            self.browser.get(url)
        except TimeoutException:
            print 'time out >> ',url
            return False
        else:
            print 'load page used:',time.time() - start
            return True

    def logout(self):
        self._signin = False
        self.browser.quit()
#        url = 'http://www.ruelala.com/access/logout'
#        self.browser.get(url)

    def login(self):
        """.. :py:method::
            login urelala
        """
        if self._signin:
            return
        
        self.browser = webdriver.Chrome()
        #self.browser.set_page_load_timeout(10)
        #self.profile = webdriver.FirefoxProfile()
        #self.profile.set_preference("general.useragent.override","Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3")

        self.browser.get('http://www.ruelala.com/event/showReminders')
        time.sleep(1)
        
        # click the login link
        node = self.browser.find_element_by_css_selector('div.homeTabs a#pendingTab')
        node.click()
        time.sleep(1)

        try:
            login_node = self.browser.find_element_by_css_selector('div#loginContainer form#loginHome')
        except NoSuchElementException:
            time.sleep(1)
            login_node = self.browser.find_element_by_css_selector('div#loginContainer form#loginHome')

        a = login_node.find_element_by_css_selector('div.loginRow input#txtEmailLogin')
        a.click()
        a.send_keys(login_email)

        b = login_node.find_element_by_css_selector('div.loginRow input#txtPass')
        b.click()
        b.send_keys(login_passwd)

        signin_button = login_node.find_element_by_css_selector('div.loginRow input#btnEnter')
        signin_button.click()

        if self.browser.title  == 'Rue La La - Show Reminders':
            self._signin = True
        else:
            self._signin = False


    @exclusive_lock(DB)
    def crawl_category(self,ctx=False):
        """.. :py:method::
            From top depts, get all the events
        """
        self.login()

        categorys = ['women', 'men', 'living', 'kids', 'gifts']
        for category in categorys:
            url = 'http://www.ruelala.com/category/{0}'.format(category)
            if category == 'gifts':
                self._get_gifts_event_list(category, url, ctx)
            else:
                self._get_event_list(category,url,ctx)

#        local = ['boston', 'chicago', 'los-angeles', 'new-york-city', 'philadelphia', 'san-francisco', 'seattle', 'washington-dc', ]
#        for category in local:
#            url = 'http://www.ruelala.com/local/{0}'.format(category)
#            self._get_event_list(category, url, ctx)


    def _get_gifts_event_list(self, category_name, url, ctx):
        """.. :py:method::
            Get gifts events, these events have no time.
            
            Problem may exist: these events off sale, update_listing will get nothing.
        """
        self.get_page(url)
        browser = lxml.html.fromstring(self.browser.page_source)
        nodes = browser.cssselect('body > div.container > div#canvasContainer > section#gift-center > div#gc-wrapper a[href]')
        if len(nodes) == 0 or not nodes:
            time.sleep(1)
            browser = lxml.html.fromstring(slef.browser.page_source)
            nodes = browser.cssselect('body > div.container > div#canvasContainer > section#gift-center > div#gc-wrapper a[href]')

        for node in nodes:
            l = node.get('href')
            event_id = l.rsplit('/', 1)[-1]
            link = l if l.startswith('http') else self.siteurl + l
            event, is_new = Event.objects.get_or_create(event_id=event_id)
            if is_new:
                event.combine_url = link
                event.dept = [category_name]
                event.urgent = True
            event.update_time = datetime.datetime.utcnow()
            event.save()
            common_saved.send(sender=ctx, site=DB, key=event_id, is_new=is_new, is_updated=False)


    def get_end_time(self, str):
        # str == u'2\xa0Days,\xa012:46:00'
        m = re.compile('.*(\d{1,2})\xa0Day.*,\xa0(\d{1,2}):(\d{1,2}):(\d{1,2})').findall(str)
        # print 're.m',m
        # print 're.str[%s]' %str
        days,hours,minutes,seconds = m[0]
        now = datetime.datetime.utcnow()
        delta = datetime.timedelta(days=int(days),hours=int(hours),minutes=int(minutes),seconds=int(seconds))
        d = now + delta
        # print 'd>',d
        #ensure the end date is precise 
        if d.minute == 0:
            return datetime.datetime(d.year,d.month,d.day,d.hour,0,0)
        elif 50 <= d.minute <= 59:
            return datetime.datetime(d.year,d.month,d.day,d.hour+1,0,0)


    def _get_event_list(self, category_name, url, ctx):
        """.. :py:method::
            Get all the events from event list.
        """
        self.get_page(url)
        browser = lxml.html.fromstring(self.browser.page_source)
        nodes = browser.cssselect('body.wl-default > div.container > div#categoryMain > section#categoryDoors > article[id^="event-"]')
        if len(nodes) == 0 or not nodes:
            time.sleep(1)
            browser = lxml.html.fromstring(self.browser.page_source)
            nodes = browser.cssselect('body.wl-default > div.container > div#categoryMain > section#categoryDoors > article[id^="event-"]')

        for node in nodes:
            link = node.cssselect('a.eventDoorLink')[0].get('href')
            event_id = link.rsplit('/', 1)[-1]
            link = link if link.startswith('http') else self.siteurl + link
            title = node.cssselect('footer.eventFooter > a.eventDoorContent > div.eventName')[0].text
            clock_css = 'footer.eventFooter span#clock{0}'.format(event_id)
            clock  = node.cssselect(clock_css)
            if clock:
                end_time = self.get_end_time(clock[0].text)
            else:
                end_time = False
            
            event,is_new = Event.objects.get_or_create(event_id=event_id)
            if is_new:
                sm = 'http://www.ruelala.com/images/content/events/{event_id}/{event_id}_doorsm.jpg'.format(event_id=event_id)
                lg = 'http://www.ruelala.com/images/content/events/{event_id}/{event_id}_doorlg.jpg'.format(event_id=event_id)
                event.image_urls = [sm, lg]
                event.dept = [category_name]
                event.urgent = True
                event.combine_url = a_url

            if end_time: event.events_end = end_time
            event.update_time = datetime.datetime.utcnow()
            event.sale_title = a_title[0].text
            event.save()
            common_saved.send(sender=ctx, site=DB, key=event_id, is_new=is_new, is_updated=False)


    def is_parent_event(self, url, ctx='')
        self.get_page(url)
        browser = lxml.html.fromstring(self.browser.page_source)
        nodes = browser.cssselect('div#main > div#productContainerThreeUp > div#productGrid > article.product')
        if not nodes:
            nodes = browser.cssselect('div#main > section#experienceParentWrapper > section#children > article[id^="event-"]')
            for node in nodes:
                link = node.cssselect('a.eventDoorLink')[0].get('href')
                event_id = link.rsplit('/', 1)[-1]
                link = link if link.startswith('http') else self.siteurl + link
                title = node.cssselect('footer.eventFooter > a.eventDoorContent > div.eventName')[0].text
                clock_css = 'footer.eventFooter span#clock{0}'.format(event_id)
                clock  = node.cssselect(clock_css)
                if clock:
                    end_time = self.get_end_time(clock[0].text)
                else:
                    end_time = False


    @exclusive_lock(DB)
    def crawl_listing(self,url,ctx=''):
        self._crawl_listing(url,ctx)

    def _crawl_listing(self,url,ctx):
        event_url = url
        event_id = self._url2saleid(event_url)
        self.login()
        self.get_page(event_url)
#        try:
#            span = self.browser.find_element_by_css_selector('div.container > div#productContainerThreeUp div#pagination > span.viewAll')
#        except:
#            pass
#        else:
#            try:
#                span.click()
#                time.sleep(1)
#            except selenium.common.exceptions.WebDriverException:
#                # just have 1 page
#                pass
#
        browser = lxml.html.fromstring(self.browser.page_source)
        nodes = browser.cssselect('div#main > div#productContainerThreeUp > div#productGrid > article.product')
#            nodes = browser.xpath('//article[@class="column eventDoor halfDoor grid-one-third alpha"]')
        if len(nodes) == 0 or not nodes:
            time.sleep(1)
            browser = lxml.html.fromstring(self.browser.page_source)
            nodes = browser.cssselect('div#main > div#productContainerThreeUp > div#productGrid > article.product')

#        if not nodes:
#
#            #patch 1:
#            #some event url (like:http://www.ruelala.com/event/57961) will 301 redirect to product detail page:
#            #http://www.ruelala.com/product/detail/eventId/57961/styleNum/4112913877/viewAll/0
#            url_301 = self.browser.current_url
#            if url_301 <>  event_url:
#                print '301,',url_301
#                self._crawl_product(url_301,ctx)
#            else:
#                raise ValueError('can not find product @url:%s sale id:%s' %(event_url, event_id))

        for node in nodes:
#            if not node.is_displayed(): continue
            href = node.xpath('./a/@href')[0]

#            # patch 2
#            # the event have some sub events
#            if href.split('/')[-2] == 'event':
#                self._crawl_listing(self.format_url(href),ctx)
#                continue

            title = node.xpath('./a/img/@alt')[0]
            url = self.format_url(href)
            product_id = self._url2product_id(url)
            strike_price = node.xpath('./div/span[@class="strikePrice"]')
            strike_price = strike_price[0].text if strike_price else ''
            product_price = node.xpath('./div/span[@class="productPrice"]')
            product_price = product_price[0].text if product_price else ''
            scarcity = node.xpath('./div/em[@class="childWarning"]')
            scarcity = scarcity[0].text if scarcity else ''
            soldout = node.cssselect('a span.soldOutOverlay')
            soldout = True if soldout else False

            # get base product info
            product,is_new = Product.objects.get_or_create(key=product_id)
            is_updated = False
            if is_new:
                product.event_id = [event_id]
                product.price = product_price
                product.list_price = strike_price
                product.combine_url = url
                product.updated = False
                if soldout: product.soldout = soldout
            else:
                if product.price != product_price or product.listprice != strike_price:
                    product.price = product_price
                    product.list_price = strike_price
                    is_updated = True
                if soldout and product.soldout != True:
                    product.soldout = soldout
                    is_updated = True
                if event_id not in product.event_id: product.event_id.append(event_id)

            product.title = title
            product.save()
            common_saved.send(sender=ctx, site=DB, key=product.key, is_new=is_new, is_updated=is_updated)

        event = Event.objects(event_id=event_id).first()
        event.urgent = False
        event.save()


    def _make_img_urls(slef, product_key, img_count):
        """
        the keyworld `RLLZ` in url  meaning large size(about 800*1000), `RLLD` meaning small size (about 400 *500)
        http://www.ruelala.com/images/product/131385/1313856984_RLLZ_1.jpg
        http://www.ruelala.com/images/product/131385/1313856984_RLLZ_2.jpg

        http://www.ruelala.com/images/product/131385/1313856984_RLLZ_1.jpg
        http://www.ruelala.com/images/product/131385/1313856984_RLLZ_2.jpg
        """
        urls = []
        prefix = 'http://www.ruelala.com/images/product/'
        for i in range(0, img_count):
            subfix = '%s/%s_RLLZ_%d.jpg' %(product_key[:6], product_key, i+1)
            url = urllib.basejoin(prefix, subfix)
            urls.append(url)
        return urls

    @exclusive_lock(DB)
    def crawl_product(self,url,ctx=''):
        self._crawl_product(url,ctx)

    def _crawl_product(self,url,ctx=''):
        """.. :py:method::
            Got all the product basic information and save into the database
        """
        self.login()
        product_id = self._url2product_id(url)
        self.get_page(url)
        browser = lxml.html.fromstring(self.browser)
        node = browser.cssselect('div.container section#productContainer')[0]

        img_nodes = node.cssselect('section#productImages div#imageViews img.productThumb')
        img_count = len(img_nodes) if img_nodes else 1
        image_urls = self._make_img_urls(product_id, img_count)

        list_info = []
        for li in node.cssselect('section#info ul li'):
            list_info.append(li.text_content())
        returned = []
        for p in node.cssselect('section#shipping'):
            returned.append(p.text_content())

        
        #########################
        # section 2 productAttributes
        #########################
        
        attribute_node = node.cssselect('section#productAttributes')[0]
        size_list = attribute_node.cssselect('section#productSelectors ul#sizeSwatches li.swatch a')
        sizes = [s.text for s in size_list] if size_list else []
#        if size_list:
#            for a in size_list:
#                a.click()
#                key = a.text
#                left = ''
#                span = attribute_node.find_element_by_id('inventoryAvailable')
#                left = span.text.split(' ')[0]
#                sizes.append((key,left))
#        else:
#            try:
#                left =  attribute_node.find_element_by_css_selector('span#inventoryAvailable.active').text
#            except NoSuchElementException:
#                pass
#        price = attribute_node.find_element_by_id('salePrice').text
#        listprice  = attribute_node.find_element_by_id('strikePrice').text
        shipping = attribute_node.cssselect('div#readyToShip')
        shipping = shipping.text_content() if shipping else ''
        limit = attribute_node.cssselect('div#cartLimit')
        limit = limit[0].text_content() if limit else ''
        ship_rule = attribute_node.cssselect('div#returnsLink ')
        ship_rule = ship_rule[0].text_content() if ship_rule else ''
        color = attribute_node.cssselect('section#productSelectors ul#colorSwatches > li > a')
        color = [c.get('title') for c in color] if color else []


        product, is_new = Product.objects.get_or_create(key=product_id)
        product.image_urls = image_urls
        product.list_info = list_info
        product.returned = '; '.join(returned)
        product.sizes = sizes
        product.shipping = shipping
        product.limit = limit
        product.ship_rule = ship_rule
        product.color = color
        product.updated = True
        product.full_update_time = datetime.datetime.utcnow()
        product.save()
        common_saved.send(sender=ctx, site=DB, key=product.key, is_new=is_new, is_updated=not is_new)

    def _url2saleid(self, url):
        """.. :py:method::

        :param url: the brand's url
        :rtype: string of sale_id
        """
        m = re.compile('.*/event/(\d{1,10})').findall(url)
        return str(m[0])

    def _url2product_id(self, url):
        # http://www.ruelala.com/event/product/60118/1411878707/0/DEFAULT
        # or http://www.ruelala.com/product/detail/eventId/59935/styleNum/4112936424/viewAll/0
        m = re.compile('http://.*ruelala.com/event/product/\d{1,10}/(\d{6,10})/\d{1}/DEFAULT').search(url)
        if not m:
            m = re.compile('http://.*.ruelala.com/product/detail/eventId/\d{1,10}/styleNum/(\d{1,10})/viewAll/0').search(url)
        return m.group(1)


    def format_url(self,url):
        """
        ensure the url is start with `http://www.xxx.com`
        """
        if url.startswith('http://'):
            return url
        else:
            s = urllib.basejoin(self.siteurl,url)
            return s

if __name__ == '__main__':
    server = Server()
    #server.crawl_listing('http://www.ruelala.com/event/59935')
    url = 'http://www.ruelala.com/event/product/60496/6020835935/1/DEFAULT'
    server.crawl_product(url)
