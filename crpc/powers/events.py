# -*- coding: utf-8 -*-
'''
Created on 2012-11-19

@author: ethan
'''

from helpers.signals import SignalQueue, Signal

pre_image_crawl = SignalQueue("pre_image_crawl")
post_image_crawl = SignalQueue("post_image_crawl")

image_crawled = SignalQueue("image_crawled")
image_crawled_failed = SignalQueue('image_crawled_failed')

run_image_crawl = SignalQueue('run_image_crawl')