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
        "jewelry": ["Women", "Jewelry & Watches"],
    },
    "contains": {
        "Women": ["Women"],
        "Men": ["Men"],
        "Handbags": ["Women", "Bags"],
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
        "jewelry-watches": ["Jewelry & Watches", "Women"],
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
    "mapping": {},
    "contains": {
        "Girls": ["Kids & Baby"],
        "Boys": ["Kids & Baby"],
        "Toys and Books": ["Kids & Baby"],
        "Home": ["Home"],
        "Moms and Dads": ["Women"],
        "Gear": ["Kids & Baby"],
    }
}

ZULILY = {
    "dept_in": "Event",
    "column": "dept",
    "contains": {},
    "mapping": {
        "baby-maternity": ["Kids & Baby"], 
        "boys": ["Kids & Baby"], 
        "girls": ["Kids & Baby"],
        "home": ["Home"], 
        "toys-playtime": ["Kids & Baby"], 
        "women": ["Women"],
    }
}


def get_site_module(site):
    return __import__('crawlers.'+site+'.models', fromlist=['Category', 'Event', 'Product'])

def lot18_mapping(site, event):
    return ["Wine"]

venteprivee_convert = {
        "Writing Instruments": "Home",
        "Womens":"Women",
        "Small Leather Goods":"Bags",
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
        "CLUTCHES": "Bags",
        "Dubai Ovenware Collection": "Home",
        "Women's Sunglasses": "Women",
        "Ties, Bowties, Tie Pins & Cufflinks": "Men",
}
def venteprivee_mapping(site, event):
    convert = venteprivee_convert
    m = get_site_module('venteprivee')
    results = m.Product.objects(event_id=event.event_id).distinct('dept')
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
    path = join(dirname(__file__), "dept.rules")
    rules_dict = defaultdict(list)
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            m = pattern.search(line)
            priority, rule, department = m.group(1), m.group(2), m.group(3)
            rule = rule.lower().decode('utf-8')
            
            rules_dict[priority].append( [set(rule.split(u' ')), department.split(u'; ')] )
    
    for k, v in rules_dict.iteritems():
        rules_dict[k] = sorted(v, key=lambda x: len(x[0]), reverse=True)
    return rules_dict

def preprocess(title):
    title = title.lower()
    title = re.sub(r'designed in .+ gold', '', title)
    title = re.sub(r'designed in .+ silver', '', title)
    title = re.sub(r'made in [a-z]+', '', title)
    # wipe out sentences `with`s and `in`s and `-`s
    title = re.sub(r'"[a-z ]+"', '', title)
    if "'s" not in title:
        title = re.sub(r"'\w+'", '', title)
    title = re.sub(r", [0-9a-z' &]+$", '', title)
    title = re.sub(r'all in one', 'all-in-one', title)
    title = re.sub(r'with you', 'with-you', title)
    title = re.sub(r'in a', 'in-a', title)
    title = re.sub(r' in .+$', '', title)
    title = re.sub(r'[a-z]+/[a-z]+', '', title)
    title = re.sub(r' with .*? accents ', '', title)
    title = re.sub(r' with .+$', '', title)
    title = re.sub(r'(.*) - (.*)', r'\2 \1', title)
    title = re.sub(r'([a-z]+)-', r'\1', title)
    title = re.sub(r'baby pink', '', title)
    title = re.sub(r'baby doll', 'babydoll', title)
    # then numbers & brackets
    title = re.sub(r'\d+/\d+ condition', '', title)
    title = re.sub(r'(.*)\(([^)]+)\)$', r'\1', title)
    title = re.sub(r' [ivxlc]+$', '', title)
    title = re.sub(r'set of [0-9]+', 'set', title)
    title = re.sub(r'[0-9]+ pcs$', '', title)
    return title

def postprocess(site, p, result):
    # Special Sites
    keys = [k.decode('utf-8') for k in  CATS.keys()]
    for thesite, only in [(u'lot18', u'Wine')]:
        if thesite == site: 
            exclude = set(keys)
            exclude.remove(only)
            result = set(result)
            result -= exclude
            result.add(only)
            result = list(result)
            break

    for exclusive, thesites in [(u'Wine',set([u'lot18']))]:
        if site in thesites and exclusive in result:
            result.remove(exclusive) 

    # add necessory converters
    if u"Women" in result:
        if u"Polos & Tees" in result:
            result.append(u"Shirts & Sweaters")
            result.remove(u"Polos & Tees")
        elif u"Socks, Underwear & Sleepwear" in result:
            result.append(u"Intimates & Loungewear")
            result.remove(u"Socks, Underwear & Sleepwear")
        elif u"Suits & Coats" in result:
            result.append(u"Outerwear")
            result.remove(u"Suits & Coats")
    if u"Men" in result:
        if u"Intimates & Loungewear" in result:
            result.append(u"Socks, Underwear & Sleepwear")
            result.remove(u"Intimates & Loungewear")
        elif u"Dresses & Skirts" in result:
            result.append(u"Shirts & Sweaters")
            result.remove(u"Dresses & Skirts")
    if u"Kids & Baby" in result:
        for clothing_category in [u"Polos & Tees", u"Shirts & Sweaters", u"Outerwear", u"Pants & Shorts", u"Dresses & Skirts", u"Intimates & Loungewear", "Suits & Coats", "Socks, Underwear & Sleepwear"]:
            if clothing_category in result:
                if u'girl' in p.title.lower():
                    result.append(u"Girls' Clothing")
                elif u'boy' in p.title.lower():
                    result.append(u"Boys' Clothing")
                else:
                    result.append(u"Girls' Clothing")
                    result.append(u"Boys' Clothing")
                result.remove(clothing_category)
                break
        if u"Shoes" in result:
            result.append(u"Girls' Shoes")
            result.append(u"Boys' Shoes")
            result.remove(u"Shoes")
        elif u"Bed & Bath" in result:
            result.append(u"Bed, Bath & Furniture")
            result.remove(u"Bed & Bath")
        elif u"Furniture & Lighting" in result:
            result.append(u"Bed, Bath & Furniture")
            result.remove(u"Furniture & Lighting")
        elif u"Tools" in result:
            result.append(u"Gear & Equipment")
            result.remove(u"Tools")
    if u"Home" in result:
        if u"Accessories" in result:
            result.append(u"Home Accessories")
            result.remove(u"Accessories")
        elif u"Intimates & Loungewear" in result:
            result.append(u"Bed & Bath")
            result.remove(u"Intimates & Loungewear")

    # Validation
    result = list(set(result))
    newresult = []
    for k, v in CATS.items():
        for sub in v:
            if k in result and sub in result:
                newresult.extend([k, sub])
    newresult.extend(list(set(result) & set(keys)))
    result = list(set(newresult))

    # reorder
    for key in keys:
        if key in result and key != result[0]:
            result.remove(key)
            result = [key] + result

    return result

            
words_split = re.compile('''[A-Za-z0-9\-%.]+''')
rules_dict = load_rules()
def classify_product_department(site, product, use_event_info=False, return_judge=False):
    m = get_site_module(site)
    p = product
    result = []
    title = p.title
    if not title:
        title = u""

    if use_event_info:
        for eid in p.event_id:
            e = m.Event.objects.get(event_id=eid)
            title = e.sale_title + u" " + title

    title = preprocess(title)

    if site in ["bluefly", "ideeli", "nomorerack", "onekingslane"]:
        title = u" ".join(p.cats) + " " + title

    if site in ["lot18"]:
        for tag in p.tagline:
            if "white wine" in tag.lower():
                if return_judge:
                    return [u"Wine", u"White Wine"], [u"Wine", u"White Wine"]
                else:
                    return [u"Wine", u"White Wine"]
            elif "red wine" in tag.lower():
                if return_judge:
                    return [u"Wine", u"Red Wine"], [u"Wine", u"Red Wine"]
                else:
                    return [u"Wine", u"Red Wine"]
            elif "sparkling" in tag.lower() or "champagne" in tag.lower():
                if return_judge:
                    return [u"Wine", u"Champagne"], [u"Wine", u"Champagne"]
                else:
                    return [u"Wine", u"Champagne"]

    kws = words_split.findall(title.lower())
    
    # check level-0 rules
    # first run: single words
    judge = [' '.join(kws)]
    level12 = True
    kws_set = set(kws) 

    for rule in rules_dict['0']:
        if not rule[0].difference(kws_set):
            result.extend(rule[1])
            level12 = False
            judge.append(['0']+rule)
            break
    
    if level12:
        # merge events info
        if p.event_id and site != 'venteprivee':
            d1 = []
            for eid in p.event_id:
                e = m.Event.objects.get(event_id=eid)
                d1.extend(classify_event_department(site, e))
            d1 = list(set(d1))
            judge.append(['B']+d1)
            result.extend( d1 )

        # do level1 and level2 classifying
        for priority in '12':
            found = False
            # last two keyword is most important, do it first
            for rule in rules_dict[priority]:
                if kws and len(rule[0])==2 and (not rule[0].difference(set(kws[-2:]))):
                    result.extend(rule[1])
                    judge.append([priority+'a']+rule)
                    found = True
                    break
            if found:
                continue

            # last keyword is most important, do it first
            for rule in rules_dict[priority]:
                if kws and (not rule[0].difference(set([kws[-1]]))):
                    result.extend(rule[1])
                    judge.append([priority+'b']+rule)
                    found = True
                    break
            if found:
                continue

            # then general keywords
            for rule in rules_dict[priority]:
                if not rule[0].difference(kws_set):
                    result.extend(rule[1])
                    judge.append([priority+'c']+rule)
                    break

    result = postprocess(site, p, result)

    # if we can't identify the product from it's title alone, try again with event info
    keys = [k.decode('utf-8') for k in  CATS.keys()]
    if use_event_info == False and (not (set(result) - set(keys))):
        if return_judge:
            result, judge = classify_product_department(site, product, use_event_info=True, return_judge=True)
        else:
            result = classify_product_department(site, product, use_event_info=True, return_judge=False)

    if return_judge:
        return result, judge
    else:
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
    import time
    import random
    from web import sites
    for site in sites:
        site = 'beyondtherack'
        m = get_site_module(site)
        count = m.Product.objects().count()
        index = random.randint(0, count-1)
        count = 0
        total = 0
        for p in m.Product.objects():
            words = classify_product_department(site, p)
            total += 1
            if not (set(words) - set(CATS.keys())):
                print "TITLE ==>", p.title
                print "==>", site, words
                count += 1
                print 1. * count/total * 100, '%'

def extract_pattern(site = 'bluefly'):
    m = get_site_module(site)
    from collections import Counter
    from pprint import pprint
    wc = Counter()
    wrongs = 0
    for p in m.Product.objects().only('title','cats','event_id'):
        if p.title:
            title = p.title.strip()
            depts = classify_product_department(site, p)
            if not (set(depts) - set(CATS.keys())):
                wrongs += 1
                title = preprocess(title)
                words = words_split.findall(title)
                title = ' '.join(words)
                for i in range(len(words)):
                    phrase = u' '.join(words[i:])
                    wc[phrase] += 1
                from termcolor import colored
                print title, colored('=>','red'), depts, p.title
    pprint(wc.most_common(1000))
    print 1. * wrongs / m.Product.objects.count() * 100, '%'

def extract_pattern2():
    from feature import sites
    from collections import Counter
    from pprint import pprint
    import sys
    wc = Counter()
    for site in sites:
        m = get_site_module(site)
        for p in m.Product.objects().only('title'):
            if not p.title:
                p.delete()
                continue
            title = p.title.strip().lower()
            if title:
                title = preprocess(title)
                words = words_split.findall(title)
                for i in range(len(words)):
                    phrase = u' '.join(words[i:])
                    wc[phrase] += 1
                sys.stdout.write(title+'\n')
                sys.stdout.flush()   

    with open('wc_most_common','w') as f:
        for phrase, counts in wc.most_common():
            f.write('{0} -> {1}\n'.format(phrase.encode('utf-8'), counts))

if __name__ == '__main__':
    m = get_site_module('beyondtherack')
    p = m.Product.objects.get(pk='COCTP400510FTP')
    print classify_product_department('beyondtherack', p, return_judge=True)
    exit(0)
    #extract_pattern2()

    from feature import sites
    for site in sites:
        extract_pattern(site)

    #test_product()
    #for rule in load_rules()['0']:
    #    print rule[0]
