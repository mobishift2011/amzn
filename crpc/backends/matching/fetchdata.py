from crawlers.myhabit.simpleclient import Myhabit
from crawlers.gilt.simpleclient import Gilt
import os

myhabit = Myhabit()
gilt = Gilt()

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def do_fetch():
    with open('from.txt') as f:
        dept, subdept = '', ''
        for l in f:
            l = l.strip() 
            if not l:
                continue

            if l.startswith('http://'):
                if l.startswith('http://www.myhabit.com'):
                    client = myhabit
                elif l.startswith('http://www.gilt'):
                    client = gilt
                else:
                    raise ValueError('client not found: '+l)

                url = l
                try:
                    name, content = client.get_product_abstract_by_url(url)
                except:
                    continue

                fname = 'dataset'+'_'+dept+'_'+subdept+'/'+name.replace('/','_')
                ensure_dir(fname)

                try:
                    open(fname,'w').write(content.encode('utf-8'))
                except:
                    continue

                print fname
                print content
                print
                print
                print

            elif l.startswith('?'):
                subdept = l[1:].strip().replace(' ','_').replace('/','_')

            else:
                dept = l.replace(' ','_').replace('/','_')

if __name__ == '__main__':
    do_fetch()
