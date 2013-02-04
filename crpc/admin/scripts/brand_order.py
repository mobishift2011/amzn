# -*- coding: utf-8 -*-
from settings import CRPC_ROOT
from powers.models import Brand
import os

with open(CRPC_ROOT+'/admin/scripts/brand_ranking4.csv', 'r') as f:
	while True:
		r = f.readline()

		if not r:
			break
		
		name, global_searchs = r.split(',')
		print name, global_searchs
		brand = Brand.objects(title_edit=name).first()
		if not brand:
			brand = Brand.objects(title=name).first()

		if not brand:
			print name
			continue

		brand.global_searchs = global_searchs
		brand.save()