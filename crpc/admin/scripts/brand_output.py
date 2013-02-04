# -*- coding: utf-8 -*-
from admin.models import Brand

def output():
	brands = Brand.objects(is_delete=False)

	with open('brand_output.txt', 'w') as f:
		for brand in brands:
			name = brand.title_edit or brand.title
			url = 'yes' if brand.url else 'no'
			desc = 'yes' if brand.blurb else 'no'
			if '\n' in url:
				print url
			if '\n' in desc:
				print desc
			f.write('{0}\t{1}\t{2}\t{3}\n'.format(
				name.encode('utf-8'), brand.level, url, desc
			))


if __name__ == '__main__':
	output()