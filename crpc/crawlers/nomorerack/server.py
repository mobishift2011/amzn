# -*- coding: utf-8 -*-
"""
crawlers.ruelala.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""

from gevent import monkey
monkey.patch_all()
from gevent.coros import Semaphore
lock = Semaphore()
from crawlers.common.rpcserver import BaseServer

from selenium.common.exceptions import *
from crawlers.common.events import category_saved, category_failed, category_deleted
from crawlers.common.events import product_saved, product_failed, product_deleted

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *
import urllib
import lxml.html
import time
import datetime

class Server(BaseServer):
    """.. :py:class:: Server
    This is zeroRPC server class for ec2 instance to crawl pages.
    """
    
    def __init__(self):
        self.siteurl = 'http://www.nomorerack.com'
        self.site ='nomorerack'
        #self.login(self.email, self.passwd)

    def login(self, email=None, passwd=None):
        """.. :py:method::
            login urelala

        :param email: login email
        :param passwd: login passwd
        """
        
        #self.browser.implicitly_wait(2)
        self.browser.get(self.siteurl)
        time.sleep(3)
        
        # click the login link
        node = self.browser.find_element_by_id('pendingTab')
        node.click()
        time.sleep(2)

        a = self.browser.find_element_by_id('txtEmailLogin')
        a.click()
        a.send_keys(email)

        b = self.browser.find_element_by_id('txtPass')
        b.click()
        b.send_keys(passwd)

        signin_button = self.browser.find_element_by_id('btnEnter')
        signin_button.click()

        title = self.browser.find_element_by_xpath('//title').text
        if title  == 'Rue La La - Boutiques':
            self._signin = True
        else:
            self._signin = False

    def crawl_category(self):
        """.. :py:method::
            From top depts, get all the events
        """
        ###########################
        # section 1, parse events
        ###########################
        self.bopen(self.siteurl)
        for e in self.browser.find_elements_by_css_selector('div.event'):
            title = e.text
            if title == 'VIEW EVENT':
                continue

            a =  e.find_element_by_css_selector('div.image a.image_tag')
            expires_on = e.find_element_by_css_selector('div.countdown').get_attribute('expires_on')
            date_obj = datetime.datetime.fromtimestamp(int(expires_on[:10]))
            href = a.get_attribute('href')
            url = self.format_url(href)
            sale_id = self.url2sale_id(url) # return a string
            img_url = 'http://nmr.allcdn.net/images/events/all/banners/event-%s-medium.jpg' %sale_id
            event ,is_new = Event.objects.get_or_create(sale_id=sale_id)
            event.title = title
            event.image_urls = [img_url]
            event.events_end = date_obj
            event.save()
            category_saved.send(sender=DB + '.crawl_category1', site=DB, key=sale_id, is_new=is_new, is_updated=not is_new)

        ###########################
        # section 2, parse category
        ###########################
        categorys = ['women','men','home','electronics','kids','lifestyle']
        for name in categorys:
            url = 'http://nomorerack.com/daily_deals/category/%s' %name
            category ,is_new = Category.objects.get_or_create(key=name)
            category_saved.send(sender=DB + '.crawl_category2', site=DB, key=name, is_new=is_new, is_updated=not is_new)

    def url2sale_id(self,url):
        return url.split('/')[-1]
    
    def crawl_listing(self,url):
        tree = self.ropen(url)
        for item in tree.xpath('//div[starts-with(@class,"productContainer")]'):
            link = item.xpath('.//div[@class="productShortName"]/a')[0]
            href = link.get('href')
            key  = self.url2product_id(href)
            url = self.format_url(href)
            product,is_new = Product.objects.get_or_create(pk=key)

            if is_new:
                product.brand = item.xpath('.//div[@class="listBrand"]/a')[0].text_content()
                product.sail_id = self.url2category_key(url)
                product.designer = link.text_content()

            price_spans = item.xpath('.//span')
            for span in price_spans:
                class_name = span.get('class')
                value = span.text.replace('\n','').replace(' ','')
                if class_name == 'priceRetailvalue':
                    product.listprice = value
                elif class_name == 'priceBlueflyFinalvalue':
                    product.price = value
                elif class_name == 'priceBlueflyvalue':
                    product.bluefly_price =  value
                
            soldout = False
            for div in item.xpath('.//div'):
                if div.get('class') == 'listOutOfStock':
                    soldout = True
                    break
            product.soldout = soldout
            product.image_urls = ['http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img=%s.pct&outputx=738&outputy=700&level=1&ver=6' %key]
            debug_info.send(sender=DB + str(product.image_urls))
            try:
                product.save()
            except:
                raise ValueError("validation failed")
            else:
                product_saved.send(sender = "bluefly.parse_listing", 
                                    site = self.site,
                                    key = product.key,
                                    is_new = is_new,                        
                                    is_updated = not is_new)

    def crawl_product(self,url):
        """.. :py:method::
            Got all the product basic information and save into the database
        """
        point1 = time.time()

        tree = self.ropen(url)
        key = self.url2product_id(url)
        main = tree.xpath('//section[@id="main-product-detail"]')[0]
        product,is_new = Product.objects.get_or_create(key=key)

        product.title = main.xpath('//h2[starts-with(@class,"product-name")]')[0].text
        list_info = [] 
        for li in main.xpath('//ul[@class="property-list"]/li'):
            list_info.append(li.text)

        product.summary = main.xpath('//div[@class="product-description"]')[0].text
        product.shipping = main.xpath('//div[@class="shipping-policy"]/a')[0].text
        product.returned  = main.xpath('//div[@class="return-policy"]/a')[0].text
        product.color =  main.xpath('//div[@class="pdp-label product-variation-label"]/em')[0].text
        image_count = len(main.xpath('//div[@class="image-thumbnail-container"]/a'))
        product.image_urls = self._make_image_urls(key,image_count)
        num_reviews = main.xpath('//a[@class="review-count"]')[0].text.split('reviews')[0]
        print 'parse by request,used ',time.time() - point1
        
        ########################
        # section 2
        ########################

        point2 = time.time()
        self.bopen(url)
        sizes = []
        for li in self.browser.find_elements_by_css_selector('div.size-picker ul.product-size li'):
            size = li.get_attribute('data-size')
            if li.get_attribute("class") == 'size-sku-waitlist':
                continue
            else:
                sizes.append(size)
        product.sizes = sizes
        
        # if not have now reviews,do nothing
        if not is_new and product.num_reviews == num_reviews:
            return
        
        product.num_reviews = num_reviews
        Review.objects.filter(product_key=key).delete()
        reviews = []
        main = self.browser.find_element_by_xpath('//div[@class="ratings-reviews active"]')
        show_more = self.browser.find_element_by_link_text('SHOW MORE').click()
        if show_more:
            show_more.click()

        for article in main.find_elements_by_tag_name('article'):
            review = Review()
            review.title = self.browser.find_element_by_xpath('//h5[@class="review-title"]').text
            review.content =  self.browser.find_element_by_xpath('//div[@class="text-preview"]').text
            post_time =  self.browser.find_element_by_xpath('//div[@class="review-date"]').text.replace('?','-')[:-1]
            review.post_time = dt_parser.parse(post_time)
            review.username = self.browser.find_element_by_xpath('//div[@class="review-author"]/a').text
            review.save()
            reviews.append(review)

        print 'parse by seleunim used ',time.time() - point2
        product.save()
        print 'parse product total used',time.time() - point1
        product_saved.send(sender=DB + '.parse_product_detail', site=DB, key=product.key, is_new=is_new, is_updated=not is_new)


if __name__ == '__main__':
    server = Server()
    server.crawl_category()

    import time
