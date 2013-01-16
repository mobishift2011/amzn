#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.autoreload

import jinja2 

from webassets import Environment as AssetsEnvironment, loaders
from webassets.ext.jinja2 import AssetsExtension

import os
import json
from math import ceil
from slumber import API
from datetime import datetime, timedelta

def get_site_module(site):
    return __import__('crawlers.'+site+'.models', fromlist=['Category', 'Event', 'Product'])

class Pagination(object):
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

class Jinja2Environment(jinja2.Environment): 
    def load(self, template_path): 
        tmpl = self.get_template(template_path) 
        if tmpl: 
            setattr(tmpl, "generate", tmpl.render) 
        return tmpl

ROOT = os.path.dirname(__file__)
TEMPLATE_PATH = os.path.join(ROOT+"views")
STATIC_PATH = os.path.join(ROOT+"assets")
MASTIFF_URI = 'http://localhost:8001/api/v1'
api = API(MASTIFF_URI)

assets_env = AssetsEnvironment(STATIC_PATH, '/assets')
bundles = loaders.YAMLLoader(os.path.join(ROOT, "bundle.yaml")).load_bundles()
for name, bundle in bundles.iteritems():
    assets_env.register(name, bundle)
JINJA2_ENV = Jinja2Environment(extensions=[AssetsExtension],
                                loader=jinja2.FileSystemLoader(TEMPLATE_PATH))
JINJA2_ENV.assets_environment = assets_env

def imagesize(imageobj, wxh):
    if imageobj:
        w, h = wxh.split('x')
        w, h = (int(w), int(h))
        for size in imageobj['resolutions']:
            if h == 0 and w == size[0]:
                h = size[1]
        return imageobj['url'] + '_{0}x{1}'.format(w, h)

JINJA2_ENV.filters['imagesize'] = imagesize

class BaseHandler(tornado.web.RequestHandler): 
    def __init__(self, *args, **kwargs): 
        tornado.web.RequestHandler.__init__( self, *args, **kwargs ) 
        self.jinja2_env = self.settings.get("jinja2_env") 

    def prepare(self):
        if self.request.headers.get("Content-Type") == "application/json":
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None
    
    def get_current_user(self):
        user = self.get_secure_cookie('user')
        return user

    def render_string(self, template_name, **kwargs): 
        # if the jinja2_env is present, then use jinja2 to render templates: 
        if self.jinja2_env: 
            context = {
                'current_user': self.get_current_user,
                'xsrf_form_html': self.xsrf_form_html,
            }
            kwargs.update(context)
            return self.jinja2_env.get_template(template_name).render(**kwargs)
        else:
            return tornado.web.RequestHandler.render_string(self, template_name, **kwargs) 

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html")

class ExampleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, module):
        self.render('examples/'+module+'.html')

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if username == 'favbuy' and password == 'tempfavbuy':
            self.set_secure_cookie('user', username)
        next_url = self.get_argument('next', '/')
        self.redirect(next_url)

class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie('user')
        next_url = self.get_argument('next', '/')
        self.redirect(next_url)

class ViewDataHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, subpath):
        if not subpath:
            self.redirect('/viewdata/events')
        if subpath == 'events':
            self.render_events()
        elif subpath == 'products':
            self.render_products()
        elif subpath == 'classification':
            self.render_classification()

    def render_classification(self):
        from backends.matching.feature import sites
        from itertools import chain
        current_site = self.get_argument('site', sites[0])
        offset = self.get_argument('offset', '0')
        limit = self.get_argument('limit', '80')
        offset, limit = int(offset), int(limit)

        m = get_site_module(current_site)
        events, categories = [], []
        num_events = 0
        num_categories = 0
        if hasattr(m, 'Event'):
            events = m.Event.objects()
            num_events = len(events)
            if num_events <= offset:
                events = []
                offset -= num_events
            elif num_events >= offset+limit:
                events = events[offset:offset+limit]
                limit  = 0
            else:
                events = events[offset:]
                offset = 0
                limit -= (num_events - offset)
        if hasattr(m, 'Category'):
            categories = m.Category.objects()
            num_categories = len(categories)
            if limit == 0:
                categories = []
            else:
                categories = categories[offset:offset+limit]
        object_list = chain(events, categories)

        total_count = num_events + num_categories
        pagination = Pagination(offset/80+1, 80, total_count)

        self.render('viewdata/classification.html', sites=sites, current_site=current_site,
            object_list=object_list, pagination=pagination)

    def render_products(self):
        from backends.matching.feature import sites
        kwargs = {}
        for k, v in self.request.arguments.iteritems():
            kwargs[k] = v[0]

        offset = kwargs.get('offset', '0')
        limit = kwargs.get('limit', '20')
        kwargs['offset'] = int(offset)
        kwargs['limit'] = int(limit)

        result = api.product.get(**kwargs)
        meta = result['meta']
        products = result['objects']
        sites = ['ALL'] + sites
        times = {
           'onehourago': datetime.utcnow()-timedelta(hours=1),
           'onedayago': datetime.utcnow()-timedelta(days=1),
           'oneweekago': datetime.utcnow()-timedelta(days=7),
        }

        pagination = Pagination(int(offset)/20+1, 20, meta['total_count'])

        self.render('viewdata/products.html', meta=meta, products=products, sites=sites, 
            times=times, pagination=pagination)

    def render_events(self):
        from backends.matching.feature import sites
        kwargs = {}
        for k, v in self.request.arguments.iteritems():
            kwargs[k] = v[0]

        offset = kwargs.get('offset', '0')
        limit = kwargs.get('limit', '20')
        kwargs['offset'] = int(offset)
        kwargs['limit'] = int(limit)

        result = api.event.get(**kwargs)
        meta = result['meta']
        events = result['objects']
        sites = ['ALL'] + sites
        times = {
           'onehourago': datetime.utcnow()-timedelta(hours=1),
           'onedayago': datetime.utcnow()-timedelta(days=1),
           'oneweekago': datetime.utcnow()-timedelta(days=7),
        }

        pagination = Pagination(int(offset)/20+1, 20, meta['total_count'])

        self.render('viewdata/events.html', meta=meta, events=events, sites=sites, 
            times=times, pagination=pagination)

settings = {
    "debug": True,
    "static_path": STATIC_PATH,
    "template_path": TEMPLATE_PATH,
    "cookie_secret": "637d1f5c6e6d1be22ed907eb3d223d858ca396d8",
    "jinja2_env": JINJA2_ENV,
    "login_url": "/login/",
    "xsrf_cookies": True,
}

application = tornado.web.Application([
    (r"/examples/(ui|form|chart|typography|gallery|table|calendar|grid|file-manager|tour|icon|error|login)/", ExampleHandler),
    (r"/login/", LoginHandler),
    (r"/logout/", LogoutHandler),
    (r"/viewdata/(.*)", ViewDataHandler),
    (r"/", IndexHandler),
    (r"/assets/(.*)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
], **settings)

if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8888)
    server.start(1)
    ioloop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(ioloop)
    ioloop.start()
