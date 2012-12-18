import esm
import esmre
import ahocorasick
import acora
import os
import time
import string
import datrie
import re

RUNS = 1000

s = '''Men > Tailorbyrd
Event Ends THU NOV 29 at 9 AM PT
Button-Down Multistripe Shirt
Mid-weight woven cotton with casual button-down collar, patch pocket, 1-button angled cuff, regular fit
Fabric: 100% cotton
Care instructions: Machine wash
Measurements: shoulder to hemline 31.5", sleeve length 25.5", taken from size M
Country of origin: China
Authentic product
International shipping available
May be returned within 21 days'''

s = s.lower()


tags = [ t.lower() for t in open('tags.list').read().split('\n') if t ]
for i in range(1000,9999):
    tags.append(str(i))


i1 = esm.Index()
i2 = esmre.Index()
i3 = datrie.Trie(string.ascii_lowercase)
i4 = set()

t1 = time.time()

for tag in tags:
    i1.enter(tag)
    i2.enter(tag, tag)
    i3[unicode(tag)] = 1
    i4.add(tag)
i1.fix() 
t2 = time.time()

for _ in xrange(RUNS):
    i1.query(s)
    
t3 = time.time()

for _ in xrange(RUNS):
    i2.query(s)

t4 = time.time()

print 'bootstrap', t2 - t1
print 'esm', t3 - t2
print 'esmre', t4 - t3

print 'esm result', i1.query(s)
print 'esmre result', i2.query(s)

stoptoken = re.compile(r'[ \t\r\n,;.%\d+\'\"_-]')

def splitmatch(s,d):
    ret = []
    for x in stoptoken.split(s):
        if x:
            if unicode(x) in d:
                ret.append(x)
    return ret


t5 = time.time()
for _ in xrange(RUNS): 
   splitmatch(s, i3)
print splitmatch(s, i3)
print 'datrie', time.time() - t5

t5 = time.time()
for _ in xrange(RUNS): 
   splitmatch(s, i4)
print splitmatch(s, i4)
print 'native set', time.time() - t5


def get_data():
    data = {}
    for dept_subdept in os.listdir('dataset'):
        for site_key in os.listdir(os.path.join('dataset', dept_subdept)):
            content = open(os.path.join('dataset', dept_subdept, site_key)).read()
            data[site_key] = content
    return data

class Esm(object):
    def __init__(self):
        self.dataset = globals()['get_data']()
        self.i1 = esm.Index()
        for tag in tags:
            self.i1.enter(tag)
        self.i1.fix() 

    def inquire(self):
        hit_list = []
        for k, v in self.dataset.iteritems():
            for pos, hit_word in self.i1.query(v.lower()):
                hit_list.append(hit_word)
        return hit_list


class Esmre(object):
    def __init__(self):
        self.dataset = globals()['get_data']()
        self.i2 = esmre.Index()
        for tag in tags:
            self.i2.enter(tag, tag)

    def inquire(self):
        hit_list = []
        for k, v in self.dataset.iteritems():
            for hit_word in self.i2.query(v.lower()):
                hit_list.append(hit_word)
        return hit_list


class Ahocorasick(object):
    def __init__(self):
        self.dataset = globals()['get_data']()
        self.__tree = ahocorasick.KeywordTree()
        for tag in tags:
            self.__tree.add(tag)
        self.__tree.make()

    def inquire(self):
        hit_list = []
        for k, v in self.dataset.iteritems():
            for start, end in self.__tree.findall(v.lower()):
                hit_list.append(v[start:end])
        return hit_list

class Acora(object):
    def __init__(self):
        self.dataset = globals()['get_data']()
        self.__builder = acora.AcoraBuilder()
        for tag in tags:
            self.__builder.add(tag)
        self.__tree = self.__builder.build()

    def inquire(self):
        hit_list = []
        for k, v in self.dataset.iteritems():
            for hit_word, pos in self.__tree.finditer(v.lower()):
                hit_list.append(hit_word)
        return hit_list

if __name__ == '__main__':

    print '\n\n\n'
    t0 = time.time()
    esm_obj = Esm()
    t1 = time.time()
    esmre_obj = Esmre()
    t2 = time.time()
    ahocorasick_obj = Ahocorasick()
    t3 = time.time()
    acora_obj = Acora()
    t4 = time.time()

    esm_init = t1 - t0
    esmre_init = t2 - t1
    ahocorasick_init = t3 - t2
    acora_init = t4 - t3
    print 'esm init: %f' % esm_init
    print 'esmre init: %f' % esmre_init
    print 'ahocorasick init: %f' % ahocorasick_init
    print 'acora init: %f' % acora_init

    a1 = esm_obj.inquire()
    t5 = time.time()
    a2 = esmre_obj.inquire()
    t6 = time.time()
    a3 = ahocorasick_obj.inquire()
    t7 = time.time()
    a4 = acora_obj.inquire()
    t8 = time.time()

    esm_process = t5 - t4
    esmre_process = t6 - t5
    ahocorasick_process = t7 - t6
    acora_process = t8 - t7
    print 'esm process: %f, hit: %d' % (esm_process, len(a1))
    print 'esmre process: %f, hit: %d' % (esmre_process, len(a2))
    print 'ahocorasick process: %f, hit: %d' % (ahocorasick_process, len(a3))
    print 'acora process: %f, hit: %d' % (acora_process, len(a4))

