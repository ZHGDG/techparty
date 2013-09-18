# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-

from bottle import Bottle
from bottle import __version__ as bottleVer
from bottle import debug, run
from bottle import redirect, abort, error
from bottle import request, response, local
from bottle import static_file
#from bottle import template
#from bottle import jinja2_view as view
from bottle import jinja2_template as template
from bottle import TEMPLATE_PATH

#from mysession import get_session_info, set_session_info
#from mysession import deco_session_check

from config import JINJA2TPL_PATH
TEMPLATE_PATH.insert(0, JINJA2TPL_PATH)
#from config import CUSTOM_TPL_PATH
#TEMPLATE_PATH.insert(0, CUSTOM_TPL_PATH)


APP = Bottle()

#APP.mount('/up', __import__('mana4up').APP)
APP.mount('/api', __import__('mana4api').APP)
#APP.mount('/mana', __import__('mana4sys').APP)

#run(host='10.33.6.22', port=8080)

'''
from bottle import install
from cors_plugin import RequestPreflightPlugin
request_preflight_plugin = RequestPreflightPlugin( allow_origin = '*'
    ,preflight_methods = [ 'GET', 'POST', 'PUT', 'DELETE', 'OPTION' ]
    ,ttl = 3600 )
APP.install( request_preflight_plugin )
'''




@APP.route('/')
#@view('404.html')
def index():
    return template('index.html')

#@view('404.html')
@APP.error(404)
def error404(error):
    return template('404.html')

@APP.route('/favicon.ico')
def favicon():
    abort(204)
    
@APP.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static')
    
@APP.route('/center')
def handel_redirect():
    return redirect(request.path+'/')


if __name__ == '__main__':
    debug(True)
    #0.0.0.0
    run(app, host="0.0.0.0",reloader=True)
