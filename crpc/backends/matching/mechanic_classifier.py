#!/usr/bin/env python
import re
from models import CATS

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

def load_rules():
    """ load rules from rules.txt 

    Returns a dict of three priority rules, each is a a list of Rule tuple, e.g
        set(["Maxi","Dress"]), ["Women", "Dresses & Skirts"]
    """
    from os.path import dirname, join
    from collections import defaultdict
    pattern = re.compile(r'^\[(\d)\] (.+) -> (.+)')
    path = join(dirname(__file__), "rules.txt")
    rules_dict = defaultdict(list)
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            m = pattern.search(line)
            priority, rule, department = m.group(1), m.group(2), m.group(3)
            
            rules_dict[priority].append( [set(rule.split(' ')), department.split('; ')] )
    
    from pprint import pprint
    for k, v in rules_dict.iteritems():
        rules_dict[k] = sorted(v, key=lambda x: len(x[0]), reverse=True)
    return rules_dict
            
words_split = re.compile('[A-Za-z0-9\-]+')
def classify_product_department(site, product):
    m = get_site_module(site)
    rules_dict = load_rules()
    p = product
    result = []
    kws = set(words_split.findall(p.title))
    
    # check level-0 rules
    level12 = True
    for rule in rules_dict['0']:
        if not rule[0].difference(kws):
            result.extend(rule[1])
            level12 = False
            break
    
    if level12:
        # merge events info
        if p.event_id:
            d1 = []
            for eid in p.event_id:
                e = m.Event.objects.get(event_id=eid)
                d1.extend(classify_event_department(site, e))
            d1 = list(set(d1))
            result.extend( d1 )

        # do level1 and level2 classifying
        for priority in '12':
            for rule in rules_dict[priority]:
                if not rule[0].difference(kws):
                    result.extend(rule[1])
                    break

    # add necessory converters
    if "Women" in result:
        if "Tops & Tees" in result:
            result.append("Shirts & Sweaters")
        elif "Socks, Underwear & Sleepwear" in result:
            result.append("Intimates & Loungewear")
        elif "Suits & Coats" in result:
            result.append("Outerwear")
    elif "Men" in result:
        if "Intimates & Loungewear" in result:
            result.append("Socks, Underwear & Sleepwear")
        elif "Dresses & Skirts" in result:
            result.append("Shirts & Sweaters")
        elif "Tops & Tees" in result:
            result.append("Polos & Tees")
    elif "Kids & Baby" in result:
        for clothing_category in ["Tops & Tees", "Shirts & Sweaters", "Outerwear", "Pants & Shorts", "Dresses & Skirts"]:
            if clothing_category in result:
                if 'Girl' in p.title:
                    result.append("Girls' Clothing")
                elif 'Boy' in p.title:
                    result.append("Boys' Clothing")
                else:
                    result.append("Girls' Clothing")
                    result.append("Boys' Clothing")
                break
        if "Shoes" in result:
            result.append("Girls' Shoes")
            result.append("Boys' Shoes")
        elif "Beds & Bath" in result or "Furniture & Lighting" in result:
            result.append("Bed, Bath & Furniture")
        elif "Tools" in result:
            result.append("Gear & Equipment")
    elif "Home" in result and "Accessories" in result:
        result.append("Home Accessories")

    # reorder
    keys = CATS.keys()
    result = list(set(result))
    for key in keys:
        if key in result and key != result[0]:
            result.remove(key)
            result = [key] + result
    return result

def test_event():
    import random
    from web import sites
    while True:
        site = random.choice(sites)
        m = get_site_module(site)
        
        if hasattr(m, 'Event'):
            e = random.choice(list(m.Event.objects()))
            print e.sale_title, e.dept, e.event_id
            print "==>", site, classify_event_department(site, e)
        raw_input()

def test_product():
    import random
    from web import sites
    while True:
        site = random.choice(sites)
        site = 'beyondtherack'
        m = get_site_module(site)
        count = m.Product.objects().count()
        index = random.randint(0, count-1)
        p = m.Product.objects().skip(index).first()
        if p.cats:
            print "CATS ==>", p.cats
        if p.dept:
            print "DEPTS ==>", p.dept,
        if p.event_id:
            for eid in p.event_id:
                e = m.Event.objects.get(event_id=eid)
                print e.dept,
        print
        print "TITLE ==>", p.title
        print "==>", site, classify_product_department(site, p)
        print
        raw_input()

if __name__ == '__main__':
    test_product()
    #load_rules() 
