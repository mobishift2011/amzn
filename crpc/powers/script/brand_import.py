# -*- coding: utf-8 -*-

from powers.models import Brand
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djCatalog.djCatalog.settings")
from djCatalog.catalogs.models import Brand as EditBrand

def import_brand():
    ebs = EditBrand.objects()
    for eb in ebs:
        brand = Brand.objects(title=eb.title).update(
            set__title_edit = eb.title_edit,
            set__title_checked = eb.title_checked,
            set__keywords = eb.keywords,
            set__url = eb.url,
            set__url_checked = eb.url_checked,
            set__blurb = eb.blurb,
            set__level = eb.level,
            set__dept = eb.dept,
            set__is_delete = eb.is_delete,
            set__done = eb.done,
            upsert = True
        )

if __name__ == '__main__':
    import time
    start = time.time()
    import_brand()
    print 'cost {0} s.'.format(int(time.time()-start))