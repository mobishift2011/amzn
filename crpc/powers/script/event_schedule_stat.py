# -*- coding: utf-8 -*-

from powers.configs import *
from crawlers.common.routine import get_site_module
from itertools import chain
from mongoengine import Q

from datetime import datetime, timedelta
import pytz

SITE_STAT = {}
TOTAL_STAT = {}

def count_schedule():
	now = datetime.utcnow()
	today = now.replace(hour=0, minute=0, second=0, microsecond=0)
	tomorrow = today + timedelta(days=1)

	for site in SITES:
		SITE_STAT[site] = {}
		m = get_site_module(site)

		if not hasattr(m, 'Event'):
			print 'site ', site, ' has not Event model\n'
			continue

		events = m.Event.objects(Q(events_begin__gte=today) & Q(events_begin__lte=tomorrow))
		for event in events:
			begin = str(event.events_begin.time())
			if begin not in SITE_STAT[site]:
				SITE_STAT[site][begin] = 1
			else:
				SITE_STAT[site][begin] += 1

if __name__ == '__main__':
	count_schedule()

	for site, value in chain(SITE_STAT.iteritems()):
		print site, ':'
		for time, count in chain(value.items()):
			print time, ' -> ', count
		print '\n'