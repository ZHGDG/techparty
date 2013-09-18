# -*- coding: utf-8 -*-
#import os
import time
import traceback
#import json
import urllib2 as urilib
from copy import deepcopy
#from tempfile import TemporaryFile
#from StringIO import StringIO
#from shutil import copyfileobj
import pprint
pp = pprint.PrettyPrinter(indent=4)

import sae
import sae.storage
import sae.kvdb
import pylibmc
import xml.etree.ElementTree as etree

from bottle import Bottle
from bottle import __version__ as bottleVer

from bottle import debug, run
from bottle import redirect, abort
from bottle import request, response, local
from bottle import get, post, put, delete
from bottle import BaseRequest
from bottle import static_file
#from bottle import template
#from bottle import jinja2_view as view
from bottle import jinja2_template as template
from bottle import TEMPLATE_PATH

#import urllib2 as urilib
from auth import auth_required, sha256_uhex
from lb4crx2cli import __genRESTsign


from utility import INCR4KV as __incr
from utility import TSTAMP, GENID
from utility import POP4KV, POP4LIST, INS2LIST, INS2DICT4LIST, IDX4LIST
from utility import ST4CRX, KV4CRX, KV4GRP
from utility import INIobjSYS, PUTHIS, PUT2SS, PUT_PIC4CRX
from config import CFG

debug(True)
APP = Bottle()

KV = sae.kvdb.KVClient(debug=1)
#SG = sae.storage.Client()

#@APP.get('/echo/?<qstr>')
#@APP.get('/echo/<qstr>')
@APP.get('/echo')
@APP.get('/echo/')
def echo_wechat():
    print request.query.keys()
    print request.query.echostr
    #print request.query_string
    #print dir(BaseRequest.query_string)
    return request.query.echostr
@APP.post('/echo')
@APP.post('/echo/')
def wechat_post():
    #print request.forms.keys()[0]
    xml = etree.XML(request.forms.keys()[0])
    fromUser = xml.findtext("ToUserName")
    toUser = xml.findtext("FromUserName")
    #print xml.findtext("CreateTime")
    #__MsgId = xml.findtext("MsgId")
    __MsgType = xml.findtext("MsgType")
    __Content = xml.findtext("Content")
    if "text" == __MsgType:
        if "h" == __Content:
            tStamp = TSTAMP()
            content = "是也乎"
            print CFG.TPL_TEXT% locals()
            return CFG.TPL_TEXT% locals()
    return None 






from operator import itemgetter
def pep265sd(d,doreverse=False):
    '''proposed in PEP 265, using  the itemgetter
    '''
    return sorted(d.iteritems(), key=itemgetter(1), reverse=doreverse)
@APP.route('/sysincr')
#@APP.route('/<ddd>/sysincr')
def sysincr():
    from utility import INCR4KV as __incr
    #kv = sae.kvdb.KVClient()
    #print  kv.get_info()
    return str(__incr())
    
    '''
    kv = sae.kvdb.KVClient()
    print dir(kv)
    print kv.get_info()
    print kv.get("TOT")
    
    if not kv.get("TOT"):
        kv.add("TOT", 1)
    print kv.get("TOT")
    print type(kv.get("TOT")+1)
    
    kv.replace("TOT",kv.get("TOT")+1)
    print kv.get("TOT")
    
    return str(kv.get("TOT"))
    '''



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
    




