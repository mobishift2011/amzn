# -*- coding: utf-8 -*-
"""
crawlers.bluefly.target_price
~~~~~~~~~~~~~~~~~~~
This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.
"""

from gevent import monkey; monkey.patch_all()
import lxml.html
import urllib
from datetime import datetime, timedelta
import itertools

from crawlers.common.stash import *

NUM_PER_PAGE = 48

class Server(object):
    """.. :py:class:: Server
        This is zeroRPC server class for ec2 instance to crawl bluefly.
    """
    
    def __init__(self):
        """
            http://www.bluefly.com/_/N-1aaq/list.fly
            This url can crawl all products in bluefly.
        """
        self.siteurl = 'http://www.bluefly.com'
        self.category_url = set()

        self.extract_slug_key_of_listingurl = re.compile(r'.*/(.+)/_/N-(.+)/list.fly')
        self.extract_category_key = re.compile(r'http://www.bluefly.com/_/N-(.+)/list.fly')
        self.extract_product_slug_key = re.compile(r'http://www.bluefly.com/(.+)/p/(.+)/detail.fly')
        self.extract_large_image = re.compile(".*smallimage: \'(.+?outputx=)(\d+)(&outputy=)(\d+)(&.+?)\'")

    def crawl_category(self, ctx='', **kwargs):
        """.. :py:method::
        """
        women_url = 'http://www.bluefly.com/a/women-clothing'
        shoes_url = 'http://www.bluefly.com/a/shoes'
        handbags_accessories_url = 'http://www.bluefly.com/a/handbags-accessories'
        jewelry_url = 'http://www.bluefly.com/a/jewelry-shop'
        beauty_url = 'http://www.bluefly.com/a/beauty-fragrance'
        men_url = 'http://www.bluefly.com/a/men-clothing-shoes-accessories'
        sale_url = 'http://www.bluefly.com/a/designer-sale'
        kids_url = 'http://www.bluefly.com/Designer-Kids/_/N-v2wq/list.fly'
        new_url = 'http://www.bluefly.com/New-Arrivals/_/N-1aaqZapsz/newarrivals.fly'

        self.crawl_women_shoes_handbags_category('women', women_url, ctx)
        self.crawl_women_shoes_handbags_category('shoes', shoes_url, ctx)
        self.crawl_women_shoes_handbags_category('handbags&accessories', handbags_accessories_url, ctx)
        self.crawl_jewelry_category('jewelry', jewelry_url, ctx)
        self.crawl_women_shoes_handbags_category('beauty', beauty_url, ctx)
        self.crawl_women_shoes_handbags_category('men', men_url, ctx)
        self.crawl_kids_category('kids', kids_url, ctx)
        self.crawl_newarrivals_category('new', new_url, ctx)
        self.crawl_sale_category('sale', sale_url, ctx)

        # add some more products, like La Perla
        self.category_url.add('http://www.bluefly.com/Designer-Beauty-Fragrance/_/N-nd52/list.fly')

        self.crawl_designer_brand_page('designer', 'http://www.bluefly.com/designers.fly', ctx)


    def download_category_return_xmltree(self, category, url, ctx):
        """.. :py:method::
            common download in crawl_category
        """
        content = fetch_page(url)
        if content is None or isinstance(content, int):
            return
        tree = lxml.html.fromstring(content)
        return tree

    def crawl_women_shoes_handbags_category(self, category, url, ctx):
        tree = self.download_category_return_xmltree(category, url, ctx)
        if tree is None: return
        navigation = tree.cssselect('div#leftDeptColumn div.dept-nav-section')[0]
        node1 = navigation.cssselect('ul li a')
        navigation = tree.cssselect('div#leftDeptColumn div.dept-nav-section')[-1]
        node2 = navigation.cssselect('ul li a')
        for i in itertools.chain(node1, node2):
            directory = i.text_content().strip()
            if directory == 'Best of Sale':
                continue
            link = i.get('href')
            if 'newarrivals.fly' in link:
                continue
            link = link if link.startswith('http') else self.siteurl + link
            m = self.extract_slug_key_of_listingurl.match(link)
            if not m: continue
            slug, key = m.groups()
            cats = [category, directory]

            combine_url = '{0}/_/N-{1}/list.fly'.format(self.siteurl, key)
            self.category_url.add(combine_url)



    def crawl_handbag_accessories_category(self, category, url, ctx):
        tree = self.download_category_return_xmltree(category, url, ctx)
        if tree is None: return
        navigation = tree.xpath('//div[@id="lnavi"]/div[@id="leftDeptColumn"]/div[@id="deptLeftnavContainer"]/h3[text()="categories"]')[0]
        parts = navigation.xpath('./following-sibling::ul[@id="deptLeftnavList"]')
        for part in parts: # handbags and accessories 2 parts
            nodes = part.xpath('./li')
            # the last [all handbags] don't need, because all children's categories contains more
            for i in range(len(nodes) - 1):
                directory = nodes[i].xpath('.//text()')[0]
                link = nodes[i].xpath('./a/@href')[0]
                link = link if link.startswith('http') else self.siteurl + link
                slug, key = self.extract_slug_key_of_listingurl.match(link).groups()
                cats = [category, directory]

                combine_url = '{0}/_/N-{1}/list.fly'.format(self.siteurl, key)
                self.category_url.add(combine_url)


    def crawl_jewelry_category(self, category, url, ctx):
        tree = self.download_category_return_xmltree(category, url, ctx)
        if tree is None: return
        navigation = tree.cssselect('div#leftDeptColumn div.dept-nav-section')[0]
        node = navigation.cssselect('ul li a')
        for i in node:
            directory = i.text_content().strip()
            link = i.get('href')
            if 'newarrivals.fly' in link:
                continue
            link = link if link.startswith('http') else self.siteurl + link
            slug, key = self.extract_slug_key_of_listingurl.match(link).groups()
            cats = [category, directory]

            combine_url = '{0}/_/N-{1}/list.fly'.format(self.siteurl, key)
            self.category_url.add(combine_url)


    def crawl_sale_category(self, category, url, ctx):
        """
            This category will generate path, "home > Shoes" ect.
        """
        tree = self.download_category_return_xmltree(category, url, ctx)
        if tree is None: return
        navigation = tree.cssselect('div#leftDeptColumn div.dept-nav-section')[0]
        node1 = navigation.cssselect('ul li a')
        navigation = tree.cssselect('div#leftDeptColumn div.dept-nav-section')[1]
        node2 = navigation.cssselect('ul li a')
        for i in itertools.chain(node1, node2):
            directory = i.text_content().strip()
            link = i.get('href')
            if 'newarrivals.fly' in link:
                continue
            link = link if link.startswith('http') else self.siteurl + link
            m = self.extract_slug_key_of_listingurl.match(link)
            if not m: continue
            slug, key = m.groups()
            cats = [category, directory]

            combine_url = '{0}/_/N-{1}/list.fly'.format(self.siteurl, key)
            self.category_url.add(combine_url)


    def crawl_kids_category(self, category, url, ctx):
        slug, key = self.extract_slug_key_of_listingurl.match(url).groups()
        cats = [category]

        combine_url = '{0}/_/N-{1}/list.fly'.format(self.siteurl, key)
        self.category_url.add(combine_url)


    def crawl_newarrivals_category(self, category, url, ctx):
        tree = self.download_category_return_xmltree(category, url, ctx)
        if tree is None: return
        nodes = tree.xpath('//div[@id="newArrivals"]/div[@id="listProductPage"]/div[@id="listProductContent"]/div[@id="leftPageColumn"]/div[@class="leftNavBlue"]/div[@id="leftNavCategories"]/span[@class="listCategoryItems"]')
        for node in nodes:
            link = node.xpath('./a/@href')[0]
            sub_category = node.xpath('./a/span/text()')[0].strip()
            slug, key = re.compile(r'.*/(.+)/_/N-(.+)/newarrivals.fly').match(link).groups()
            cats = [category, sub_category]

            combine_url = '{0}/_/N-{1}/list.fly'.format(self.siteurl, key)
            self.category_url.add(combine_url)


    def crawl_designer_brand_page(self, cat, url, ctx):
        tree = self.download_category_return_xmltree(cat, url, ctx)
        if tree is None: return
        brands_nodes = tree.cssselect('div#designerAlpha > ul#designList > li > a[href]')
        for node in brands_nodes:
            brand = node.get('name')
            link = node.get('href')
            key = link.rsplit('/', 1)[-1]
            link = link if link.startswith('http') else self.siteurl + link

            combine_url = link
            self.category_url.add(combine_url)


    def crawl_listing(self, url, ctx='', **kwargs):
        """.. :py:method::
            differenct between normal listing and newarrivals listing page
            nav = tree.xpath('//div[@id="listPage"]/div[@id="listProductPage"]') # normal listing
            nav = tree.xpath('//div[@id="newArrivals"]/div[@id="listProductPage"]') # new arrival
        """
        content = fetch_page(url)
        if content is None: content = fetch_page(url)
        if content is None or isinstance(content, int):
            return
        tree = lxml.html.fromstring(content)

        if 'bluefly.com/designer/' in url:
            self.crawl_brand_listing(url, tree, ctx)
            return

        key = self.extract_category_key.match(url).group(1)
        navigation = tree.cssselect('div[id] > div#listProductPage')
        if not navigation:
            content = fetch_page(url)
            tree = lxml.html.fromstring(content)
            navigation = tree.cssselect('div[id] > div#listProductPage')[0]
        else:
            navigation = navigation[0]

        category_path = navigation.xpath('./div[@class="breadCrumbNav"]/div[@class="breadCrumbMargin"]//text()')
        category_path = ' '.join( [c.strip() for c in category_path if c.strip()] )
        products = navigation.cssselect('div#listProductContent > div#rightPageColumn > div.listProductGrid > div#productGridContainer > div.productGridRow div.productContainer')
        products_num = navigation.cssselect('div#listProductContent > div#rightPageColumn > div#ls_topRightNavBar > div.ls_pageNav > span#ls_pageNumDisplayInfo > span.ls_minEmphasis')
        if not products_num:
            return
        products_num = navigation.cssselect('div#listProductContent > div#rightPageColumn > div#ls_topRightNavBar > div.ls_pageNav > span#ls_pageNumDisplayInfo > span.ls_minEmphasis')[0].text_content().split('of')[-1].strip()

        pages_num = ( int(products_num) - 1) // NUM_PER_PAGE + 1
        
        for prd in products:
            self.crawl_every_product_in_listing(category_path, prd, 1, ctx)

        for page_num in xrange(1, pages_num): # the real page number is page_num+1
            page_url = '{0}/_/N-{1}/Nao-{2}/list.fly'.format(self.siteurl, key, page_num*NUM_PER_PAGE)
            self.get_next_page_in_listing(key, category_path, page_url, page_num+1, ctx)


    def crawl_brand_listing(self, url, tree, ctx):
        page_num = tree.cssselect('div#ls_topRightNavBar > div.ls_pageNav > a:nth-last-of-type(1)')
        if page_num:
            page_num = int( page_num[0].text_content() )
        nodes = tree.cssselect('div#productGridContainer > div.productGridRow > div.productContainer')
        for node in nodes:
            self.crawl_every_product_in_listing([], node, 1, ctx)

        if page_num:
            for i in xrange(1, page_num):
                page_url = '{0}?page={1}'.format(url, i+1)
                content = fetch_page(page_url)
                if content is None: content = fetch_page(page_url)
                if content is None or isinstance(content, int):
                    return
                tree = lxml.html.fromstring(content)
                nodes = tree.cssselect('div#productGridContainer > div.productGridRow > div.productContainer')
                for node in nodes:
                    self.crawl_every_product_in_listing([], node, i+1, ctx)


    def get_next_page_in_listing(self, key, category_path, url, page_num, ctx):
        """.. :py:method::
            crawl next listing page
        :param key: category key in this listing
        :param category_path: "home > Women's Apparel > Blazers, Jackets & Vests"
        :param url: url of this page
        """
        content = fetch_page(url)
        if content is None: content = fetch_page(url)
        if content is None or isinstance(content, int):
            return
        tree = lxml.html.fromstring(content)
        navigation = tree.cssselect('div[id] > div#listProductPage')[0]
        products = navigation.cssselect('div#listProductContent > div#rightPageColumn > div.listProductGrid > div#productGridContainer > div.productGridRow div.productContainer')
        for prd in products:
            self.crawl_every_product_in_listing(category_path, prd, page_num, ctx)


    def crawl_every_product_in_listing(self, category_path, prd, page_num, ctx):
        """.. :py:method::
            crawl next listing page

        :param category_path: "home > Women's Apparel > Blazers, Jackets & Vests"
        :param prd: product node in this page
        :param page_num: the categroy listing page number
        """
        link = prd.cssselect('div.listProdImage a[href]')[0].get('href')
        link = link if link.startswith('http') else self.siteurl + link

        price = prd.xpath('./div[@class="layoutChanger"]/div[@class="listProductPrices"]/div[@class="priceSale"]/span[@class="priceSalevalue"]')
        if not price: price = prd.cssselect('div.layoutChanger > div.listProductPrices div.priceSale > span.priceSalevalue')

#        if not price: price = prd.xpath('./div[@class="layoutChanger"]/div[@class="listProductPrices"]/div[@class="priceBlueflyFinal"]/span[@class="priceBlueflyFinalvalue"]')
        if not price: price = prd.cssselect('div.layoutChanger > div.listProductPrices div.priceBlueflyFinal > span.priceBlueflyFinalvalue')

#        if not price: price = prd.xpath('./div[@class="layoutChanger"]/div[@class="listProductPrices"]/div[@class="priceReduced"]/span[@class="priceReducedvalue"]')
        if not price: price = prd.cssselect('div.layoutChanger > div.listProductPrices div.priceReduced > span.priceReducedvalue')
        if not price: price = prd.cssselect('div.layoutChanger > div.listProductPrices div.priceClearance > span.priceClearancevalue')
        if price:
            price = price[0].text_content().replace('$', '').replace(',', '').strip()

        slug, key = self.extract_product_slug_key.match(link).groups()
        listprice = prd.cssselect('div.layoutChanger > div.listProductPrices > div.priceRetail > span.priceRetailvalue')
        listprice = listprice[0].text_content().replace('$', '').replace(',', '').strip() if listprice else ''
        
        combine_url = '{0}/slug/p/{1}/detail.fly'.format(self.siteurl, key)
        if (price and '.' not in price) or (listprice and '.' not in listprice):
            self.alarm( '[{0},{1}], {2}'.format(listprice, price, combine_url) )


    def alarm(self, message):
        url = 'http://monitor.favbuy.org:5000/message/7afb42247532896255a48df47e046d1e/'
        obj = urllib.urlopen(url=url, data = urllib.urlencode({'message': message, 'shared_secret':'tempfavbuy'}) )

        if obj.read() != 'OK':
            print message
        obj.close()


if __name__ == '__main__':
    ss = Server()
    ss.crawl_category()
    for url in ss.category_url:
        try:
            ss.crawl_listing(url)
        except:
            open('url.txt', 'a').write( url + '\n')

