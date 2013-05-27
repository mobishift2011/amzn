# -*- coding: utf-8 -*-
from admin.models import Brand

def main():
    with open('/home/ethan/bt.csv', 'r') as f:
        line = f.readline()
        while line:
            line = f.readline()
            if line:
                title_en, title_cn = line.split(',')
                brand = Brand.objects(title_edit=title_en, is_delete=False).first()
                if not brand:
                    brand = Brand.objects(title=title_en, is_delete=False).first()

                if not brand:
                    print u'no brand {} in db'.format(title_en)
                    continue

                brand.title_cn = title_cn
                brand.save()

if __name__ == '__main__':
    main()