import esmre
import esm
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
