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
from crawlers.common.baseserver import BaseServer

from selenium.common.exceptions import *
from selenium import webdriver
from crawlers.common.events import category_saved, category_failed, category_deleted
from crawlers.common.events import product_saved, product_failed, product_deleted

from models import *
from crawlers.common.events import *
from crawlers.common.stash import *
import urllib
import lxml.html
import time
import datetime
from dateutil import parser as dt_parser

class Server(BaseServer):
    """.. :py:class:: Server
    This is zeroRPC server class for ec2 instance to crawl pages.
    """
    
    def __init__(self):
        self.siteurl = 'http://www.bluefly.com'
        self.site ='bluefly'
        #self.login(self.email, self.passwd)
        try:
            self.browser = webdriver.Chrome()
        except:
            self.browser = webdriver.Firefox()
            self.browser.set_page_load_timeout(10)

    def bopen(self,url):
        """ open url with browser
        """
        start = time.time()
        try:
            self.browser.get(url)
        except TimeoutException:
            return False
        else:
            #self.html = self.browser.content
            #self.tree = lxml.html.fromstring(self.html)
            print 'bopen used',time.time() - start
            return True

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

    def get_navs(self):
        result = []
        tree = self.ropen(self.siteurl)
        for a in tree.xpath('//ul[@id="siteNav1"]/li/a')[:-1]:
            name = a.text_content()
            href = a.get('href') 
            url = self.format_url(href)
            result.append((name,url))
        return result

    def url2category_key(self,href):
        return  href.split('/')[-2]

    def _get_all_category(self,nav,url,ctx=False):
        tree = self.ropen(url)
        for div in tree.xpath('//div[@id="deptLeftnavContainer"]'):
            h3 = div.xpath('.//h3')[0].text_content()
            if h3 == 'categories':
                links = div.xpath('.//ul/li/a')
                break
        # patch
        if nav.upper() == 'KIDS':
            links = tree.xpath('//span[@class="listCategoryItems"]/a')

        for a in links:
            href = a.get('href')
            name = a.text_content()
            url = self.format_url(href)
            key = self.url2category_key(href)
            
            category ,is_new = Category.objects.get_or_create(key=key)
            category.name = name
            category.url = url
            print 'category.url',url
            category.save()
            # send singnal
            if ctx:
                ctx.send(sender = 'bluefly.crawl_category',
                                site = self.site,
                                key = key,
                                is_new = is_new,
                                is_updated = not is_new)

    def crawl_category(self,ctx=False):
        """.. :py:method::
            From top depts, get all the events
        """
        for i in self.get_navs():
            nav,url = i
            print nav,url
            self._get_all_category(nav,url,ctx)
    
    def crawl_listing(self,url,ctx=False):
        tree = self.ropen(url)
        for item in tree.xpath('//div[starts-with(@class,"productContainer")]'):
            link = item.xpath('.//div[@class="productShortName"]/a')[0]
            title = link.text
            href = link.get('href')
            key  = self.url2product_id(href)
            url = self.format_url(href)
            sale_id = [self.url2category_key(url)]
            brand = item.xpath('.//div[@class="listBrand"]/a')[0].text_content()
            designer = link.text_content()
            print 'key',key,type(key)
            product,is_new = Product.objects.get_or_create(pk=key)

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

            if is_new:
                product.sale_id = sale_id
            else:
                product.sale_id = list(set(product.sale_id + sale_id))

            product.title = title
            product.soldout = soldout
            product.image_urls = ['http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img=%s.pct&outputx=738&outputy=700&level=1&ver=6' %key]
            try:
                product.save()
            except:
                product.reviews = []
                product.save()
            if ctx:
                ctx.send(sender = "bluefly.parse_listing", 
                                    site = self.site,
                                    key = product.key,
                                    is_new = is_new,                        
                                    is_updated = not is_new)

    def url2product_id(self,href):
        return href.split('/')[-2]

    def _make_image_urls(self,product_key,image_count):
        urls = []
        for i in range(0,image_count):
            if i == 0:
                url = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img=%s.pct&outputx=738&outputy=700&level=1&ver=6' %product_key
            else:
                url = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img=%s_alt0%s.pct&outputx=738&outputy=700&level=1&ver=6' %(product_key,i)

            urls.append(url)
        return urls

    def crawl_product(self,url,ctx=False):
        """.. :py:method::
            Got all the product basic information and save into the database
        """
        print 'start parse product ',url
        point1 = time.time()
        #tree = self.ropen(url)
        self.bopen(url)
        key = self.url2product_id(url)
        main = self.browser.find_element_by_css_selector('section#main-product-detail')
        product,is_new = Product.objects.get_or_create(key=key)
        product.title = main.find_element_by_xpath('//h2[starts-with(@class,"product-name")]').text

        list_info = [] 
        for li in main.find_elements_by_css_selector('ul.property-list li'):
            list_info.append(li.text)

        product.summary = main.find_element_by_css_selector('div.product-description').text
        try:
            product.shipping = main.find_element_by_css_selector('div.shipping-policy a').text
        except NoSuchElementException:
            pass

        try:
            product.returned  = main.find_element_by_css_selector('div.return-policy a').text
        except NoSuchElementException:
            pass

        try:
            product.color =  main.find_element_by_xpath('//div[@class="pdp-label product-variation-label"]/em').text
        except NoSuchElementException:
            pass

        image_count = len(main.find_elements_by_css_selector('div.image-thumbnail-container a'))
        product.image_urls = self._make_image_urls(key,image_count)
        try:
            num_reviews = main.find_element_by_css_selector('a.review-count').text.split('reviews')[0]
        except NoSuchElementException:
            num_reviews = '0'
        
        point2 = time.time()
        sizes = []
        try:
            bt = self.browser.find_element_by_css_selector('span.selection')
        except NoSuchElementException:
            left = self.browser.find_element_by_css_selector('div.size-error-message').text
            sizes = [('',left)]
        else:
            for li in self.browser.find_elements_by_css_selector('div.size-picker ul.product-size li'):
                bt.click()
                size = li.get_attribute('data-size')
                if li.get_attribute("class") == 'size-sku-waitlist':
                    continue
                else:
                    # find the left count
                    try:
                        if li.is_displayed():
                            li.click()
                            left = self.browser.find_element_by_css_selector('span.size-info').text
                        else:
                            continue
                    except NoSuchElementException:
                        i = (size,'')
                    else:
                        i = (size,left)
                    sizes.append(i)

        product.sizes = sizes
        # if not have now reviews,do nothing
        if not is_new and product.num_reviews == num_reviews:
            pass
        else:
            product.num_reviews = num_reviews
            reviews = []
            main = self.browser.find_element_by_xpath('//div[@class="ratings-reviews active"]')
            try:
                show_more = self.browser.find_element_by_link_text('SHOW MORE')
            except NoSuchElementException:
                show_more = False

            if show_more:
                show_more.click()

            # remove the old reviews
            Review.objects.filter(product_key=key).delete()
            for article in main.find_elements_by_tag_name('article'):
                review = Review()
                review.title = self.browser.find_element_by_xpath('//h5[@class="review-title"]').text
                review.content =  self.browser.find_element_by_xpath('//div[@class="text-preview"]').text
                date_str=  self.browser.find_element_by_xpath('//div[@class="review-date"]').text
                # patch
                if '?' in date_str:
                    date_str = date_str[:-1]
                date_obj = dt_parser.parse(date_str)
                review.post_time = date_obj
                review.username = self.browser.find_element_by_xpath('//div[@class="review-author"]/a').text
                review.save()
                reviews.append(review)
            print 'reviews',reviews
            if reviews:
                product.reviews = reviews

        print 'parse by seleunim used ',time.time() - point2
        product.save()
        print 'parse product total used',time.time() - point1
        if ctx:
            ctx.send(sender=DB + '.parse_product_detail', site=DB, key=product.key, is_new=is_new, is_updated=not is_new)


if __name__ == '__main__':
    server = Server()
    import time
    #server._get_all_category('test','http://www.bluefly.com/a/shoes')
    if 0:
        pass

    if 0:
        point1 = time.time()
        #server.crawl_category()
        print 'category count',Category.objects.all().count()
        print 'parse category used',time.time() - point1
        
        point2 = time.time()
        for c in Category.objects.all():
            print 'c.url',c.url
            server.crawl_listing(c.url)

        point3 = time.time()
        total_count = Product.objects.all().count()
        print '>>>total time',time.time() - point1
        print '>>total product',total_count

        count = 0
        for p in Product.objects.all():
            server.crawl_product(p.url)
            count += 1 
            print 'total product',total_count
            print 'parsed product ',count
            print 'parse product detail used time',time.time() - point3

        print 'crawl all lising used',time.time() - point3
        print '>>end'
        print 'total time',time.time() - point1

        #print server.get_navs()
    if 1:
        for c in Category.objects.all():
            url = c.url
            print '>>>> url',url
            url = 'http://www.bluefly.com/Designer-Leggings/_/N-fkg/list.fly'
            print server.crawl_listing(url)
    if 0:
        url = 'http://www.bluefly.com/Charles-David-black-leather-Proper-tall-boots/p/314091701/detail.fly'
        print server.crawl_product(url)

