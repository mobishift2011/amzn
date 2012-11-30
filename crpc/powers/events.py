# -*- coding: utf-8 -*-
'''
Created on 2012-11-19

@author: ethan
'''

from helpers.signals import Signal

pre_image_crawl			=	Signal("pre_image_crawl")
post_image_crawl 		=	Signal("post_image_crawl")

image_crawled 			=	Signal("image_crawled")
image_crawled_failed 	=	Signal('image_crawled_failed')

brand_extracted 		=	Signal('brand_extracted')
brand_extracted_failed	=	Signal('brand_extracted_failed')

ready_for_batch = Signal('ready_for_batch')
