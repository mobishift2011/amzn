from backends.cleansing.kwt import KeywordSearch
from models import Brand

def get_searchs():
    brands = []
    for b in Brand.objects(is_delete=False):
        if b.title_edit != "":
            brand = b.title_edit
        else:
            brand = b.title
        brands.append(brand)

    ks = KeywordSearch()
    for i in range(len(brands)/50):
        thebrands = brands[i*50:i*50+50]
        kwdict = ks.search(thebrands)
        for kw, result in kwdict.iteritems():
            gs, ls = result
            gs, ls = int(gs), int(ls)
            print kw, gs, ls

get_searchs()
        
