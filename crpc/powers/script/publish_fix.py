#! /usr/bin/env python
# -*- coding: utf-8 -*-
from crawlers.common.stash import picked_crawlers
from powers.routine import get_site_module
from publisher.publish import Publisher
from helpers.log import getlogger
from datetime import datetime, timedelta
import sys

logger = getlogger("publish_fixer")
publisher = Publisher()

three_days_ago = datetime.utcnow() - timedelta(days=3)

def fix_event(site, event):
    logger.debug('To fix {} event: {}'.format(site, event.event_id))
    publisher.publish_event(event, upd=True)

def fix_product(site, product):
    logger.debug('To fix {} product: {}'.format(site, product.key))
    publisher.publish_product(product, upd=True)

def main(sites=None):
    if sites is None:
        sites = picked_crawlers
    for site in sites:
        logger.info('site: {}'.format(site))
        mod = get_site_module(site)

        if hasattr(mod, 'Event'):
            for event in mod.Event.objects(create_time__lt=three_days_ago):
                logger.info('{} event: {}'.format(site, event.event_id))
                fix_event(site, event)

        for product in mod.Product.objects(create_time__lt=three_days_ago):
            logger.info('{} product: {}'.format(site, product.key))
            fix_product(site, product)

if __name__ == '__main__':
    sites = (sys.argv[1],) if len(sys.argv) > 1 else None
    main(sites)