# -*- coding: utf-8 -*-
from models import Brand

def get_all_brands():
	import time
	start = time.time()
	brands = [brand.to_json() for brand in Brand.objects()[0:101]]
	print '~~~~~~~~~~~~~~~total: ', time.time() - start
	return brands