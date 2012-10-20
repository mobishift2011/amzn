#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kwt import AdwordsAutomater, CREDENTIALS

for email, passwd in CREDENTIALS[1:]:
    aa = AdwordsAutomater(email, passwd, timeout=30)
    while True:
        aa.find_keyword_volumes(['ipad','cars','kindle'])
        print "press Y to continue or N to search again(Y/n)"
        key = raw_input()
        if (not key) or key.upper() != 'N':
            break
    aa.ff.quit()
