from crawlers.myhabit.simpleclient import Myhabit
from crawlers.gilt.simpleclient import Gilt
from crawlers.ruelala.simpleclient import Ruelala
import os

myhabit = Myhabit()
gilt = Gilt()
ruelala = Ruelala()

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def do_fetch():
    print 'started to fetch'
    with open('from.txt') as f:
        dept, subdept = '', ''
        for l in f:
            l = l.strip() 
            if not l:
                continue

            if l.startswith('http://'):
                if l.startswith('http://www.myhabit.com'):
                    client = myhabit
                elif l.startswith('http://www.gilt.com'):
                    client = gilt
                elif l.startswith('http://www.ruelala.com'):
                    client = ruelala
                else:
                    raise ValueError('client not found: '+l)

                url = l
                try:
                    name, content = client.get_product_abstract_by_url(url)
                except:
                    print 'failed', url,
                    continue

                fname = 'dataset'+'/'+dept+'_'+subdept+'/'+name.replace('/','_')
                fname = fname.encode('ascii', 'xmlcharrefreplace')
                ensure_dir(fname)

                open(fname,'w').write(content)

                print fname

            elif l.startswith('?'):
                subdept = l[1:].strip().replace(' ','_').replace('/','_')

            else:
                dept = l.replace(' ','_').replace('/','_')

if __name__ == '__main__':
    do_fetch()
