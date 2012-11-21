# -*- coding: utf-8 -*-
'''
Created on 2012-11-19

@author: ethan
'''

from helpers.signals import Signal

pre_image_crawl = Signal("pre_image_crawl")
post_image_crawl = Signal("post_image_crawl")

image_crawled = Signal("image_crawled")
image_crawled_failed = Signal('image_crawled_failed')

run_image_crawl = Signal('run_image_crawl')
