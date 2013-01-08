# -*- coding: utf-8 -*-

from powers.models import Brand
import requests
import json
import os
from helpers.log import getlogger

logger = getlogger('brandimport', filename='/tmp/brandimport.log')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djCatalog.djCatalog.settings")
from djCatalog.catalogs.models import Brand as EditBrand

__host = 'http://mongodb.favbuy.org:1317'
__urls = {
    'import': '{0}/brands/import'.format(__host),
    'refresh': '{0}/brands/refresh'.format(__host) 
}

def import_brands(payloads):
    '''
    Update the db of power.brand on mongodb server.
    '''
    try:
        r = requests.post(__urls['import'], data={'brand': json.dumps(payloads)})
        r.raise_for_status()
        return True
    except Exception as e:
        logger.error('Brands {0} post exception: {1}'.format(payloads, str(e)))
        return False

def refresh_brands():
    '''
    Notify to refresh the brands index in the memory for brand extraction on text server.
    '''
    try:
        r = requests.post(__urls['refresh'])
        r.raise_for_status()
    except Exception as e:
        logger.error('Brands notification exception: {0}'.format(str(e)))

def update_brands():
    ebs = EditBrand.objects()
    counter = 0
    for eb in ebs:
        ret = import_brands(eb.to_json())
        counter += 1
        if ret:
            print counter, 'brand import ok'
        else:
            print counter, 'brand import failed'
    refresh_brands()

if __name__ == '__main__':
    import time
    start = time.time()
    update_brands()
    print 'cost {0} s.'.format(int(time.time()-start))