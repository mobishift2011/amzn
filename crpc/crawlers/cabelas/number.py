#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

con = pymongo.Connection('127.0.0.1')
col = con['cabelas']['category']
num = col.find({'is_leaf': True, 'num': {'$exists': True}}, fields=['cats', 'num'], timeout=False)
total = 0
for i in num:
    total += int(i['num'])

#with open('file.txt', 'w') as fd:
#    for i in num:
#        total += int(i['num'])
#        fd.write(i['catstr']+'\t'+str(i['num'])+'\n')
#
print total
