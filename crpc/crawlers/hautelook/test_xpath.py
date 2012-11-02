#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: bishop Liu <miracle (at) gmail.com>

import requests
import json
import itertools
from datetime import datetime, timedelta
from crawlers.common.stash import *

headers = { 
    'Accept': 'application/json',
    'Accept-Charset': 'UTF-8,*;q=0.5',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,en-US;q=0.8,en;q=0.6',
    'Auth': 'HWS a5a4d56c84b8d8cd0e0a0920edb8994c',
    'Connection': 'keep-alive',
    'Content-encoding': 'gzip,deflate',
    'Content-type': 'application/json',
    'Host': 'www.hautelook.com',
    'Referer': 'http://www.hautelook.com/events',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Ubuntu/12.10 Chromium/22.0.1229.94 Chrome/22.0.1229.94 Safari/537.4',
    'X-Requested-With': 'XMLHttpRequest',
}

config = { 
    'max_retries': 3,
    'pool_connections': 10, 
    'pool_maxsize': 10, 
}

request = requests.Session(prefetch=True, timeout=17, config=config, headers=headers)

#    http://www.hautelook.com/event/ + event_id    # event page
#    http://www.hautelook.com/content/ + event_id  # event discription page

def convert_time(date_str):
    # '2012-10-31T08:00:00-07:00'
    date, time = date_str.split('T')
    time_str = date + '-' + time.split('-')[0]
    fmt = "%Y-%m-%d-%X"
    hours, minutes = time.split('-')[1].split(':')
    return datetime.strptime(time_str, fmt) - timedelta(hours=int(hours), minutes=int(minutes))

def fetch_json():
    url = 'http://www.hautelook.com/v3/events'
    upcoming_url = 'http://www.hautelook.com/v3/events?upcoming_soon_days=7'

    resp = request.get(upcoming_url)
    data = json.loads(resp.text)
    return data
    lay1 = data['events']
    lay2_upcoming, lay2_ending_soon, lay2_today = lay1['upcoming'], lay1['ending_soon'], lay1['today']

    for event in itertools.chain(lay2_upcoming, lay2_ending_soon, lay2_today):
        info = event['event']

        event_id = info['event_id']
        sale_title = info['title']
        sale_description = requests.get(info['info']).text
        dept = [i['name'] for i in info['event_types']]

        event_code = info['event_code']
        pop_img = 'http://www.hautelook.com/assets/{0}/pop-large.jpg'.format(event_code)
        grid_img = 'http://www.hautelook.com/assets/{0}/grid-large.jpg'.format(event_code)
        image_url = [pop_img, grid_img]

        begin = convert_time( info['start_date'] )
        end = convert_time( info['end_date'] )

        sort_order = info['sort_order']
        tag = info['tagline']
        category = info['category']


if __name__ == '__main__':
    fetch_json()

