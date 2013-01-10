import os
import tornado.ioloop
import tornado.web
import tornado.httpserver
from webassets import Environment as AssetsEnvironment, loaders
from webassets.ext.jinja2 import AssetsExtension
import jinja2 

class Jinja2Environment(jinja2.Environment): 
    def load(self, template_path): 
        tmpl = self.get_template(template_path) 
        if tmpl: 
            setattr(tmpl, "generate", tmpl.render) 
        return tmpl 

ROOT = os.path.dirname(__file__)
TEMPLATE_PATH = os.path.join(ROOT+"views")
STATIC_PATH = os.path.join(ROOT+"assets")

assets_env = AssetsEnvironment(STATIC_PATH, '/assets')
bundles = loaders.YAMLLoader(os.path.join(ROOT, "bundle.yaml")).load_bundles()
for name, bundle in bundles.iteritems():
    assets_env.register(name, bundle)
JINJA2_ENV = Jinja2Environment(extensions=[AssetsExtension],
                                loader=jinja2.FileSystemLoader(TEMPLATE_PATH))
JINJA2_ENV.assets_environment = assets_env

class BaseHandler(tornado.web.RequestHandler): 
    def __init__(self, *args, **kwargs): 
        tornado.web.RequestHandler.__init__( self, *args, **kwargs ) 
        self.jinja2_env = self.settings.get("jinja2_env") 

    def render_string(self, template_name, **kwargs): 
        # if the jinja2_env is present, then use jinja2 to render templates: 
        if self.jinja2_env: 
            return self.jinja2_env.get_template(template_name).render(**kwargs)
        else:
            return tornado.web.RequestHandler.render_string(self, template_name, **kwargs) 

class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")

class ExampleHandler(BaseHandler):
    def get(self, module):
        self.render('examples/'+module+'.html')

settings = {
    "static_path": STATIC_PATH,
    "template_path": TEMPLATE_PATH,
    "cookie_secret": "637d1f5c6e6d1be22ed907eb3d223d858ca396d8",
    "jinja2_env": JINJA2_ENV,
    "login_url": "/login",
    "xsrf_cookies": True,
}

application = tornado.web.Application([
    (r"/(ui|form|chart|typography|gallery|table|calendar|grid|file-manager|tour|icon|error|login)/", ExampleHandler),
    (r"/", IndexHandler),
    (r"/assets/(.*)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
], **settings)

if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(application)
    server.bind(8888)
    server.start(1)
    tornado.ioloop.IOLoop.instance().start()

