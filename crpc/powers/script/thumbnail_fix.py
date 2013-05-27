from boto.s3.connection import S3Connection
from PIL import Image
from cStringIO import StringIO
from settings import MASTIFF_HOST
from crawlers.common.stash import picked_crawlers
from powers.configs import *
from powers.routine import get_site_module
from powers.tools import ImageTool
from optparse import OptionParser
import requests
import slumber
import os, sys
import traceback

api = slumber.API(MASTIFF_HOST)

print 'connecting to s3...'
__s3conn = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
it = ImageTool(connection=__s3conn)
print 'connected'; print

def thumbnail(instance, doctype):
    updated = False

    for image_dict in instance.image_path:
        url = image_dict['url']
        resolutions = image_dict['resolutions']
        image = None

        urlsplits = url.rsplit('/')
        key = os.path.join(urlsplits[-4], urlsplits[-3], urlsplits[-2], urlsplits[-1])

        for size in IMAGE_SIZE[doctype]:
            width, height = size['width'], size['height']
            policy, color = size['thumbnail-policy'], size['background-color']

            if not width or not height or [width, height] in resolutions:
                print url, ' skip ', (width, height)
                continue
            
            if not image:
                print 'downloading: ', url
                MAX_RETRIES = 3
                for i in xrange(MAX_RETRIES):
                    try:
                        image = it.download(url)
                        break
                    except requests.exceptions.ConnectionError:
                        if i >= 2:
                            print traceback.format_exc()
                            return False
                        continue

            print [width, height], 'not in, begin to thumbnail...'
            
            im = Image.open(StringIO(image))
            fileobj, realsize = it.create_thumbnail(im, (width, height), policy, color)
            width, height = realsize
            resolutions.append(realsize)

            path, name = os.path.split(key)
            thumbnail_name = '{name}_{width}x{height}'.format(width=width, height=height, name=name)
            im_key = os.path.join(path, thumbnail_name)
            it.upload2s3(fileobj, im_key)
            updated = True
            print im_key

        print
    
    return updated

def main(sites=[], doctype='Product'):
    doctype = doctype.capitalize()
    sites = sites or picked_crawlers
    for site in sites:
        m = get_site_module(site)
        try:
            instances = getattr(m, doctype).objects().timeout(False)
        except AttributeError:
            print traceback.format_exc()
            continue
        print 'site: ', site
        print 'total {0}: {1}: '.format(doctype, len(instances))

        for instance in instances:
            if thumbnail(instance, doctype):
                if instance.muri:
                    params = {'cover_image': instance.image_path[0], 'images': instance.image_path} \
                        if doctype == 'Product' else {'cover_image': instance.image_path[0]}
                    getattr(api, doctype.lower())(instance.muri.split("/")[-2]).patch(params)

                    print 'updating ', doctype, instance.key if doctype == 'Product' else instance.event_id
                    instance.save()
            print

        print; print

if __name__ == '__main__':
    parser = OptionParser(usage='usage: %prog [options]')
    parser.add_option('-s', '--site', dest='site', help='site info', default='')
    options, args = parser.parse_args(sys.argv[1:])
    if options.site:
        sites = options.site.split()
        main(sites = sites)

    else:
        main()