# -*- coding: utf-8 -*-
from helpers.signals import Signal

# pre_image_crawl		=	Signal("pre_image_crawl")
# post_image_crawl 		=	Signal("post_image_crawl")
image_crawled 			=	Signal("image_crawled")
image_crawled_failed 	=	Signal('image_crawled_failed')

brand_extracted 		=	Signal('brand_extracted')
brand_extracted_failed	=	Signal('brand_extracted_failed')
brand_refresh			=	Signal('brand_refresh')

ready_for_batch 		=	Signal('ready_for_batch')
ready_for_publish 		=	Signal('ready_for_publish')
update_for_publish		=	Signal('update_for_publish')