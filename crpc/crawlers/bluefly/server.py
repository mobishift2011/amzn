# -*- coding: utf-8 -*-
"""
crawlers.bluefly.server
~~~~~~~~~~~~~~~~~~~
This is the server part of zeroRPC module. Call by client automatically, run on many differen ec2 instances.
"""

from gevent import monkey; monkey.patch_all()
import lxml.html
from datetime import datetime, timedelta

from models import *
from crawlers.common.stash import *
from crawlers.common.events import common_saved, common_failed

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
        men_url = 'http://www.bluefly.com/a/men-clothing-shoes-accessories'
        sale_url = 'http://www.bluefly.com/a/designer-sale'
        kids_url = 'http://www.bluefly.com/Designer-Kids/_/N-v2wq/list.fly'
        new_url = 'http://www.bluefly.com/New-Arrivals/_/N-1aaqZapsz/newarrivals.fly'

#        self.crawl_women_or_shoes_category('women', women_url, ctx)
#        self.crawl_women_or_shoes_category('shoes', shoes_url, ctx)
#        self.crawl_handbag_accessories_category('handbags&accessories', handbags_accessories_url, ctx)
#        self.crawl_jewelry_or_men_category('jewelry', jewelry_url, ctx)
#        self.crawl_jewelry_or_men_category('men', men_url, ctx)
#        self.crawl_sale_category('sale', sale_url, ctx)
#        self.crawl_kids_category('kids', kids_url, ctx)
#        self.crawl_newarrivals_category('new', new_url, ctx)
#
#        # add some more products, like La Perla
#        self.save_category_to_db('http://www.bluefly.com/Designer-Beauty-Fragrance/_/N-nd52/list.fly',
#                'nd52',
#                'Designer-Beauty-Fragrance',
#                ['Home', 'Beauty & Fragrance'],
#                ctx)

        self.crawl_designer_brand_page('designer', 'http://www.bluefly.com/designers.fly', ctx)


    def save_category_to_db(self, url, key, slug, cats, ctx):
        """.. :py:method::
            common save to db in crawl_category
        """
        is_new, is_updated = False, False
        category = Category.objects(key=key).first()
        if not category:
            is_new = True
            category = Category(key=key)
            category.is_leaf = True
            category.combine_url = '{0}/_/N-{1}/list.fly'.format(self.siteurl, key)
            category.slug = slug
            category.cats = cats
        category.update_time = datetime.utcnow()
        category.save()
        common_saved.send(sender=ctx, obj_type='Category', key=key, url=url, is_new=is_new, is_updated=is_updated)

    def download_category_return_xmltree(self, category, url, ctx):
        """.. :py:method::
            common download in crawl_category
        """
        content = fetch_page(url)
        if content is None or isinstance(content, int):
            common_failed.send(sender=ctx, key=category, url=url,
                    reason='download error {0} or {1} return'.format(category, content))
            return
        tree = lxml.html.fromstring(content)
        return tree

    def crawl_women_or_shoes_category(self, category, url, ctx):
        tree = self.download_category_return_xmltree(category, url, ctx)
        if tree is None: return
        navigation = tree.xpath('//div[@id="lnavi"]/div[@id="leftDeptColumn"]/div[@id="deptLeftnavContainer"]/h3[text()="categories"]')[0]
        nodes = navigation.xpath('./following-sibling::ul[@id="deptLeftnavList"]/li[@class="new-link-test"]/following-sibling::li')
        for i in range(len(nodes) - 2): # sale not need, crawl it separately. all already contains
            directory = nodes[i].xpath('.//text()')[0]
            link = nodes[i].xpath('./a/@href')[0]
            link = link if link.startswith('http') else self.siteurl + link
            slug, key = self.extract_slug_key_of_listingurl.match(link).groups()
            cats = [category, directory]
            self.save_category_to_db(url, key, slug, cats, ctx)


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
                self.save_category_to_db(url, key, slug, cats, ctx)


    def crawl_jewelry_or_men_category(self, category, url, ctx):
        tree = self.download_category_return_xmltree(category, url, ctx)
        if tree is None: return
        navigation = tree.xpath('//div[@id="lnavi"]/div[@id="leftDeptColumn"]/div[@id="deptLeftnavContainer"]/h3[text()="categories"]')[0]
        parts = navigation.xpath('./following-sibling::ul[@id="deptLeftnavList"]')
        for part in parts:
            sub_category = part.xpath('./preceding-sibling::h2[1]/a/text()')[0]
            if sub_category == "Men's Sale":
                continue
            nodes = part.xpath('./li')
            for node in nodes:
                directory = node.xpath('.//text()')[0]
                link = node.xpath('./a/@href')[0]
                link = link if link.startswith('http') else self.siteurl + link
                slug, key = self.extract_slug_key_of_listingurl.match(link).groups()
                cats = [category, sub_category, directory]
                self.save_category_to_db(url, key, slug, cats, ctx)


    def crawl_sale_category(self, category, url, ctx):
        """
            This category will generate path, "home > Shoes" ect.
        """
        tree = self.download_category_return_xmltree(category, url, ctx)
        if tree is None: return
        navigation = tree.xpath('//div[@id="lnavi"]/div[@id="leftDeptColumn"]/div[@id="deptLeftnavContainer"]/h3[text()="categories"]')[0]
        nodes = navigation.xpath('./following-sibling::h2')
        for i in range(len(nodes) - 1):
            directory = nodes[i].xpath('.//text()')[0]
            link = nodes[i].xpath('./a/@href')[0]
            link = link if link.startswith('http') else self.siteurl + link
            slug, key = self.extract_slug_key_of_listingurl.match(link).groups()
            cats = [category, directory]
            self.save_category_to_db(url, key, slug, cats, ctx)


    def crawl_kids_category(self, category, url, ctx):
        slug, key = self.extract_slug_key_of_listingurl.match(url).groups()
        cats = [category]
        self.save_category_to_db(url, key, slug, cats, ctx)


    def crawl_newarrivals_category(self, category, url, ctx):
        tree = self.download_category_return_xmltree(category, url, ctx)
        if tree is None: return
        nodes = tree.xpath('//div[@id="newArrivals"]/div[@id="listProductPage"]/div[@id="listProductContent"]/div[@id="leftPageColumn"]/div[@class="leftNavBlue"]/div[@id="leftNavCategories"]/span[@class="listCategoryItems"]')
        for node in nodes:
            link = node.xpath('./a/@href')[0]
            sub_category = node.xpath('./a/span/text()')[0].strip()
            slug, key = re.compile(r'.*/(.+)/_/N-(.+)/newarrivals.fly').match(link).groups()
            cats = [category, sub_category]
            self.save_category_to_db(url, key, slug, cats, ctx)


    def crawl_designer_brand_page(self, cat, url, ctx):
        tree = self.download_category_return_xmltree(category, url, ctx)
        if tree is None: return
        brands_nodes = tree.cssselect('div#designerAlpha > ul#designList > li > a[href]')
        for node in brands_nodes:
            brand = node.get('name')
            link = node.get('href')
            key = link.rsplit('/', 1)[-1]
            link = link if link.startswith('http') else self.siteurl + link

            is_new, is_updated = False, False
            category = Category.objects(key=key).first()
            if not category:
                is_new = True
                category = Category(key=key)
                category.is_leaf = True
                category.combine_url = link
                category.cats = [cat, key]
            category.update_time = datetime.utcnow()
            category.save()
            common_saved.send(sender=ctx, obj_type='Category', key=key, url=link, is_new=is_new, is_updated=is_updated)


    def crawl_listing(self, url, ctx='', **kwargs):
        """.. :py:method::
            differenct between normal listing and newarrivals listing page
            nav = tree.xpath('//div[@id="listPage"]/div[@id="listProductPage"]') # normal listing
            nav = tree.xpath('//div[@id="newArrivals"]/div[@id="listProductPage"]') # new arrival
        """
        content = fetch_page(url)
        if content is None: content = fetch_page(url)
        if content is None or isinstance(content, int):
            common_failed.send(sender=ctx, key=key, url=url,
                    reason='download error listing or {0} return'.format(content))
            return
        tree = lxml.html.fromstring(content)

        if 'bluefly.com/designer/' in url:
            self.crawl_brand_listing(url, tree, ctx)

        key = self.extract_category_key.match(url).group(1)
        navigation = tree.cssselect('div[id] > div#listProductPage')
        if not navigation:
            with open('test.html', 'w') as fd:
                fd.write(url)
                fd.write(content)
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
            # common_failed.send(sender=ctx, key=key, url=url, reason='This url have no product number.')
            return
        products_num = navigation.cssselect('div#listProductContent > div#rightPageColumn > div#ls_topRightNavBar > div.ls_pageNav > span#ls_pageNumDisplayInfo > span.ls_minEmphasis')[0].text_content().split('of')[-1].strip()

        pages_num = ( int(products_num) - 1) // NUM_PER_PAGE + 1
        Category.objects(key=key).update_one(set__num=int(products_num),
                                             set__update_time=datetime.utcnow())
        
        for prd in products:
            self.crawl_every_product_in_listing(key, category_path, prd, 1, ctx)

        for page_num in xrange(1, pages_num): # the real page number is page_num+1
            page_url = '{0}/_/N-{1}/Nao-{2}/list.fly'.format(self.siteurl, key, page_num*NUM_PER_PAGE)
            self.get_next_page_in_listing(key, category_path, page_url, page_num+1, ctx)


    def crawl_brand_listing(self, url, tree, ctx):
        page_num = tree.cssselect('div#ls_topRightNavBar > div.ls_pageNav > a:last-of-type')
        if page_num: page_num = int( page_num[0].text_content() )
        nodes = tree.cssselect('div#productGridContainer > div.productGridRow > div.productContainer')
        for node in nodes:
            self.crawl_every_product_in_listing(url.rsplit('/', 1)[-1], [], node, 1, ctx)

        if page_num:
            for i in xrange(1, page_num):
                page_url = '{0}?page={1}'.format(url, i+1)
                content = fetch_page(page_url)
                if content is None: content = fetch_page(page_url)
                if content is None or isinstance(content, int):
                    common_failed.send(sender=ctx, key='', url=page_url,
                            reason='download error listing or {0} return'.format(content))
                    return
                tree = lxml.html.fromstring(content)
                nodes = tree.cssselect('div#productGridContainer > div.productGridRow > div.productContainer')
                for node in nodes:
                    self.crawl_every_product_in_listing(url.rsplit('/', 1)[-1], [], node, i+1, ctx)


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
            common_failed.send(sender=ctx, key=key, url=url,
                    reason='download error listing {0} or {1} return'.format(page_num, content))
            return
        tree = lxml.html.fromstring(content)
        navigation = tree.cssselect('div[id] > div#listProductPage')[0]
        products = navigation.cssselect('div#listProductContent > div#rightPageColumn > div.listProductGrid > div#productGridContainer > div.productGridRow div.productContainer')
        for prd in products:
            self.crawl_every_product_in_listing(key, category_path, prd, page_num, ctx)


    def crawl_every_product_in_listing(self, category_key, category_path, prd, page_num, ctx):
        """.. :py:method::
            crawl next listing page

        :param category_key: category key in this listing
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
            price = price[0].text_content().strip()
#        else:
#            common_failed.send(sender=ctx, key=category_key, url=link,
#                    reason='This product have no price.page_num: {0}'.format(page_num))

        slug, key = self.extract_product_slug_key.match(link).groups()
        soldout = True if prd.cssselect('div.stockMessage div.listOutOfStock') else False
        brand = prd.cssselect('div.layoutChanger > div.listBrand > a')[0].text_content().strip()
        title = prd.cssselect('div.layoutChanger > div.listLineMargin > div.productShortName')[0].text_content().strip()
        listprice = prd.cssselect('div.layoutChanger > div.listProductPrices > div.priceRetail > span.priceRetailvalue')
        listprice = listprice[0].text_content().strip() if listprice else ''
        
        rating = prd.cssselect('div.layoutChanger > div.product-detail-rating > img')
        rating = rating[0].get('alt') if rating else ''

        is_new, is_updated = False, False
        product = Product.objects(key=key).first()
        if not product:
            is_new = True
            product = Product(key=key)
            product.updated = False
            product.combine_url = '{0}/slug/p/{1}/detail.fly'.format(self.siteurl, key)
            product.slug = slug
            product.soldout = soldout
            product.brand = brand
            product.title = title
            product.rating = rating if rating else ''
        else:
            if product.soldout != soldout: # bluefly can change back
                product.soldout = soldout
                is_updated = True
                product.update_history.update({ 'soldout': datetime.utcnow() })
        if listprice and not product.listprice: product.listprice = listprice
        if price and not product.price: product.price = price
        if category_key not in product.category_key: product.category_key.append(category_key)
        if category_path and category_path not in product.cats: product.cats.append(category_path)
        product.list_update_time = datetime.utcnow()
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=key, url=link, is_new=is_new, is_updated=is_updated)


    def crawl_product(self, url, ctx='', **kwargs):
        """.. :py:method::
        """
        slug, key = self.extract_product_slug_key.match(url).groups()
        content = fetch_page(url)
        if content is None or isinstance(content, int):
            content = fetch_page(url)
            if content is None or isinstance(content, int):
                common_failed.send(sender=ctx, key=key, url=url,
                        reason='download product page error or {0} return'.format(content))
                return
        tree = lxml.html.fromstring(content)
        detail = tree.cssselect('div#page-wrapper > div#main-container > section#main-product-detail')[0]

        image_urls = []
        imgs = detail.cssselect('div.product-image > div.image-thumbnail-container > a')
        for img in imgs:
            aa, outx, bb, outy, cc = self.extract_large_image.search(img.get('rel')).groups()
            image_urls.append( '{0}{1}{2}{3}{4}'.format(aa, int(outx)*2, bb, int(outy)*2, cc) )
        if image_urls == []:
            img = detail.cssselect('div.product-image > a[href] > img.current-product-image')
            if img:
                aa, outx, bb, outy, cc = re.compile("(.+?outputx=)(\d+)(&outputy=)(\d+)(&.+)").match(img[0].get('src')).groups()
                image_urls = [ '{0}{1}{2}{3}{4}'.format(aa, int(outx)*2, bb, int(outy)*2, cc) ]
            else:
                img = detail.cssselect('div.product-image > a[data-large-image]')
                if img: image_urls = [ img[0].get('data-large-image') ]

        color = detail.cssselect('div.product-info > form#product > div.product-variations > div.pdp-label > em')
        color = color[0].text_content() if color else ''
        sizes = detail.cssselect('div.product-info > form#product > div.product-sizes > div.size-picker > ul.product-size > li')

        sizes_scarcity = []
        for size in sizes:
            for i in sizes_scarcity:
                if i[0] == size.get('data-size'):
                    i[1] = size.get('data-stock')
                    break
            else:
                sizes_scarcity.append( [size.get('data-size'), size.get('data-stock')] )

        shipping = detail.cssselect('div.product-info > div.shipping-policy')
        shipping = shipping[0].text_content().strip().replace('\n', '') if shipping else ''
        returned = detail.cssselect('div.product-info > div.return-policy')
        returned = returned[0].text_content().strip().replace('\n', '') if returned else ''
        summary = detail.cssselect('div.product-info > div.product-info-tabs > div.product-detail-list > div.product-description')[0].text_content().strip()
        property_list_info = detail.cssselect('div.product-info > div.product-info-tabs > div.product-detail-list > ul.property-list > li')
        list_info = []
        for p in property_list_info:
            list_info.append( p.text_content().strip().replace('\n', '') )

        num_reviews = tree.cssselect('div#page-wrapper > div#ratings-reviews-qa > div.ratings-reviews > div.review-stats > div.product-rating-summary > div.review-count')
        num_reviews = num_reviews[0].text_content() if num_reviews else ''

        is_new, is_updated = False, False
        product = Product.objects(key=key).first()
        if not product:
            is_new = True
            product = Product(key=key)

        if not product.price:
            prices = detail.cssselect('div.product-info > div.product-prices > div.product-price')
            if prices:
                product.price = prices[0].cssselect('span[itemprop=price]')[0].text_content().strip()
                if not product.listprice:
                    product.listprice = prices[0].cssselect('span.retail-price')[0].text_content().replace('retail :', '').strip()

        product.image_urls = image_urls
        product.color = color
        product.sizes_scarcity = sizes_scarcity
        product.shipping = shipping
        product.returned = returned
        product.summary = summary
        product.list_info = list_info
        product.num_reviews = num_reviews
        product.full_update_time = datetime.utcnow()
        if product.updated == False:
            product.updated = True
            ready = True
        else: ready = False
        product.save()
        common_saved.send(sender=ctx, obj_type='Product', key=key, url=url, is_new=is_new, is_updated=is_updated, ready=ready)


    def _make_image_urls(self, product_key, image_count):
        """
            not use this function anymore, because image may have 1,2,3,5, no 4 in the middle
        """
        urls = ['http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}.pct&outputx=1020&outputy=1224&level=1'.format(product_key)]
        for i in range(1, image_count):
            urls.append( 'http://cdn.is.bluefly.com/mgen/Bluefly/eqzoom85.ms?img={0}_alt0{1}.pct&outputx=1020&outputy=1224&level=1'.format(product_key, i) )
        return urls


if __name__ == '__main__':
    Server().crawl_category()
    exit()
    server = zerorpc.Server(Server())
    server.bind("tcp://0.0.0.0:{0}".format(CRAWLER_PORT))
    server.run()
