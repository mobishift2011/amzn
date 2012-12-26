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

def lot18_mapping(site, event):
    return ["Home"]

def venteprivee_mapping(site, event):
    m = get_site_module('venteprivee')
    results = m.Product.objects(event_id=event.event_id).distinct('dept')
    convert = {
        "Writing Instruments": "Home",
        "Womens":"Women",
        "Small Leather Goods":"Handbags",
        "Mens":"Men",
        "Earrings":"Jewelry & Watches",
        "Necklaces":"Jewelry & Watches",
        "Bracelets":"Jewelry & Watches",
        "Infant":"Kids & Baby",
        "Men": "Men",
        "Women": "Women",
        "Girls": "Kids & Baby",
        "Boys": "Kids & Baby",
        "Pumps": "Women",
        "Rings": "Jewelry & Watches",
        "Necklaces & Pendants": "Jewelry & Watches",
        "Men's": "Men",
        "CLUTCHES": "Handbags",
        "Dubai Ovenware Collection": "Home",
        "Women's Sunglasses": "Women",
        "Ties, Bowties, Tie Pins & Cufflinks": "Men",
    }
    new_results = []
    for r in results:
        if convert.get(r):
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
    "onekingslane": DEFAULT,
    "ruelala": DEFAULT,
    "totsy": TOTSY,
    "venteprivee": venteprivee_mapping,
    "zulily": ZULILY,
}

def classify_event_department(site, event):
    mapping = EVENT_MAPPING.get(site, DEFAULT)
    results = []
    if isinstance(mapping, dict):
        e = event
        for dept in getattr(e, 'dept'):
            results.extend(mapping['mapping'].get(dept,[]))
            for key in mapping['contains'].keys():
                if key in dept:
                    results.extend(mapping['contains'][key])
    else:
        results = mapping(site, event)
    return list(set(results))

if __name__ == '__main__':
    from web import sites
    import random
    while True:
        site = random.choice(sites)
        m = get_site_module(site)
        
        if hasattr(m, 'Event'):
            e = random.choice(list(m.Event.objects()))
            print e.sale_title, e.dept, e.event_id
            print "==>", site, classify_event_department(site, e)
        raw_input()
