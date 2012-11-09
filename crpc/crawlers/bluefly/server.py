# -*- coding: utf-8 -*-
"""
crawlers.ruelala.server
~~~~~~~~~~~~~~~~~~~

This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.

"""

from gevent import monkey
monkey.patch_all()
from crawlers.common.baseserver import BaseServer

from selenium.common.exceptions import *
from selenium import webdriver
from crawlers.common.events import category_saved, category_failed, category_deleted
from crawlers.common.events import product_saved, product_failed, product_deleted

from models import *
from models import Event as Category
from crawlers.common.events import *
from crawlers.common.stash import *
import urllib
import lxml.html
import time
import datetime
from dateutil import parser as dt_parser
from crawlers.common.events import common_saved, common_failed

class Server(BaseServer):
    """.. :py:class:: Server
    This is zeroRPC server class for ec2 instance to crawl pages.
    """
    
    def __init__(self):
        self.siteurl = 'http://www.bluefly.com'
        self.site ='bluefly'
        self.browser = False
        self._signin = False
        #self.login(self.email, self.passwd)

    def bopen(self,url):
        """ open url with browser
        """
        if not self.browser:
            try:
                self.browser = webdriver.Chrome()
            except:
                self.browser = webdriver.Firefox()
                self.browser.set_page_load_timeout(10)


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
        # http://www.bluefly.com/Designer-Baby/_/N-v2ws/list.fly
        # http://www.bluefly.com/Designer-Handbags-Accessories/_/N-1abcZapsz/newarrivals.fly 
        # http://www.bluefly.com/Designer-Women/_/N-1pqkZapsz/Nao-288/newarrivals.fly
        m = re.compile('.*/_/(N-[a-z,A-Z,0-9]{1,20})/.*.fly').findall(href)
        return m[0]

    def _get_all_category(self,nav,url,ctx=False):
        tree = self.ropen(url)
        for div in tree.xpath('//div[@id="deptLeftnavContainer"]'):
            h3 = div.xpath('.//h3')[0].text_content()
            if h3 == 'categories':
                links = div.xpath('.//a')
                break
        # patch
        if nav.upper() == 'KIDS':
            links = tree.xpath('//span[@class="listCategoryItems"]/a')

        for a in links:
            href = a.get('href')
            url = self.format_url(href)
            print '>url',url
            _tree = self.ropen(url)
            cats = []
            for a in _tree.xpath('//div[@class="breadCrumbMargin"]/a'):
                cats.append(a.text)
            try:
                name = _tree.xpath('//div[@class="listPageHeader"]/h1')[0].text
            except IndexError:
                continue
            try:
                key = self.url2category_key(href)
            except IndexError:
                continue
            
            category ,is_new = Category.objects.get_or_create(key=key)
            if is_new:
                is_updated = False
            elif category.name == name:
                is_updated = False
            else:
                # TODO 
                print '>>'*10
                print 'key',category.key
                print 'old name',category.name
                category.name = name
                print 'save',category.save()
                print 'new name',category.name
                is_updated = False

            category.url = url
            category.cats = cats
            category.is_leaf = True
            category.save()
            common_saved.send(sender=ctx, site=DB, key=category.key, is_new=is_new, is_updated=is_updated)

    @exclusive_lock(DB)
    def crawl_category(self,ctx=False):
        """.. :py:method::
            From top depts, get all the events
        """
        for i in self.get_navs():
            nav,url = i
            print nav,url
            self._get_all_category(nav,url,ctx)
    
    @exclusive_lock(DB)
    def crawl_listing(self,url,ctx=''):
        self._crawl_listing(url,ctx)

    def _crawl_listing(self,url,ctx=''):
        print 'list url',url
        event_id = [self.url2category_key(url)]
        tree = self.ropen(url)
        for item in tree.xpath('//div[starts-with(@class,"productContainer")]'):
            link = item.xpath('.//div[@class="productShortName"]/a')[0]
            title = link.text
            href = link.get('href')
            key  = self.url2product_id(href)
            url = self.format_url(href)
            designer = item.xpath('.//div[@class="listBrand"]/a')[0].text_content()
            price_spans = item.xpath('.//span')
            listprice,price = '',''
            for span in price_spans:
                class_name = span.get('class')
                value = span.text.replace('\n','').replace(' ','')
                if class_name == 'priceRetailvalue':
                    listprice = value
                elif class_name == 'priceSalevalue':
                    price = value
                elif class_name =='priceReducedvalue' and not price:
                    price = value
                
            soldout = False
            for div in item.xpath('.//div'):
                if div.get('class') == 'listOutOfStock':
                    soldout = True
                    break

            product,is_new = Product.objects.get_or_create(pk=key)
            if is_new:
                is_updated = False
            elif product.soldout == soldout and product.title == title and product.price == price and product.listprice == listprice:
                is_updated = False
            else:
                print '>>>'*10
                print 'old price',product.price,product.title
                print 'new price',price,title
                is_updated = True

            if is_new:
                product.event_id = event_id
            else:
                product.event_id = list(set(product.event_id + event_id))

            product.title = title
            if price:product.price = price
            if listprice:product.listprice = listprice
            product.event_id = event_id
            product.soldout = soldout
            product.image_urls = ['http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img=%s.pct&outputx=738&outputy=700&level=1&ver=6' %key]
            product.url = url
            product.designer = designer

            try:
                product.save()
            except Exception,e:
                product.reviews = []
                product.save()
            common_saved.send(sender=ctx, site=DB, key=product.key, is_new=is_new, is_updated=is_updated)

        try:
            href = tree.xpath('//a[@class="next"]')[1].get('href')
        except IndexError:
            next_page_url = False
        else:
            next_page_url = self.format_url(href)
            print 'next page',next_page_url
            self._crawl_listing(next_page_url,ctx)

    def url2product_id(self,href):
        # http://www.bluefly.com/Kelsi-Dagger-tan-suede-Berti-studded-pointed-toe-flats/p/320294403/detail.fly
        m = re.compile('.*/p/(\d{1,15})/detail.fly').findall(href)
        return m[0]

    def _make_image_urls(self,product_key,image_count):
        urls = []
        for i in range(0,image_count):
            if i == 0:
                url = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img=%s.pct&outputx=738&outputy=700&level=1&ver=6' %product_key
            else:
                url = 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img=%s_alt0%s.pct&outputx=738&outputy=700&level=1&ver=6' %(product_key,i)

            urls.append(url)
        return urls

    @exclusive_lock(DB)
    def crawl_product(self,url,ctx=False):
        """.. :py:method::
            Got all the product basic information and save into the database
        """

        if not url:return
        if not self.browser:
            try:
                self.browser = webdriver.Chrome()
            except:
                self.browser = webdriver.Firefox()
                self.browser.set_page_load_timeout(10)

        #tree = self.ropen(url)
        self.browser.get(url)
        key = self.url2product_id(url)
        main = self.browser.find_element_by_css_selector('section#main-product-detail')
        title = main.find_element_by_xpath('//h2[starts-with(@class,"product-name")]').text
        list_info = [] 
        for li in main.find_elements_by_css_selector('ul.property-list li'):
            list_info.append(li.text)
        summary = main.find_element_by_css_selector('div.product-description').text
        try:
            shipping = main.find_element_by_css_selector('div.shipping-policy a').text
        except NoSuchElementException:
            shipping = ''

        try:
            returned  = main.find_element_by_css_selector('div.return-policy a').text
        except NoSuchElementException:
            returned = ''

        cats = []
        for a in self.browser.find_elements_by_css_selector('a.product-category'):
            cats.append(a.text)

        try:
            color =  main.find_element_by_xpath('//div[@class="pdp-label product-variation-label"]/em').text
        except NoSuchElementException:
            color = ''

        image_count = len(main.find_elements_by_css_selector('div.image-thumbnail-container a'))
        image_urls = self._make_image_urls(key,image_count)

        try:
            num_reviews = main.find_element_by_css_selector('a.review-count').text.split('reviews')[0]
        except NoSuchElementException:
            num_reviews = '0'
        
        sizes = []
        try:
            bt = self.browser.find_element_by_css_selector('span.selection')
            left = self.browser.find_element_by_css_selector('div.size-error-message').text
        except NoSuchElementException:
            pass
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

        product,is_new = Product.objects.get_or_create(key=key)
        if is_new:
            is_updated = False
        elif product.title == title:
            is_updated = False
        else:
            is_updated = True

        product.title = title
        if cats:product.cats = cats
        product.sizes_scarcity = sizes
        product.shipping = shipping
        product.summary = summary
        product.returned = returned
        product.color = color
        product.image_urls = image_urls
        product.updated = True

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
                    date_str = date_str[:-1].replace('?','-')
                date_obj = dt_parser.parse(date_str)
                review.post_time = date_obj
                review.username = self.browser.find_element_by_xpath('//div[@class="review-author"]/a').text
                review.save()
                reviews.append(review)
            if reviews:
                product.reviews = reviews

        try:
            product.save()
        except Exception,e:
            common_failed.send(sender=ctx, site=DB, key=product.key, is_new=is_new, is_updated=is_updated)
        else:
            common_saved.send(sender=ctx, site=DB, key=product.key, is_new=is_new, is_updated=is_updated)

if __name__ == '__main__':
    server = Server()
    import time
    #server.crawl_category()
    #server.crawl_listing('http://www.bluefly.com/Designer-Loafers-Flats/_/N-fs8/list.fly')
    #server._get_all_category('test','http://www.bluefly.com/a/shoes')
    print 'xxx',server.crawl_product('http://www.bluefly.com/Beyond-Rings-black-and-gold-druzy-ring/p/319923701/detail.fly')

