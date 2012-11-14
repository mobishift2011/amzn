import traceback
from zerorpc import Client
from backends.monitor.scheduler import get_rpcs

for c in get_rpcs():
    try:
        print c
        c.call('test','123')
    except:
        traceback.print_exc()
