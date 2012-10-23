from bottle import route, run, template, static_file
from os.path import join, dirname

@route('/assets/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=join(dirname(__file__), 'assets'))

@route('/')
def index():
    return template('index')

run(host='localhost', port=8080)
