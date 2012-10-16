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


    def find_leaf(self):
        return self.category.find({'leaf': 1, 'num': {'$exists': True}}, fields=['url', 'catstr'])

    def get_product(self, bah):
        return self.product.find_one({'bah': bah}, {'update_time':1})

    def product_seen(self, bah):   
        return self.product.find_one({'bah': bah}, {'bah':1, 'catstr':1})

    def update_listing(self, bah, image, url, review, brand, title, hightlight, available, model, price, shipping, best_sell_rank, catstr, update_time, detail_parse):
        item = self.product_seen(bah)
        if item:
            # mongodb load string is unicode,python in linux default utf-8
            if catstr.decode('utf-8') in item['catstr']:
                self.product.update({'bah': bah}, {'$set': {'image': image, 'url': url, 'review': review, 'brand': brand, 'title': title, 'hightlight': hightlight, 'available': available, 'model': model, 'price': price, 'shipping': shipping, 'best_sell_rank': best_sell_rank, 'update_time': update_time, 'detail_parse': detail_parse}}, upsert=True, multi=False)
            else:
                item['catstr'].append(catstr.decode('utf-8'))
                self.product.update({'bah': bah}, {'$set': {'image': image, 'url': url, 'review': review, 'brand': brand, 'title': title, 'hightlight': hightlight, 'available': available, 'model': model, 'price': price, 'shipping': shipping, 'best_sell_rank': best_sell_rank, 'catstr': item['catstr'], 'update_time': update_time, 'detail_parse': detail_parse}}, upsert=True, multi=False)
        else:
            self.product.insert({'bah': bah, 'image': image, 'url': url, 'review': review, 'brand': brand, 'title': title, 'hightlight': hightlight, 'available': available, 'model': model, 'price': price, 'shipping': shipping, 'best_sell_rank': best_sell_rank, 'catstr': [catstr], 'update_time': update_time, 'detail_parse': detail_parse})


    def update_product(self, bah, bill_later, specifications, in_box, rating, buy_together=None):
        """ insert info which did not contain in listing page
        """
        if buy_together:
            self.product.update({'bah': bah}, {'$set': {'bill_later': bill_later, 'specifications': specifications, 'in_box': in_box, 'rating': rating, 'buy_together': buy_together}}, upsert=True, multi=False)
        else:
            self.product.update({'bah': bah}, {'$set': {'bill_later': bill_later, 'specifications': specifications, 'in_box': in_box, 'rating': rating}}, upsert=True, multi=False)


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

    def set_leaf_category(self, category_prefix, num):
        ''' set the category node as leaf node
        '''
        category_str = ' > '.join(category_prefix)
        row = self.category.find_one({'catstr': category_str})
        if row:
            row['leaf'] = 1
            row['num'] = num
            self.category.save(row)
