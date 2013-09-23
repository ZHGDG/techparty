# -*- coding: utf-8 -*-
import time
from datetime import datetime
import traceback
import hashlib
from copy import deepcopy
import xml.etree.ElementTree as etree

#import sae
#import sae.storage
#import sae.kvdb

#from wechat.official import WxNewsResponse
#from wechat.official import WxTextResponse

from bottle import *
from bottle import __version__ as bottleVer
from bottle import jinja2_template as template

#from auth import auth_required, sha256_uhex
#from lb4crx2cli import __genRESTsign

from utility import INCR4KV as __incr
from utility import TSTAMP, GENID
#from utility import POP4KV, POP4LIST, INS2LIST, INS2DICT4LIST, IDX4LIST
#from utility import ST4CRX, KV4CRX, KV4GRP
#from utility import INIobjSYS, PUTHIS, PUT2SS, PUT_PIC4CRX
from config import CFG

debug(True)
APP = Bottle()

KV = CFG.KV #sae.kvdb.KVClient(debug=1)
#SG = sae.storage.Client()

@APP.get('/echo')
@APP.get('/echo/')
def echo_wechat():
    print request.query.keys()
    print request.query.echostr
    #print request.query_string
    #print dir(BaseRequest.query_string)
    return request.query.echostr
def __echo_txt(fromUsr, toUsr, text):
    tStamp = TSTAMP()
    fromUser = fromUsr
    toUser = toUsr
    content = text
    print CFG.TPL_TEXT% locals()
    return CFG.TPL_TEXT% locals()

@APP.post('/echo')
@APP.post('/echo/')
def wechat_post():
    #print request.forms.keys()[0]
    xml = etree.XML(request.forms.keys()[0])
    fromUser = xml.findtext("ToUserName")
    toUser = xml.findtext("FromUserName")
    sha1_name = hashlib.sha1(toUser).hexdigest()
    pre_uuid = "u:%s"% sha1_name
    __MsgType = xml.findtext("MsgType")
    
    Content = xml.findtext("Content")#.encode('utf8')
    if isinstance(Content, unicode):
        print "可能是中文"
        #__Content = Content.encode('utf-8')
    else:
        __Content = Content
        print __Content #.encode('utf8')

        if "text" == __MsgType:
            #print CFG.CMD_ALIAS['help']
            if __Content in CFG.CMD_ALIAS['help'] :

                return __echo_txt(fromUser, toUser, CFG.TXT_HELP)

                return None
            elif __Content in CFG.CMD_ALIAS['version']:
                return __echo_txt(fromUser, toUser, CFG.VERSION)

                return None
            elif __Content in CFG.CMD_ALIAS['info']:
                usrs = [(u[0], u[1]) for u in KV.get_by_prefix(pre_uuid)]
                print usrs
                print "CFG.TOT ", CFG.TOT
                if 0 == len(usrs):
                    # 1st ping
                    print "sha1_name: ", sha1_name
                    uuid = GENID('usr', name = sha1_name)
                    new_usr = deepcopy(CFG.objUSR)
                    new_usr['his_id'] = GENID('his')
                    new_usr['pp'] = toUser
                    new_usr['lasttm'] = time.time()
                    print uuid, new_usr
                    KV.add(uuid, new_usr)
                    return __echo_txt(fromUser, toUser, CFG.TXT_NEW_USR)
                else:
                    # had reg.
                    member = usrs[0][1]
                    if "" == member['em']:
                        return __echo_txt(fromUser, toUser, CFG.TXT_PLS_EM)
                    else:
                        return __echo_txt(fromUser, toUser, CFG.TXT_CRT_EM% member['em'])


                return None

                '''Traceback (most recent call last):
                  File "/data1/www/htdocs/466/weknow/2/bottle.py", line 764, in _handle
                    return route.call(**args)
                  File "/data1/www/htdocs/466/weknow/2/bottle.py", line 1575, in wrapper
                    rv = callback(*a, **ka)
                  File "/data1/www/htdocs/466/weknow/2/web/mana4api.py", line 68, in wechat_post
                    if 0 == len(usr):
                TypeError: object of type 'generator' has no len() yq34 
                '''
                '''
                objUSR={"uuid":""            
                    , "his_id":""   # 更新戮
                    , "del":0
                    , "fsm":""      # 有限状态机 当前状态
                    , "acl":1       # ban:0 usr:1 staff:10 api:42 admin:100
                    , "desc":""     # 解释
                    , "pp":''       # Passport 
                    , "nm":""       # NickName "Zoom.Quiet"
                    , 'em':''       #'zhouqi@ijinshan.com',
                    , "lasttm": ''  #"2013-07-05 19:01:33",
                    }    
                '''


            elif "em" in __Content.split(":"):
                em = __Content[3:]
                print em
                if " " in em:
                    print "canceled +"
                    em = "+".join(em.split())
                #return None
                usrs = [(u[0], u[1]) for u in KV.get_by_prefix(pre_uuid)]
                member = usrs[0][1] 
                member['em'] = em
                KV.replace(usrs[0][0] , member)
                print KV.get(usrs[0][0])

                return __echo_txt(fromUser, toUser, CFG.TXT_CRT_EM% em)

                return None


            elif __Content in CFG.CMD_ALIAS['search']:
                item_count = 1
                title = "是也乎"
                description = "G术图书:5 超级聊天术"
                picurl = "http://mmsns.qpic.cn/mmsns/LkTfzZ1ialTo0ibaAicYJwQkqXyEJXEdhnhpZOD2PlnX69w3ESxibQ3vfw/0"
                url = "http://mp.weixin.qq.com/mp/appmsg/show?__biz=MjM5Mjk3MDI2MA==&appmsgid=10000132&itemidx=1&sign=dcb49b00b0773aee85c67810385a1b19#wechat_redirect"
                items = CFG.TPL_ITEM% locals()
                print CFG.TPL_URIS% locals()
                return CFG.TPL_URIS% locals()


                return None
            elif __Content in CFG.CMD_ALIAS['sayeahoo']:
                print KV.get_info()
                return __echo_txt(fromUser, toUser, KV.get_info())


                #return None


            else:
                pass
                #return __echo_txt(fromUser, toUser, CFG.TXT_WELCOME)

                return None
        
    







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
    




