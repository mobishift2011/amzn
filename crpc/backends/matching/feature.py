import random

sites = ['beyondtherack', 'bluefly', 'gilt', 'hautelook', 'ideeli', 'lot18', 'modnique', 'myhabit', 'nomorerack', 'onekingslane', 'ruelala', 'venteprivee', 'totsy', 'belleandclive', 'zulily']


def get_site_module(site):
    return __import__('crawlers.'+site+'.models', fromlist=['Category', 'Event', 'Product'])

def get_site_key():
    site = random.choice(sites)
    m = get_site_module(site)

    count = m.Product.objects().count()
    if count == 0:
        #sites.remove(site)
        return get_site_key()

    index = random.randint(1, count-1)
    p = m.Product.objects().skip(index).first()

    if (not p.title) or (not p.list_info):
        print p.title
        return get_site_key()

    return site+'_'+p.key

def get_text(site_key):
    site, key = site_key.split('_', 1)
    m = get_site_module(site)
    p = m.Product.objects.get(key=key)
    try:
        depts = []
        for eid in p.event_id:
            e = m.Event.objects.get(event_id=eid)
            depts.extend( e.dept )
            if hasattr(e, 'short_desc'):
                depts.append( e.short_desc )
        depts.extend(p.cats)
        depts = list(set(depts))

        content = site + u'\n'
        if depts:
            content += u'; '.join(depts) + u'\n'
        if p.brand:
            content += p.brand + u'\n'
        if p.tagline:
            content += u'; '.join(p.tagline) + u'\n'
        content += p.title + u'\n'
        content += u'\n'.join(p.list_info)
    except:
        import traceback
        traceback.print_exc()

    return p.combine_url, p.image_urls, content.replace('\n','<br />')

