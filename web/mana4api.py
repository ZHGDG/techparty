# -*- coding: utf-8 -*-
import sys   
#sys.path.append("..")  
import time
from datetime import datetime
import traceback
import hashlib
from copy import deepcopy
import xml.etree.ElementTree as etree

#import sae
#import sae.storage
#import sae.kvdb
import pyfsm
from pyfsm import state, transition

#from wechat.official import WxNewsResponse
#from wechat.official import WxTextResponse

from bottle import *
from bottle import __version__ as bottleVer
from bottle import jinja2_template as template

from auth import _query2dict, _chkQueryArgs
#from lb4crx2cli import __genRESTsign

from utility import INCR4KV as __incr
from utility import TSTAMP, GENID, USRID
from utility import ADD4SYS


#print sys.path
from config import CFG
from xsettings import XCFG
KV = CFG.KV #sae.kvdb.KVClient(debug=1)
#SG = sae.storage.Client()
debug(True)

APP = Bottle()

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
    __MsgType = xml.findtext("MsgType")
    __Content = xml.findtext("Content") #.encode('utf8')
    fromUser = xml.findtext("ToUserName")
    toUser = xml.findtext("FromUserName")
    G_CRT_USR = __chkRegUsr(toUser)
    G_CRT_USR['msg'] = __Content
    G_CRT_USR['fromUser'] = fromUser
    G_CRT_USR['toUser'] = toUser
    # usage pyfsm as FSM echo all kinds of usr ask
    weknow = pyfsm.Registry.get_task('weknow')
    if G_CRT_USR['fsm']:
        weknow.start2(G_CRT_USR['fsm'], G_CRT_USR)
        __update_usr(G_CRT_USR)
    else:
        weknow.start2('setup', G_CRT_USR)
        G_CRT_USR['fsm'] = "setup"
        __update_usr(G_CRT_USR)
    weknow.send2(__Content, G_CRT_USR)
    return None
    
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
                if "" == crt_usr['em']:
                    # 1st ping
                    return __echo_txt(fromUser, toUser, CFG.TXT_NEW_USR)
                else:
                    # had reg.
                    return __echo_txt(fromUser, toUser, CFG.TXT_CRT_EM% crt_usr['em'])


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
                crt_usr['em'] = em
                KV.replace(usrs[0][0] , crt_usr)
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
                return __echo_txt(fromUser, toUser, CFG.TXT_WELCOME)

                return None
        
    







@state('weknow')
@transition('e', 'events')
@transition('E', 'events')
@transition('re', 'reg_event')
@transition('rc', 'reg_cancel')
@transition('ri', 'reg_info')
@transition('i', 'info_me')
@transition('I', 'info_me')
@transition('me', 'info_me')
@transition('ei', 'edit_info')
@transition('s', 'seek')
@transition('S', 'seek')
#@transition('dm', 'dm_addr')
#@transition('DM', 'dm_addr')
@transition('h', 'helpme')
@transition('?', 'helpme')
@transition('help', 'helpme')
@transition('V', 'version')
@transition('v', 'version')
@transition('version', 'version')
@transition('log', 'version')
@transition('st', 'status')
@transition('stat', 'status')
def setup(self, crt_usr):
    print 'setup->{h V e re rc ir i ei s}|大妈信息'
    print crt_usr['msg']
    if 8 > len(crt_usr['msg']):
        print "try march dama"
        for DM in CFG.DM_ALIAS.keys():
            #print DM
            if crt_usr['msg'] in CFG.DM_ALIAS[DM]:
                print "found DM!", CFG.DM_ALIAS[DM][-1]


            
                



@state('weknow')
def end(self, crt_usr):
    crt_usr['fsm'] = "setup"
    __update_usr(crt_usr)
    print '...->end'


@state('weknow')
@transition('end', 'end')
def dm_addr(self, crt_usr):
    print 'setup->dm_addr->end'



    
@state('weknow')
@transition('end', 'end')
def info_me(self, crt_usr):
    print 'setup->info_me->end'
    print crt_usr['fsm']
    crt_usr['fsm'] = "setup"
    __update_usr(crt_usr)
    if "" == crt_usr['em']:
        # not set info. yet
        return __echo_txt(crt_usr['fromUser']
            , crt_usr['toUser']
            , CFG.TXT_NO_INIT
            )
    else:
        return __echo_txt(crt_usr['fromUser']
            , crt_usr['toUser']
            , CFG.TXT_CRT_ME% (crt_usr['nm'].encode('utf-8'), crt_usr['em'])
            )

@state('weknow')
@transition('*', 'end')
@transition('ia', 'info_alias')
def edit_info(self, crt_usr):
    print "edit_info::",crt_usr['msg']
    print 'setup->edit_info->info_alias 提醒输入妮称'
    crt_usr['fsm'] = "info_alias"
    __update_usr(crt_usr)
    return __echo_txt(crt_usr['fromUser']
        , crt_usr['toUser']
        , CFG.TXT_PLS_ALIAS
        )
'''    if isinstance(crt_usr['msg'], unicode):
        print "可能是中文"
        crt_usr['fsm'] = "edit_info"
        return __echo_txt(crt_usr['fromUser']
            , crt_usr['toUser']
            , CFG.TXT_PLS_EN4NM
            )
    else:
'''    
@state('weknow')
@transition('*', 'end')
@transition('im', 'info_mail')
def info_alias(self, crt_usr):
    print "info_alias::", crt_usr['msg']
    print 'setup->edit_info->info_alias->info_mail 提醒输入邮箱'
    crt_usr['fsm'] = "info_mail"
    crt_usr['nm'] = crt_usr['msg']
    __update_usr(crt_usr)
    return __echo_txt(crt_usr['fromUser']
        , crt_usr['toUser']
        , CFG.TXT_PLS_EM
        )

@state('weknow')
@transition('*', 'end')
@transition('end', 'end')
def info_mail(self, crt_usr):
    print "info_mail::", crt_usr['msg']
    if "@" in crt_usr['msg']:
        crt_usr['em'] = crt_usr['msg']
        crt_usr['fsm'] = "setup"
        __update_usr(crt_usr)
        return __echo_txt(crt_usr['fromUser']
            , crt_usr['toUser']
            , CFG.TXT_DONE_EI% (crt_usr['nm'].encode('utf-8'), crt_usr['em'])
            )
    else:
        crt_usr['fsm'] = "info_mail"
        __update_usr(crt_usr)
        return __echo_txt(crt_usr['fromUser']
            , crt_usr['toUser']
            , CFG.TXT_REALY_EM
            )
    print 'setup->edit_info->info_alias->info_mail->end 回报收集的'


@state('weknow')
@transition('end', 'end')
def events(self, crt_usr):
    print 'setup->events->end'
    


@state('weknow')
@transition('end', 'end')
def reg_event(self, crt_usr):
    print 'setup->reg_event->end'

@state('weknow')
@transition('end', 'end')
def reg_cancel(self, crt_usr):
    print 'setup->reg_cancel->end'

@state('weknow')
@transition('end', 'end')
def reg_info(self, crt_usr):
    print 'setup->info_reg->end'

@state('weknow')
@transition('end', 'end')
def helpme(self, crt_usr):
    print 'setup->helpme->end'
    return __echo_txt(crt_usr['fromUser']
        , crt_usr['toUser']
        , CFG.TXT_HELP
        )

@state('weknow')
@transition('end', 'end')
def version(self, crt_usr):
    print 'setup->version->end'
    return __echo_txt(crt_usr['fromUser']
        , crt_usr['toUser']
        , KV.get_info()
        )

@state('weknow')
@transition('end', 'end')
def status(self, crt_usr):
    print 'setup->status->end'
    return __echo_txt(crt_usr['fromUser']
        , crt_usr['toUser']
        , KV.get_info()
        )

@state('weknow')
@transition('gb', 'gbook')
@transition('dd', 'dcode')
@transition('gt', 'gtime')
@transition('dm', 'dama')
@transition('ot', 'others')
def seek(self, crt_usr):
    print "G_CRT_USR", crt_usr
    crt_usr['fsm'] = "seek"
    __update_usr(crt_usr)
    print 'setup->seek->{gb dd gt dm ot}'

@state('weknow')
@transition('no', 'no_paper')
@transition('*', 'end')
def gbook(self, crt_usr):
    print 'setup->seek->gb->no'
    crt_usr['fsm'] = "no_paper"
    __update_usr(crt_usr)

@state('weknow')
@transition('no', 'no_paper')
@transition('*', 'end')
def dcode(self, crt_usr):
    print 'setup->seek->dd->no'
    crt_usr['fsm'] = "no_paper"
    __update_usr(crt_usr)

@state('weknow')
@transition('no', 'no_paper')
@transition('*', 'end')
def gtime(self, crt_usr):
    print 'setup->seek->gt->no'
    crt_usr['fsm'] = "no_paper"
    __update_usr(crt_usr)

@state('weknow')
@transition('no', 'no_paper')
@transition('*', 'end')
def dama(self, crt_usr):
    print 'setup->seek->dm->no'
    crt_usr['fsm'] = "no_paper"
    __update_usr(crt_usr)

@state('weknow')
@transition('no', 'no_paper')
@transition('*', 'end')
def others(self, crt_usr):
    print 'setup->seek->ot->no'
    crt_usr['fsm'] = "no_paper"
    __update_usr(crt_usr)
    
@state('weknow')
@transition('end', 'end')
@transition('*', 'end')
def no_paper(self, crt_usr):
    print 'setup->seek->...->no->end'
    print crt_usr['msg']
    if crt_usr['msg'].isdigit():
        print "exp URI xml..."
        crt_usr['fsm'] = "setup"
        __update_usr(crt_usr)
    else:
        crt_usr['fsm'] = "no_paper"
        __update_usr(crt_usr)
        return __echo_txt(crt_usr['fromUser']
            , crt_usr['toUser']
            , CFG.TXT_PLS_INT
            )
def __chkRegUsr(openid):
    '''chk or init. webchat usr.:
        - gen KV uuid, try get
        - if no-exited, init. fsm
    '''
    sha1_name = hashlib.sha1(openid).hexdigest()
    uuid = USRID(sha1_name)
    usr = KV.get(uuid)
    if usr:
        print usr
        return usr
    else:
        # inti.
        new_usr = deepcopy(CFG.objUSR)
        new_usr['his_id'] = GENID('his')
        new_usr['pp'] = openid
        new_usr['lasttm'] = time.time()
        new_usr['fsm'] = None
        KV.add(uuid, new_usr)
        ADD4SYS('member', uuid)
        print new_usr
        return new_usr



        
        
def __update_usr(objUsr):
    sha1_name = hashlib.sha1(objUsr['pp']).hexdigest()
    uuid = USRID(sha1_name)
    KV.replace(uuid, objUsr)
def __echo_txt(fromUsr, toUsr, text):
    tStamp = TSTAMP()
    fromUser = fromUsr
    toUser = toUsr
    content = text
    print CFG.TPL_TEXT% locals()
    return CFG.TPL_TEXT% locals()

# echo for RESTful remote actions
'''[api]RESTful管理事务设计 on lbTC-开发协调 | Trello
	https://trello.com/c/ztdsulpM/82-api-restful
- 全部基于: `/api/cli` 前缀
    - 版本区隔为: `/api/v2/cli` 前缀
- 签名检验
- 时间检验(4.2秒以内, 并发不得超过 `N` 次)
'''

@APP.get('/cli/st/kv/<qstr>')
def st_kv(qstr):
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/st/kv", q_dict, "GET"):
        data = []
        #data.append(KV.get_info())
        return KV.get_info()
        return {'msg':"safe quary;-)"
            , 'data':data
            }
    else:
        return "alert quary!-("

# collection usr ACL matter
'''
'''
@APP.get('/cli/sum/usr/<qstr>')
def sum_usr(qstr):
    #print request.query_string #query.keys()#.appkey
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/sum/usr", q_dict, "GET"):
        data = []
        usrs = KV.get(CFG.K4D['member'])
        print usrs
        for u in usrs[:3]:
            data.append(KV.get(u))
    
        return {'msg':"safe quary;-)"
            , 'data':data
            , 'count': len(usrs)
            }
    else:
        return "alert quary!-("

@APP.put('/cli/acl/usr/<uuid>')
def put_usr_acl(uuid):
    q_dict = request.forms
    #print q_dict
    if _chkQueryArgs("/cli/acl/usr/%s"% uuid, q_dict, "PUT"):
        if 'set' in q_dict.keys():
            q_acl = base64.urlsafe_b64decode(q_dict['set'])
            if q_acl in CFG.ACL_USR.keys():
                print q_acl, CFG.ACL_USR[q_acl]
                data = {}
                his_id = HISIT('usr', uuid, "U")
                print CFG.USR.update({'uuid':uuid}
                    ,{"$set": {"acl": CFG.ACL_USR[q_acl]
                        , 'his_id':his_id
                        }
                    })
                data['hisid'] = his_id
                data['setACL'] = CFG.ACL_USR[q_acl]
                
                #print dump, "\n\t", len(dump)
                #print marshal.loads(dump)
            else:
                return {'alert':'bad acl alias!-( MUST:[ban|usr|api|admin]'}

            return {'msg':"safe quary;-)"
                , 'data': data
                }
        else:
            return {'alert':"lost set=XXX !-("}
    else:
        return "alert quary!-("

@APP.put('/cli/reliv/usr/<uuid>')
def put_usr_reliv(uuid):
    q_dict = request.forms
    #print q_dict
    if _chkQueryArgs("/cli/reliv/usr/%s"% uuid, q_dict, "PUT"):
        if 'set' in q_dict.keys():
            data = {}
            his_id = HISIT('usr', uuid, "U")
            print CFG.USR.update({'uuid':uuid}
                ,{"$set": {"del": 0
                    , 'his_id':his_id
                    }
                })
            data['hisid'] = his_id
            data['means'] = "usr reliving now"
            return {'msg':"safe quary;-)"
                , 'data': data
                }
        else:
            return {'alert':"lost set=XXX !-("}
    else:
        return "alert quary!-("



@APP.delete('/cli/del/usr/<uuid>/<qstr>')
def del_usr(uuid, qstr):
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/del/usr/%s"% uuid, q_dict, "DELETE"):
        data = {}
        his_id = HISIT('usr', uuid, "D")
        print CFG.USR.update({'uuid':uuid}
            ,{"$set": {"del": 1
                , 'his_id':his_id
                }
            })
        data['hisid'] = his_id
        data['means'] = "usr DELETE now!"
        return {'msg':"safe quary;-)"
            , 'data': data
            }
    else:
        return "alert quary!-("





@APP.get('/cli/info/usr/<uuid>/<qstr>')
def get_usr_info(uuid, qstr):
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/info/usr/%s"% uuid, q_dict, "GET"):
        return {'msg':"safe quary;-)"
            , 'data':CFG.USR.find_one({'uuid': uuid}, {'_id':0})
            }
    else:
        return "alert quary!-("

@APP.get('/cli/list/usr/<acl>/<qstr>')
def q_usr_acl(acl, qstr):
    '''ACL_USR={'ban':0,'usr':1,'api':42,'admin':100}
    '''
    print acl
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/list/usr/%s"% acl, q_dict, "GET"):
        data = []
        for u in CFG.USR.find({'acl':acl}
            , {'_id':0, 'pp':1, 'nm':1, 'acl':1, 'uuid':1}
            , limit=5).sort("uuid"):
            data.append(u)
            
        return {'msg':"safe quary;-)"
            , 'data':data
            , 'count': CFG.USR.find({'acl':acl}).count()
            }
    else:
        return "alert quary!-("

@APP.get('/cli/find/usr/<kword>/<qstr>')
def find_usr_kword(kword, qstr):
    #print request.query_string #query.keys()#.appkey
    q_dict = _query2dict(qstr)
    pattern = re.compile(".*%s.*"% kword)
    if _chkQueryArgs("/cli/find/usr/%s"% kword, q_dict, "GET"):
        data = []
        for u in CFG.USR.find({"$or":[{'nm':pattern}
                , {'em':pattern}
                , {'acc':pattern}
                , {'uuid':pattern}
                ]}
            , {'_id':0, 'pp':1, 'nm':1, 'acl':1, 'uuid':1}
            , limit=5):
            data.append(u)
            
        return {'msg':"safe quary;-)"
            , 'data':data
            , 'count': CFG.USR.find({"$or":[{'nm':pattern}
                , {'em':pattern}
                , {'mb':pattern}
                , {'uuid':pattern}
                ]}).count()
            }
    else:
        return "alert quary!-("

# collection usr ACL matter
'''

  统计节点(任意)修订次数
    sum/his
  检阅最后一次节点(任意)修订
    his/last

'''
@APP.get('/cli/sum/his/<qstr>')
def sum_tag(qstr):
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/sum/his", q_dict, "GET"):
        data = []
        for u in CFG.HIS.find({}
            , {'_id':0, 'usrid':1, 'hisobj':1, 'uuid':1, 'actype':1}
            , limit=2):
            data.append(u)
        return {'msg':"safe quary;-)"
            , 'data':data
            , 'count': CFG.HIS.find({}).count()
            }
    else:
        return "alert quary!-("

@APP.get('/cli/his/last/<qstr>')
def sum_tag(qstr):
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/his/last", q_dict, "GET"):
        #data = []
        q_mongo = CFG.HIS.find({},{'_id':0},limit=1).sort("uuid", pymongo.DESCENDING)
        #print q_mongo[0] cPickle.loads('N.')
        return {'msg':"safe quary;-)"
            , 'data':q_mongo[0]
            , 'count': CFG.HIS.find({}).count()
            }
    else:
        return "alert quary!-("

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
    






