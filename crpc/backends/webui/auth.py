# -*- coding: utf-8 -*-
#from bottle import request, response, HTTPError
#
#def protected(check, realm="private", text="Access denied"):
#    def decorator(func):
#        def wrapper(*a, **ka):
#            user, password = request.auth or (None, None)
#            if user is None or not check(user, password):
#                response.headers['WWW-Authenticate'] = 'Basic realm="%s"' % realm
#                return HTTPError(401, text)
#            return func(*a, **ka)
#        return wrapper
#    return decorator
#
#def check_valid_user(usr, pwd):
#    ''' Return True if username and password are valid. '''
#    return usr == 'admin' and pwd == 'secret'
#
#login_required = protected(check_valid_user)

from beaker.middleware import SessionMiddleware
import bottle
from bottle import route, post, request, redirect, template
 
bottle.debug(True) #remove in production
 
session_opts={
    'session.type':'file',
    'session.cookie_expires':3600,
    'session.data_dir':'./data',
    'session.auto':True
}

LOGIN_PAGE = "login.tpl"

def login_required(func):
    def check_login(*args,**kwargs):
        try:
            session=bottle.request.environ["beaker.session"]
        except KeyError:
            redirect('/login')
        if "is_login" in session and session["is_login"]==True:
            return func(*args,**kwargs)
        redirect('/login')
    return check_login

def login():
    bottle.request.environ["beaker.session"] = {}
    session=bottle.request.environ["beaker.session"]
    session["is_login"]=True
    return session
 
def logout():
    session=bottle.request.environ["beaker.session"]
    session["is_login"]=False
    redirect("/login")

@route("/login")
def login_get():
    return template(LOGIN_PAGE)

@post("/login")
def login_post():
    username = request.POST.get("username").strip()
    password=request.POST.get("password").strip()
    if True:#if username=='devadmin' and password=='tempfavbuy88':
        login()
        redirect('/task')
    else:
        return template(LOGIN_PAGE, {'login_failed': True})

#def login_post():
#    import hashlib
#    passwd=request.POST.get("pass").strip()
#    if hashlib.new("md5", passwd).hexdigest()=="xxx":
#        login()
#    redirect("./login.html")
 
@route("/logout.html")
def logout_get():
    logout()