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

@APP.route('/')
def api():
    #print "\t/api by Bottle %s"% bottleVer
    return "\t/api by Bottle %s"% bottleVer
    #return template('api.tpl')
    #redirect('/api/%s/sysincr'% 123)


@APP.route('/cron/dlrank', method='OPTIONS')
@APP.route('/dc/<uuid>', method='OPTIONS')
@APP.route('/dc/add/<uuid>', method='OPTIONS')
@APP.route('/dc/dlrank/<order>', method='OPTIONS')
def CORSupport(uuid):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Headers', 'x-requested-with')
    #print "\t>>>OPTIONS"
    
    
#@APP.route('/dc/<uuid>', method='OPTIONS')
#@APP.route('/dc/<:re:.*>', method='OPTIONS')
#@APP.route('/dc/<uuid>', method='OPTIONS')
#@APP.route('/dc/<:re:.*>', method='OPTIONS')
def cors():
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Headers', 'x-requested-with')
    #response.set_header('Content-Type','application/json; charset=utf-8')
    


@APP.route('/dc/<uuid>', method='GET')
def apidc(uuid):
    #print "\t>>>GET"
    result = {}
    crx = KV.get(uuid)
    if crx:
        crx['dlrank'] = int(crx['dlrank'])
        #KV.set(uuid, crx)
        result['dc'] = crx['dlrank']
        result['success'] = 1
    else:
        result['msg'] = "%s NOT exist!"
        result['success'] = 0
    result['method'] = "GET"
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Headers', 'x-requested-with')
    response.set_header('Content-Type','application/json; charset=utf-8')
    return result
    #return "callback($scope,['%s','%s'])"%('GET',AJS)
    


@APP.route('/dc/add/<uuid>', method='GET')
def addc(uuid):
    '''add one download count
    '''
    #print "\t>>>GET"
    result = {}
    crx = KV.get(uuid)
    if crx:
        crx['dlrank'] = int(crx['dlrank'])+1
        KV.set(uuid, crx)
        result['dc'] = crx['dlrank']
        result['success'] = 1
    else:
        result['msg'] = "%s NOT exist!"
        result['success'] = 0
    result['method'] = "GET"
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Headers', 'x-requested-with')
    response.set_header('Content-Type','application/json; charset=utf-8')
    return result
    #return "callback($scope,['%s','%s'])"%('GET',AJS)


@APP.route('/dc/dlrank/<order>', method='GET')
def dlrank(order):
    '''return all UUID by dlrank from memcache!
        - ASC   ~ ascend
        - DESC  ~ descend
    '''
    result = {}
    k4crx, crcrxs = INIobjSYS('crx')
    #print crcrxs
    crtdl = {}
    mc = pylibmc.Client()
    if "ASC" == order:
        result['dlorder'] = mc.get("ASCdlorder")
    else:
        result['dlorder'] = mc.get("DESCdlorder")
    #print mc.get("ASCdlorder")
    #print mc.get("DESCdlorder")
    result['success'] = 1
    result['method'] = "GET"
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Headers', 'x-requested-with')
    response.set_header('Content-Type','application/json; charset=utf-8')
    return result
    #return "callback($scope,['%s','%s'])"%('GET',AJS)
    
@APP.route('/cron/dlrank', method='GET')
def cron4dlrank():
    '''return all UUID by dlrank 
        - ASC   ~ ascend
        - DESC  ~ descend
    '''
    k4crx, crcrxs = INIobjSYS('crx')
    crtdl = {}
    for k in crcrxs:
        crtdl[k] = int(KV.get(k)['dlrank'])
    mc = pylibmc.Client()
    mc.set("ASCdlorder", pep265sd(crtdl,doreverse = False))
    mc.set("DESCdlorder", pep265sd(crtdl,doreverse = True))
    print "CRONed for dlrank update Memcache<<<"
    #print "ASCdlorder cronED::", mc.get("ASCdlorder")
    #print "DESCdlorder cronED::", mc.get("DESCdlorder")


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
#各种 命令行工具的响应支持!

@APP.route('/cli/<actype>/<usract>/<APPKEY>/<tstamp>/<ssing>')
def apicliusr(actype, usract, APPKEY, tstamp, ssing):
    args = "%s"% usract
    args += "/%s"% CFG.APPKEY       #"appkey=" + 
    args += "/%d"% time.time()      #"&timestamp=" + 
    sign_base_string = "%s/%s"% (CFG.APITYPE, args)
    #resign = __genRESTsign(sign_base_string)
    result = {}
    if ssing == __genRESTsign(sign_base_string):
        result['success'] = 1
        if "usr" == actype[:3]:
            #print "USR matters"
            uname, passwd, level = usract.split(":")
            #print uname, passwd, level
            suname = sha256_uhex(uname)
            spasswd = sha256_uhex(passwd)
            usrid = "%s%s"% (CFG.PREUID, suname)
            print usrid
            if KV.get(usrid):
                if "usradd" == actype:
                    if KV.get(usrid):
                        result['msg'] = CFG.MSG4PW['mod']
                        _usrset(usract)
                    else:
                        result['msg'] = CFG.MSG4PW['add']
                        _usradd(usract)

                elif "usrdel" == actype:
                    result['msg'] = CFG.MSG4PW['del']
                    usr =  KV.get(usrid)
                    usr['isdel'] = 1
                    KV.set(usrid, usr)
                elif "usrmod" == actype:
                    result['msg'] = CFG.MSG4PW['mod']
                    _usrset(usract)
                elif "usrchk" == actype:
                    result['msg'] = CFG.MSG4PW['chk']
                    result['data'] = _usrchk()
            else:
                #print actype
                result['msg'] = CFG.MSG4PW['add']
                _usradd(usract)


            '''
            objUSR = {'id':None # "usr:"+unicode(sha256(用户名).hexdigest())
                ,'crxs':[]
                ,'name':""
                ,'passwd':""    # unicode(sha256(口令).hexdigest())
                ,'isdel':0      # 是否删除
                ,'level':0      # 0|1 管理|团队
            }
            '''
        elif "crx" == actype[:3]:
            #print "CRX matters"
            uuid, attribute, value = usract.split(":")
            print uuid, attribute, value

            if "crxmod" == actype:
                try:
                    result['msg'] = CFG.MSG4CRX['mod']
                    crx = KV.get(uuid)
                    print crx[attribute]
                    crx[attribute] = value
                    KV.set(uuid, crx)
                    result['data'] = [uuid,attribute,value]
                except:
                    result['msg'] = ">>>%s apicliusr \n\t%s"% (CFG.MSG4CRX['err']
                        ,traceback.print_exc())
                    print ">>>apicliusr \n\t", traceback.print_exc()
            elif "crxchk" == actype:
                result['msg'] = CFG.MSG4CRX['chk']

                k4crx, crcrxs = INIobjSYS('crx')
                k4try, crtrys = INIobjSYS('try')
                k4out, crouts = INIobjSYS('out')
                k4bak, crbaks = INIobjSYS('bak')
                k4arc, crarch = INIobjSYS('arch')
                xinfo = {}
                xinfo['pub'] = {'sum':len(crcrxs)
                    ,'crx':_xinfo(crcrxs)
                    }
                xinfo['try'] = {'sum':len(crtrys)
                    ,'crx':_xinfo(crtrys)
                    }
                xinfo['out'] = {'sum':len(crouts)
                    ,'crx':_xinfo(crouts)
                    }
                xinfo['bak'] = {'sum':len(crbaks)
                    ,'crx':_xinfo(crbaks)
                    }
                xinfo['arch'] = {'sum':len(crarch)
                    ,'crx':_xinfo(crarch)
                    }

                result['data'] = xinfo
                #pp.pprint(result)
            elif "crxinfo" == actype:
                result['msg'] = CFG.MSG4CRX['info']
                crx = KV.get(uuid)
                result['data'] = _json(crx)

    else:
        result['success'] = 0
        result['errno'] = -2
    #pp.pprint(result)
    return result
    #return template('api.tpl')
    #redirect('/api/%s/sysincr'% 123)


#api/cli/ADD/up/up/5t4r3e2w1q/1345544583/a7a9cbd1c9e32dd40d7276780a692d19
def _usradd(usract):
    uname, passwd, level = usract.split(":")
    suname = sha256_uhex(uname)
    spasswd = sha256_uhex(passwd)
    usrid = "%s%s"% (CFG.PREUID, suname)
    
    usr =  deepcopy(CFG.objUSR)
    usr['id'] = usrid
    usr['name'] = uname
    usr['passwd'] = spasswd
    usr['level'] = level
    KV.set(usrid, usr)
    
    k4usrs, crtusrs = INIobjSYS('usr')
    crtusrs.append(usrid)
    #print crtusrs
    KV.set(k4usrs, crtusrs)
    
def _usrset(usract):
    uname, passwd, level = usract.split(":")
    suname = sha256_uhex(uname)
    spasswd = sha256_uhex(passwd)
    usrid = "%s%s"% (CFG.PREUID, suname)
    
    usr =  KV.get(usrid)
    usr['passwd'] = spasswd
    usr['level'] = level
    KV.set(usrid, usr)

def _usrchk():
    '''chk and export all SYS:user
    '''
    k4usrs, crtusrs = INIobjSYS('usr')
    return crtusrs
def _xinfo(crxs):
    info = []
    for uuid in crxs:
        crx = KV.get(uuid)
        info.append([uuid
            , crx['name']
            , crx['version']
            , crx['dlrank']
            ])
    return info
def _json(crx):
    info = {}
    for k in crx.keys():
        if crx[k]:
            info[k] = crx[k]
        else:
            info[k] = "None"
    return info

'''如果 API 调用成功:
    {"success": 1, "data": $data, "msg": $msg}
    调用失败,返回一个 json 字符串:
    {"success": 0, "errno": $errno, "msg": $msg}
$errno 	$msg 	说明
-1 	AppKeyError 	应用的key不存在或者key已经失效
-2 	SignError 	无效的签名
-3 	$server_timestamp 	无效的时间戳。$server_timestamp是服务器当前的时间戳
-4 	CountLimit 	超过当天查询次数限制
-5 	SpeedLimit 	查询过于频繁
-6 	ArgFormatError 查询参数格式错误，例如某些API我们要求对参数进行base64编码，如果base64编码错误，服务器将返回此错误提示
-7 	$arg 	缺少必需的查询参数。$arg说明所缺少的具体参数名
-8 	ServerBusyError 	服务器繁忙
-9 	ConflictStamp 	重复的时间戳
'''
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
    




