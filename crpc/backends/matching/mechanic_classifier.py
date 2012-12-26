#!/usr/bin/env python
DEFAULT =  {
    "dept_in": "Event",
    "column": "dept", 
    "contains": {},
    "mapping": {
        "kids": ["Kids & Baby"],
        "men": ["Men"],
        "women": ["Women"],
        "home": ["Home"],
        "living": ["Home"],
        "wine": ["Wine"],
    },
} 

BLUEFLY = {
    "dept_in": "Category",
    "column": "cats",
    "mapping": {
        "men": ["Men"],
        "women": ["Women"],
        "kids": ["Kids & Baby"],
        "shoes": ["Women"],
        "handbags&accessories": ["Women", "Handbags"],
        "jewelry": ["Women", "Jewelry & Watches"],
    },
    "contains": {
        "Women": ["Women"],
        "Men": ["Men"],
        "Handbags": ["Women", "Handbags"],
        "Beauty": ["Women", "Beauty & Health"],
        "Jewelry": ["Women", "Jewelry & Watches"],
    }
}

HAUTELOOK = {
    "dept_in": "Event",
    "column": "dept",
    "contains": {},
    "mapping": {
        "Kids": ["Kids & Baby"], 
        "Beauty": ["Beauty & Health", "Women"], 
        "Women": ["Women"], 
        "Home": ["Home"], 
        "Men": ["Men"],
    }
}

MODNIQUE = {
    "dept_in": "Event",
    "column": "dept",
    "contains": {},
    "mapping": {
        "handbags-accessories" : ["Handbags", "Women"],
        "jewelry-watches": ["Jewelry & Watches", "Women"],
        "apparel": ["Women"],
        "men": ["Men"],
        "beauty": ["Beauty & Health"],
        "shoes": ["Women"],
    }
}

NOMORERACK = {
    "dept_in": "Category",
    "column": "key",
    "contains": {},
    "mapping": {
        "electronics": ["Home"], 
        "lifestyle": ["Home"], 
        "home": ["Home"], 
        "kids": ["Kids & Baby"], 
        "men": ["Men"], 
        "women": ["Women"],
    }
}

ONEKINGSLANE = {
    "dept_in": "Category",
    "column": "cats",
    "contains": {},
    "mapping": {
        "home": ["Home"],
    },
}


TOTSY = {
    "dept_in": "Event",
    "column": "dept",
    "contains": {},
    "mapping": {
        "Girls": ["Kids"],
        "Boys": ["Kids"],
        "Accessories": ["Kids"],
        "Shoes": ["Kids"],
        "Toys and Books": ["Kids"],
        "Home": ["Kids"],
        "Moms and Dads": ["Kids"],
        "Gear": ["Kids"],
    }
}

ZULILY = {
    "dept_in": "Event",
    "column": "dept",
    "contains": {},
    "mapping": {
        "baby-maternity": ["Kids"], 
        "boys": ["Kids"], 
        "girls": ["Kids"],
        "home": ["Home"], 
        "toys-playtime": ["Kids"], 
        "women": ["Women"],
    }
}


def get_site_module(site):
    return __import__('crawlers.'+site+'.models', fromlist=['Category', 'Event', 'Product'])

def lot18_mapping(site, key):
    return ["Home"]

def venteprivee_mapping(site, key):
    m = get_site_module('venteprivee')
    results = m.Product.objects(event_id=key).distinct('dept')
    convert = {
        "Writing Instruments": "Home",
        "Womens":"Women",
        "Small Leather Goods":"Handbags",
        "Mens":"Women",
        "Earrings":"Jewelry & Watches",
        "Necklaces":"Jewelry & Watches",
        "Jackets, Sweaters & Cardigans":"Women",
        "Bracelets":"Jewelry & Watches",
        "Dresses":"Women",
        "Sweaters & Cardigans":"Women",
        "Jackets":"Women",
        "Tops":"Women",
        "Accessories":"Women",
        "Infant":"Kids & Baby",
        "Men": "Men",
        "Women": "Women",
        "Girls": "Kids & Baby",
        "Boys": "Kids & Baby",
        "Boots": "Women",
        "Flats": "Women",
        "Sandals": "Women",
        "Pumps": "Women",
        "Rings": "Jewelry & Watches",
        "Necklaces & Pendants": "Jewelry & Watches",
        "Men's": "Men",
        "CLUTCHES": "Handbags",
        "Dubai Ovenware Collection": "Home",
        "Stockholm Collection": "Home",
        "San Francisco Collection": "Home",
        "Women's Sunglasses": "Women",
        "Ties, Bowties, Tie Pins & Cufflinks": "Men",
        "Shirts & Polos": "Women",
        "Trousers": "Women",
        "Scarves & Socks": "Women",
        "Parrot": "Women"
    }
    new_results = []
    for r in results:
        new_results.append(convert.get(r))
    return new_results 

EVENT_MAPPING = {
    "beyondtherack": DEFAULT,
    "bluefly": BLUEFLY,
    "gilt": DEFAULT,
    "hautelook": HAUTELOOK,
    "ideeli": DEFAULT,
    "lot18": lot18_mapping,
    "modnique": MODNIQUE,
    "myhabit": DEFAULT,
    "nomorerack": NOMORERACK,
    "onekingslane": ONEKINGSLANE,
    "ruelala": DEFAULT,
    "totsy": TOTSY,
    "venteprivee": venteprivee_mapping,
    "zulily": ZULILY,
}

def classify_event_department(site, key):
    mapping = EVENT_MAPPING.get(site, DEFAULT)
    results = []
    if isinstance(mapping, dict):
        m = get_site_module(site)
        try:
            if type == 'Event':
                e = m.Event.objects.get(event_id=key) 
            else:
                e = m.Category.objects.get(key=key) 
        except:
            return []
        for dept in getattr(e, mapping['column']):
            results.extend(mapping['mapping'].get(dept,[]))
            for key in mapping['contains'].keys():
                if key in dept:
                    results.extend(mapping['contains'][key])
    else:
        results = mapping(site, key)
    return list(set(results))

if __name__ == '__main__':
    from web import sites
    import random
    while True:
        site = random.choice(sites)
        m = get_site_module(site)
        try:
            type = EVENT_MAPPING[site]['dept_in'] 
        except:
            if site=='venteprivee':
                type = 'Event'
            else:
                continue
        
        if type == 'Category':
            e = random.choice(list(m.Category.objects()))
            print e.cats
            print "==>", site, classify_event_department(site, e.key)
        else:
            e = random.choice(list(m.Event.objects()))
            print e.sale_title, e.dept, e.event_id
            print "==>", site, classify_event_department(site, e.event_id)
        raw_input()
