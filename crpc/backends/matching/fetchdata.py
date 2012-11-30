from crawlers.myhabit.server2 import Server as Myhabit
import os

myhabit = Myhabit()

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
                url = l
                name, content = myhabit.get_product_abstract_by_url(url)
                fname = dept+'_'+subdept+'/'+name.replace('/','_')
                ensure_dir(fname)
                open(fname,'w').write(content.encode('utf-8'))
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
