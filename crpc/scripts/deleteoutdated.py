from backends.matching.feature import sites
from datetime import datetime
from settings import MASTIFF_HOST
import requests
import threading

def get_site_module(site):
    return __import__('crawlers.'+site+'.models', fromlist=['Category', 'Event', 'Product'])

def outdate(site):
    utcnow = datetime.utcnow()
    m = get_site_module(site)
    if hasattr(m, 'Event'):
        for e in m.Event.objects(events_end__lt=utcnow):
            print 'DELETING', site, e.sale_title
            for p in m.Product.objects(event_id=e.event_id):
                if p.muri:
                    url = MASTIFF_HOST+p.muri[7:]
                    requests.delete(url)
                p.delete()
            if e.muri:
                url = MASTIFF_HOST+e.muri[7:]
                requests.delete(url)
            e.delete()

jobs = []
for site in sites:
    job = threading.Thread(target=outdate, args=(site,))
    job.start()
    jobs.append(job)

for j in jobs:
    j.join()

