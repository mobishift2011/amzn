from crawlers.myhabit.simpleclient import Myhabit
from crawlers.gilt.simpleclient import Gilt
from crawlers.ruelala.simpleclient import Ruelala
from crawlers.lot18.simpleclient import Lot18
from crawlers.hautelook.simpleclient import Hautelook
from crawlers.nomorerack.simpleclient import Nomorerack
from crawlers.onekingslane.simpleclient import Onekingslane
import os

hautelook = Hautelook()
myhabit = Myhabit()
gilt = Gilt()
ruelala = Ruelala()
lot18 = Lot18()
nomorerack = Nomorerack()
onekingslane = Onekingslane()

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def do_fetch():
    print 'started to fetch'
    with open('links.txt') as f:
        dept, subdept = '', ''
        for l in f:
            if not l:
                continue

            if l.startswith('http'):
                if l.startswith('http://www.myhabit.com'):
                    client = myhabit
                elif l.startswith('http://www.gilt.com'):
                    client = gilt
                elif l.startswith('http://www.ruelala.com'):
                    client = ruelala
                elif l.startswith('http://www.lot18.com'):
                    client = lot18
                elif l.startswith('http://www.hautelook.com'):
                    client = hautelook
                elif l.startswith('http://nomorerack.com') or l.startswith('http://www.nomorerack.com'):
                    client = nomorerack
                elif l.startswith('https://www.onekingslane.com'):
                    client = onekingslane
                else:
                    raise ValueError('client not found: '+l)

                url = l.strip()
                try:
                    name, content = client.get_product_abstract_by_url(url)
                except:
                    import traceback
                    traceback.print_exc()
                    print 'failed', url
                    continue

                fname = 'dataset'+'/'+dept+'|'+subdept+'/'+name.replace('/','_')
                fname = fname.encode('ascii', 'xmlcharrefreplace')
                ensure_dir(fname)

                open(fname,'w').write(content)

                print fname

            elif l.startswith('   '):
                subdept = l[1:].strip()
            else:
                if l.strip() != '':
                    dept = l.strip()

if __name__ == '__main__':
    do_fetch()
