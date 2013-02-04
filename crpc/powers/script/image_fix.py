# -*- coding: utf-8 -*-
from settings import CRPC_ROOT
from powers.configs import AWS_ACCESS_KEY, AWS_SECRET_KEY
from powers.tools import ImageTool
from powers.routine import get_site_module
from boto.s3.connection import S3Connection
from crawlers.common.stash import exclude_crawlers
from os import listdir
from os.path import join, isdir 

__s3conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)

def crawl_images(instance, site, model):
    it = ImageTool(connection=__s3conn)
    key = 'event_id' if model.lower() == 'event' else 'key'
    it.crawl(instance.image_urls, site, model, getattr(instance, key), thumb=True)
    if it.image_complete:
        instance.image_path = it.image_path
        instance.image_complete = bool(instance.image_path)
        instance.save()


def try_to_fix(event):
    if event.image_path and not event.image_path[0].get('resolutions'):
        print event.event_id, event.image_path[0]
        return True
    return False


def fix_events_images(m, site):
    try:
        events = m.Event.objects()
    except AttributeError:
        print site
        return

    print 'fixing event -> {0} ...'.format(site)
    for event in events:
        if try_to_fix(event):
            crawl_images(event, site, 'event')


def main():
    for name in listdir(join(CRPC_ROOT, "crawlers")):
        path = join(CRPC_ROOT, "crawlers", name)
        if name in exclude_crawlers or not isdir(path):
            continue

        m = __import__("crawlers."+name+'.models', fromlist=['Event', 'Product'])
        fix_events_images(m, name)


if __name__ == '__main__':
    main()