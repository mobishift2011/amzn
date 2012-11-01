#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import lxml.html
import re
from datetime import datetime, timedelta
#from settings import *
#from models import *

import requests
import json
import itertools

url = 'http://www.hautelook.com/v3/events'
upcoming_url = 'http://www.hautelook.com/v3/events?upcoming_soon_days=7'

resp = requests.get(upcoming_url)
data = json.loads(resp.text)
lay1 = data['events']
lay2_upcoming, lay2_ending_soon, lay2_today = lay1['upcoming'], lay1['ending_soon'], lay1['today']
for event in itertools.chain(lay2_upcoming, lay2_ending_soon, lay2_today):
    info = event['event']
    event_id = info['event_id']
    sale_description = requests.get(info['info']).text
    event_id = info['']


if __name__ == '__main__':
    pass

