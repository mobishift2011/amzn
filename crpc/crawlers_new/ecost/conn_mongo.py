#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Author: Yuande <miraclecome (at) gmail.com>

import pymongo

class conn_mongo(object):

    def __init__(self, database='bestbuy', host='127.0.0.1', port=27017):
        self.mongo_conn = pymongo.Connection('localhost')
        self.conn = self.mongo_conn[database]

    def close_mongo(self):
        self.mongo_conn.disconnect()

    def get_category_col(self, collection):
        self.category = self.conn[collection]
        return self.category

    def get_product_col(self, collection):
        self.product = self.conn[collection]
        return self.product

    def index_unique(self, collection, key):
        collection.ensure_index(key, unique=True)

    def title_link(self, title, link, price):
        if price is not '':
            self.product.update({'special_page': True, 'url': link}, {'$set': {'title': title, 'price': price, 'updated': False}}, upsert=True, multi=False)
        else:
            self.product.update({'special_page': True, 'url': link}, {'$set': {'title': title, 'updated': False}}, upsert=True, multi=False)


#    def get_product(self, ecost):
#        return self.product.find_one({'ecost': ecost}, {'update_time':1})
#
    def product_seen(self, ecost):   
        return self.product.find_one({'ecost': ecost}, {'ecost':1, 'catstr':1})

    def update_listing(self, ecost, model, price, sell_rank, link, catstr, update_time, updated):
        item = self.product_seen(ecost)
        if item:
            # mongodb load string is unicode,python in linux default utf-8
            if catstr.decode('utf-8') in item['catstr']:
                self.product.update({'ecost': ecost}, {'$set': {'link': link, 'model': model, 'price': price, 'sell_rank': sell_rank, 'update_time': update_time, 'updated': updated}}, upsert=True, multi=False)
            else:
#                if isinstance(item['catstr'], unicode):
#                    print item['catstr']
                item['catstr'].append(catstr.decode('utf-8'))
                self.product.update({'ecost': ecost}, {'$set': {'link': link, 'model': model, 'price': price, 'sell_rank': sell_rank, 'catstr': item['catstr'], 'update_time': update_time, 'updated': updated}}, upsert=True, multi=False)
        else:
            self.product.insert({'ecost': ecost, 'link': link, 'model': model, 'price': price, 'sell_rank': sell_rank, 'catstr': [catstr], 'update_time': update_time, 'updated': updated})



    def update_product(self, title, image, price, ecost, model, shipping, available, platform, manufacturer, upc, review, rating, specifications):
        """ insert info which did not contain in listing page
        """
        self.product.update({'ecost': ecost}, {'$set': {'title': title, 'image': image, 'price': price, 'model': model, 'shipping': shipping, 'available': available, 'platform': platform, 'manufacturer': manufacturer, 'upc': upc, 'review': review, 'rating': rating, 'specifaications': specifications, 'updated': True}}, upsert=True, multi=False)


    def set_update_flag(self, top_category):
        ''' Set all categories under the top category to the state of not update
        '''
        self.category.update({'catstr': {'$regex': '^'+ top_category+'.*'}, '$atomic': True}, {'$set': {'updated': '0'}}, upsert=False, multi=True)


    def insert_update_category(self, cats, url):
        ''' category already have: update; category not exist: insert.
            set updated: "1"
        '''
        category_str = ' > '.join(cats)
        if self.category_seen(category_str):
            self.update_category(category_str)
        else:
            self.insert_category(cats, category_str, url)

    def category_seen(self, category_str):   
        return self.category.find_one({'catstr': category_str})

    def category_updated(self, category_str):
        return self.category.find_one({'catstr': category_str, 'updated': '1'})

    def update_category(self, category_str):
        self.category.update({'catstr': category_str}, {'$set': {'updated': '1'}})

    def insert_category(self, cats, category_str, url):
        self.category.insert({'cats':cats, 'catstr': category_str, 'url':url, 'updated': '1'})

    def delete_antique(self):
        ''' delete the category which is not index by amazon any more.
        '''
        self.category.remove({'updated': '0', '$atomic': True})

    def set_leaf_category(self, category_prefix, num=None):
        ''' set the category node as leaf node
        '''
        category_str = ' > '.join(category_prefix)
        row = self.category.find_one({'catstr': category_str})
        if row:
            row['leaf'] = 1
            if num:
                row['num'] = num
            self.category.save(row)
