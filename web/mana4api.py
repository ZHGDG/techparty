# -*- coding: utf-8 -*-
import sys   
import time #import time, gmtime, strftime, localtime
from datetime import datetime
import traceback
import httplib, urllib, hashlib
import json

import base64
import cPickle
#import ConfigParser
from os.path import splitext as os_splitext
from os.path import exists as os_exists

from copy import deepcopy
import xml.etree.ElementTree as etree

import pyfsm
from pyfsm import state, transition

from wechat.official import WxApplication, WxRequest, WxTextResponse, WxNewsResponse, WxArticle

from bottle import *
from bottle import __version__ as bottleVer
#from bottle import jinja2_template as template

from auth import _query2dict, _chkQueryArgs

from utility import INCR4KV as __incr
from utility import TSTAMP, GENID, USRID, DAMAID
from utility import ADD4SYS
from utility import PUT2SS
#print sys.path
from config import CFG
from xsettings import XCFG
KV = CFG.KV #sae.kvdb.KVClient(debug=1)
BK = CFG.BK
debug(True)

APP = Bottle()

@APP.get('/echo')
@APP.get('/echo/')
def echo_wechat():
    '''wechat app token echo
    '''
    #print request.query.keys()
    #print request.query.echostr
    #print request.query_string
    #print dir(BaseRequest.query_string)
    return request.query.echostr

'''
def wechat(request):
    app = EchoApp()
    result = app.process(request.GET, request.body, token='your token')
    return HttpResponse(result)
'''

# echo for RESTful remote actions
'''[api]RESTful管理事务设计 on lbTC-开发协调 | Trello
	https://trello.com/c/ztdsulpM/82-api-restful
- 全部基于: `/api/cli` 前缀
    - 版本区隔为: `/api/v2/cli` 前缀
- 签名检验
- 时间检验(4.2秒以内, 并发不得超过 `N` 次)
query_string 
'''

@APP.get('/cli/info/<uuid>/<qstr>')
def info_kv(uuid, qstr):
    '''查询 UUID 的信息
    '''
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/info/%s"% uuid, q_dict, "GET"):
        feed_back = {'data':[]}
        print "info_kv()>>> ",uuid
        print KV.get(uuid)
        #return KV.get(uuid)
        feed_back['msg'] = "safe quary;-)"
        feed_back['data'] = KV.get(uuid)
        return feed_back
    else:
        return "alert quary!-("

@APP.get('/cli/sum/<matter>/<qstr>')
def st_kv(matter, qstr):
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/sum/%s"% matter, q_dict, "GET"):
        feed_back = {'data':[]}
        if 'db' == matter:
            feed_back['msg'] = "all SYS_* status."
            feed_back['data'] = ["%s hold %s node info."% (k
                , len(KV.get(CFG.K4D[k] )) ) for k in CFG.K4D.keys() if "incr"!=k
                ]
        elif 'bk' == matter:
            count = 0
            for dump in BK.list():
                count += 1
                feed_back['data'].append("%s ~ %s"%(dump['name']
                    , dump['bytes']
                    ))
            feed_back['msg'] = "all Storaged %s dumps"% count
        else:
            if matter in CFG.K4D.keys():
                feed_back['msg'] = "base %s data."% CFG.K4D[matter]
                feed_back['data'] = "%s hold %s node info."% (CFG.K4D[matter]
                    , len(KV.get(CFG.K4D[matter] )) 
                    )
            else:
                feed_back['msg'] = "sum key is OUT CFG.K4D !-("
        return feed_back
        
    else:
        return "alert quary !-("

@APP.get('/cli/st/kv/<qstr>')
def st_kv(qstr):
    '''查询 KVDB 整体现状
    '''
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/st/kv", q_dict, "GET"):
        feed_back = {'data':[]}
        #data.append(KV.get_info())
        return KV.get_info()
        feed_back['msg'] = "safe quary;-)"
        feed_back['data'] = KV.get_info()
        return feed_back
    else:
        return "alert quary!-("

# collection KVDB mana. matters
'''
'''
@APP.post('/cli/bk/<matter>')
def bkup_dump(matter):
    q_dict = request.forms
    if _chkQueryArgs("/cli/bk/%s"% matter, q_dict, "PUT"):
        feed_back = {'data':[]}
        if 'db' ==  matter:
            print "try dumps all nodes from KVDB"
            kb_objs = {}
            total = 0
            for k in CFG.K4D:
                #print k
                if 'incr' == k:
                    # 只要替换一个自增值
                    #kb_objs[k] = CFG.K4D[k]
                    kb_objs[CFG.K4D[k] ] = KV.get(CFG.K4D[k])
                    total += 1
                else:
                    # 需要根据索引值列逐一提取数据
                    #kb_objs[k] = CFG.K4D[k]
                    kb_objs[CFG.K4D[k] ] = KV.get(CFG.K4D[k])
                    total += 1
                    if 0 != len(kb_objs[CFG.K4D[k] ] ):
                        for k4v in kb_objs[CFG.K4D[k] ]:
                            crt_v = KV.get(k4v)
                            if None != crt_v:
                                kb_objs[k4v] = crt_v
                                total += 1
            dumps = cPickle.dumps(kb_objs)
            feed_back['data'].append("%s pointed %s nodes"%(CFG.K4D, total) )

            #print kb_objs

            msg = "bkup KVDB dumped"
        else:
            kb_objs = {}
            kb_objs[CFG.K4D[matter] ] = KV.get(CFG.K4D[matter])
            if 0 != len(kb_objs[CFG.K4D[matter] ] ):
                for k in kb_objs[CFG.K4D[matter] ]:
                    kb_objs[k] = KV.get(k)
            dumps = cPickle.dumps(kb_objs)
            feed_back['data'].append("%s pointed %s nodes"%(CFG.K4D[matter] 
                , len(kb_objs[CFG.K4D[matter] ] )))
            #print kb_objs
            msg = "bkup %s dumped"% CFG.K4D[matter]
        
        sid, uri = PUT2SS(dumps, name=matter)
        feed_back['data'].append( BK.stat_object(sid) )
        feed_back['msg'] = msg
        feed_back['uri'] = uri
        #data.append(KV.get_info())
        return feed_back
    else:
        return "alert quary!-("

@APP.put('/cli/revert/<matter>')
def revert_dump(matter):
    q_dict = request.forms
    if _chkQueryArgs("/cli/revert/%s"% matter, q_dict, "PUT"):
        feed_back = {'data':[]}
        set_key = list(set(q_dict.keys())-set(CFG.SECURE_ARGS))[0]
        set_var = base64.urlsafe_b64decode(request.forms[set_key])
        #print set_key, set_var
        if 'db' ==  matter:
            print "try revert ALL date from KVDB"
            dumps = BK.get_object_contents(set_var)
            re_obj = cPickle.loads(dumps)
            feed_back['msg'] = "reverted %s nodes for whole KVDB "% len(re_obj.keys())
            _INX_KEYS = [CFG.K4D[k] for k in CFG.K4D.keys()]
            # replace global idx K/V, maybe make ghost K/V
            _his = set()#KV.get(CFG.K4D['his'])            
            for k in re_obj.keys():
                if k in _INX_KEYS:
                    # 索引键处理
                    if 'SYS_TOT' == k:
                        # 只要替换一个自增值
                        KV.set(k, re_obj[k])
                        _his.add(k)
                    elif 'SYS_pubs_HIS' == k:
                        # 统一增替
                        _his.add(k)
                    else:
                        print "revert ->", k 
                        #print _his
                        #print type(re_obj[k])
                        _his.add(k)
                        _his.update(set(re_obj[k]))
                        print "_his ", len(_his)
                        #KV.set(CFG.K4D['his'], KV.get(CFG.K4D['his']).update(set(re_obj[k])) )
                else:
                    # 数据键恢复
                    #print k, re_obj[k]
                    if None == KV.get(k):
                        KV.add(k, re_obj[k])
                    else:
                        KV.replace(k, re_obj[k])
            KV.set(CFG.K4D['his'], list(_his) )
            #print KV.get(CFG.K4D['his'])



        else:
            dumps = BK.get_object_contents(set_var)
            re_obj = cPickle.loads(dumps)
            feed_back['msg'] = "reverted %s nodes as %s "% (len(re_obj[CFG.K4D[matter]])
                , CFG.K4D[matter]
                )
            # replace global idx K/V, maybe make ghost K/V
            _his = KV.get(CFG.K4D['his'])
            _his.append(re_obj[CFG.K4D[matter]] )
            _his = list(set(CFG.K4D['his']) )
            KV.set(CFG.K4D['his'], _his)

            uuids = re_obj[CFG.K4D[matter]]
            KV.replace(CFG.K4D[matter], uuids)
            for uuid in uuids:
                #print uuid, re_obj[uuid]
                if None == KV.get(uuid):
                    KV.add(uuid, re_obj[uuid])
                else:
                    KV.replace(uuid, re_obj[uuid])





                    
        feed_back['data'].append( BK.stat_object(set_var) )
        #data.append(KV.get_info())
        return feed_back
    else:
        return "alert quary!-("

@APP.put('/cli/resolve/<matter>')
def resolve_his(matter):
    q_dict = request.forms
    if _chkQueryArgs("/cli/resolve/%s"% matter, q_dict, "PUT"):
        feed_back = {'data':[]}
        set_key = list(set(q_dict.keys())-set(CFG.SECURE_ARGS))[0]
        set_var = base64.urlsafe_b64decode(request.forms[set_key])
        print "resolve_his()  ", set_key, set_var
        if 'his' ==  matter:
            print "try resolve_his ALL from KVDB"
            _INX_KEYS = [CFG.K4D[k] for k in CFG.K4D.keys()]
            _his = set() #KV.get(CFG.K4D['his'])  
            feed_back['msg'] = []
            #print _INX_KEYS, type(_INX_KEYS)
            for k in _INX_KEYS:
                # 索引键处理
                print k
                if 'SYS_TOT' == k:
                    _his.add(k)
                elif 'SYS_pubs_HIS' == k:
                    # 统一合并
                    _his.add(k)
                else:
                    _idx = KV.get(k)
                    print "revert -> %s <- %s nodes"% (k, len(_idx) ) 
                    _his.add(k)
                    _his.update(set(_idx) )
                    #KV.set(CFG.K4D['his'], KV.get(CFG.K4D['his']).update(set(re_obj[k])) )
                    feed_back['msg'].append("%s >>> %s nodes"% (k, len(_idx) ) ) 

            KV.set(CFG.K4D['his'], list(_his) )
            #print KV.get(CFG.K4D['his'])




            feed_back['data'] = "re-merged all KVDB info into %s nodes"% len(_his)
        elif 'wx' ==  matter:
            print "try rebuild Passpord->UUID"
            # 根据 K4D['m'] 的索引,建立 成员 Passpord->UUID 的索引字典
            users = KV.get(CFG.K4D['m'])
            for m in users:
                upp = KV.get(m)['pp']
                #print "%s -> %s"%(m, upp)
                ppu = KV.get(upp)
                if not ppu:
                    KV.add(upp, m)
            #KV.set(CFG.K4D['his'], list(_his) )
            #print KV.get(CFG.K4D['his'])
            feed_back['data'] = "re-point all Member key %s nodes"% len(users)





            feed_back['msg'] = "re-build Passpord->UUID" 
        #data.append(KV.get_info())
        return feed_back
    else:
        return "alert quary!-("

@APP.delete('/cli/del/bk/<uuid>/<qstr>')
def del_bk(uuid, qstr):
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/del/bk/%s"% uuid, q_dict, "DELETE"):
        feed_back = {'data':[]}
        feed_back['msg'] = "deleted: %s"% uuid
        feed_back['data'].append( BK.stat_object(uuid) )
        BK.delete_object(uuid)
        return feed_back
    else:
        return "alert quary!-("

# collection wechat papers mana. matters
'''
'''
@APP.get('/cli/sum/p/<tag>/<qstr>')
def st_p_tag(tag, qstr):
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/sum/p/%s"% tag, q_dict, "GET"):
        feed_back = {'data':[]}
        #print tag
        all_papers = KV.get(CFG.K4D['p'])
        #print type(all_papers)
        all_papers.sort()
        tmp = {}
        for puuid in KV.get(CFG.K4D['p']):
            #print puuid, " --> ", KV.get(puuid)
            if tag ==  puuid[:2]:
                p = KV.get(puuid)
                #print p
                if 0 == p['del']:
                    exp = "%s:%-28s"%(p['code'], puuid)
                    tmp[exp] = p['title']
                    feed_back['data'].append(exp) 
        feed_back['data'].sort()
        for i in range(len(feed_back['data'])):
            k = feed_back['data'][i]
            feed_back['data'][i] = "%s%s"% (k, tmp[k])
        feed_back['msg'] = "%s papers had %s ."% (tag, len(feed_back['data']))
        return feed_back
        
    else:
        return "alert quary !-("

@APP.delete('/cli/del/p/<uuid>/<qstr>')
def del_p(uuid, qstr):
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/del/p/%s"% uuid, q_dict, "DELETE"):
        feed_back = {'data':[]}
        p = KV.get(uuid)
        p['del'] = 1
        KV.replace(uuid, p)
        feed_back['data'].append("%s:%s"% (p['code'],p['title']))
        feed_back['msg'] = "deleted: %s"% uuid
        return feed_back
    else:
        return "alert quary!-("

@APP.post('/cli/push/p/<qstr>')
def push_papers(qstr):
    q_dict = _query2dict(qstr)
    q_form = request.forms
    q_file = request.files.get('json')
    #f_name, f_ext = os_splitext(q_file.filename)
    #print f_name, f_ext
    set_var = q_file.file.read()
    if _chkQueryArgs("/cli/push/p", q_dict, "POST"):
        feed_back = {'data':[]}
        #set_key = list(set(q_form.keys())-set(CFG.SECURE_ARGS))[0]
        #set_var = base64.urlsafe_b64decode(request.forms[set_key])
        j = eval(set_var) #, set_var
        p_tag = j.keys()[0]
        #print j.keys()
        #return None
        for paper in j[p_tag]:
            uuid = GENID(p_tag)
            feed_back['data'].append(uuid)
            #print uuid
            new_paper = deepcopy(CFG.K4WD)
            new_paper['uuid'] = uuid
            new_paper['his_id'] = uuid
            new_paper['lasttm'] = time.time()
            new_paper['tag'] = p_tag
            new_paper['title'] = paper['title']
            new_paper['url'] = paper['uri']
            new_paper['picurl'] = paper['picuri']
            new_paper['code'] = paper['code']
            KV.add(uuid, new_paper)
            ADD4SYS('p', uuid)
            #print uuid, new_paper

        #feed_back['data'].append( BK.stat_object(sid) )
        feed_back['msg'] = "uploaded %s papers info."% len(j[p_tag])
        #data.append(KV.get_info())
        return feed_back
    else:
        return "alert quary!-("



@APP.put('/cli/fix/p/<tag>/<uuid>')
def fix_paper(tag, uuid):
    q_dict = request.forms
    if _chkQueryArgs("/cli/fix/p/%s/%s"% (tag, uuid), q_dict, "PUT"):
        feed_back = {'data':[]}
        set_key = list(set(q_dict.keys())-set(CFG.SECURE_ARGS))[0]
        set_var = base64.urlsafe_b64decode(request.forms[set_key])
        print "\t", set_key
        print set_var
        #return None
        
        if set_key in CFG.K4WD.keys():
            print set_key, set_var
            uuid, pub = __chkPAPER(tag, uuid)
            if not uuid:
                feed_back['msg'] = "BAD tag: %s out pre-defined"% tag
            else:
                pub[set_key] = set_var.decode('utf-8')
                KV.replace(uuid, pub)
                #print pub
                feed_back['data'].append(pub)
                feed_back['uuid'] = uuid
        else:
            feed_back['msg'] = "out keys, NULL fixed!" 
            feed_back['can_fix_keys'] = CFG.K4WD.keys()
        #data.append(KV.get_info())
        return feed_back
    else:
        return "alert quary!-("




def __chkPAPER(tag, uuid):
    '''chk or init. webchat paper:
        - if uuid == null init. node
        - else try get it
    '''
    paper = KV.get(uuid)
    if paper:
        print uuid, paper
        ADD4SYS('p', uuid)  # for old sys, collected uuid into idx node!
        return uuid, paper
    else:
        # inti.
        if tag not in CFG.ESSAY_TAG.keys():
            return None, None
        uuid = GENID(tag)
        if not uuid:
            print "tag out GENID() accept area!"
            return None, None
        ADD4SYS('p', uuid)
        new_paper = deepcopy(CFG.K4WD)
        new_paper['uuid'] = uuid
        new_paper['tag'] = tag
        new_paper['his_id'] = GENID('his')
        new_paper['lasttm'] = time.time()
        new_paper['title'] = "waiting set..."
        KV.add(uuid, new_paper)
        print uuid, new_paper
        return uuid, new_paper



        
        
@APP.put('/cli/fix/e/<code>')
def fix_event(code):
    '''events info. editor
    '''
    q_dict = request.forms
    if _chkQueryArgs("/cli/fix/e/%s"% code, q_dict, "PUT"):
        feed_back = {'data':[]}
        set_key = list(set(q_dict.keys())-set(CFG.SECURE_ARGS))[0]
        set_var = base64.urlsafe_b64decode(request.forms[set_key])
        if set_key in CFG.K4DM.keys():
            print set_key, set_var
            feed_back['msg'] = "func. not working now..." 
            
        else:
            feed_back['msg'] = "out keys, NULL fixed!" 
            feed_back['can_fix_keys'] = CFG.K4DM.keys()
        #data.append(KV.get_info())
        return feed_back
    else:
        return "alert quary!-("

# collection usr ACL matter
'''
'''
@APP.get('/cli/find/m/<kword>/<qstr>')
def find_m(kword, qstr):
    #print request.query_string #query.keys()#.appkey
    q_dict = _query2dict(qstr)
    if _chkQueryArgs("/cli/find/m/%s"% kword, q_dict, "GET"):
        feed_back = {'data':[]}
        print "find_m-> ", kword
        usrs = KV.get(CFG.K4D['m'])
        #print usrs
        for u in usrs:
            m = KV.get(u)
            m_info = "%s %s %s"%(m['em'].strip()
                , m['nm'].strip()
                , m['desc'].strip()
                )
            if kword in m_info.lower():
                feed_back['data'].append(m)
    
        feed_back['msg'] = "safe quary;-)"
        return feed_back
    else:
        return "alert quary!-("

@APP.put('/cli/fix/dm/<nm>')
def fix_dm(nm):
    q_dict = request.forms
    if _chkQueryArgs("/cli/fix/dm/%s"% nm, q_dict, "PUT"):
        feed_back = {'data':[]}
        set_key = list(set(q_dict.keys())-set(CFG.SECURE_ARGS))[0]
        set_var = base64.urlsafe_b64decode(request.forms[set_key])
        if set_key in CFG.K4DM.keys():
            #print set_key, set_var
            #print "<nm>", nm
            uuid, dm = __chkDAMA(nm.strip())
            #print uuid,dm
            if uuid:
                dm[set_key] = set_var.decode('utf-8')
                KV.replace(uuid, dm)
                feed_back['data'].append(dm)
                feed_back['uuid'] = uuid
        else:
            feed_back['msg'] = "out keys, NULL fixed!" 
            feed_back['can_fix_keys'] = CFG.K4DM.keys()
        #data.append(KV.get_info())
        return feed_back
    else:
        return "alert quary!-("

@APP.put('/cli/fix/m/<uuid>')
def fix_member(uuid):
    q_dict = request.forms
    if _chkQueryArgs("/cli/fix/m/%s"% uuid, q_dict, "PUT"):
        feed_back = {'data':[]}
        set_key = list(set(q_dict.keys())-set(CFG.SECURE_ARGS))[0]
        set_var = base64.urlsafe_b64decode(request.forms[set_key])
        if set_key in CFG.K4DM.keys():
            print set_key, set_var
            feed_back['msg'] = "func. not working now..." 
            
        else:
            feed_back['msg'] = "out keys, NULL fixed!" 
            feed_back['can_fix_keys'] = CFG.K4DM.keys()
        #data.append(KV.get_info())
        return feed_back
    else:
        return "alert quary!-("

def __chkDMID(text):
    for DM in CFG.DM_ALIAS.keys():
        #print CFG.DM_ALIAS[DM]
        if text in CFG.DM_ALIAS[DM]:
            print "found DAMA!", CFG.DM_ALIAS[DM][0]
            return DM
    
    print "not march DAMA!"
    return None

def __chkDAMA(zipname):
    '''chk or init. webchat usr.:
        - gen KV uuid, try get
        - if no-exited, init. DM node
    '''
    k4dm = __chkDMID(zipname)
    if not k4dm:
        return None, None
    uuid = DAMAID(k4dm)
    ADD4SYS('dm', uuid)  # for old sys, collected uuid into idx node!
    usr = KV.get(uuid)
    if usr:
        #print uuid, usr
        return uuid, usr
    else:
        # inti.
        new_usr = deepcopy(CFG.K4DM)
        new_usr['his_id'] = GENID('his')
        new_usr['lasttm'] = time.time()
        new_usr['nm'] = CFG.DM_ALIAS[k4dm][0]
        KV.add(uuid, new_usr)
        #ADD4SYS('dm', uuid)
        #print uuid, new_usr
        return uuid, new_usr


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

@APP.post('/echo')
@APP.post('/echo/')
def wechat_post():
    #print "wechat GET\n ",request.query.keys()
    #print "wechat GET type\n ",type(request.query)
    # usage jeff SDK for wechat...
    if CFG.AS_SAE:
        wxa = WxApplication(token=XCFG.TOKEN)
        chkwx = wxa.is_valid_params(request.query)
        if not chkwx:
            return None
    else:
        print "Debugging localhost..."
    wxreq = WxRequest(request.forms.keys()[0])
    print "FromUserName->%s\nToUserName->%s"%( wxreq.FromUserName
        , wxreq.FromUserName
        )
    #print "WxTextResponse:\n", WxTextResponse("hello world", wxreq).as_xml()
    G_CRT_USR = __chkRegUsr(wxreq.FromUserName)
    wxreq.crt_usr = G_CRT_USR
    # usage pyfsm as FSM echo all kinds of usr ask
    weknow = pyfsm.Registry.get_task('weknow')
    if G_CRT_USR['fsm']:
        weknow.start2(G_CRT_USR['fsm'], wxreq)
    else:
        weknow.start2('setup', wxreq)
        G_CRT_USR['fsm'] = "setup"
        __update_usr(G_CRT_USR)
    #print "weknow.send2:\n"
    return weknow.send2(wxreq.Content.strip(), wxreq)




    return None
    '''collected old code for doc.
    '''
    # base hard code for all 
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
    print "weknow.send2:\n", weknow.send2(__Content, G_CRT_USR)
    return None
    
    # base choas if elif else
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
        







def __chkRegUsr(passport):
    '''chk or init. webchat usr.:
        - gen KV uuid, try get
        - if no-exited, init. fsm
    '''
    sha1_name = hashlib.sha1(passport).hexdigest()
    uuid = USRID(sha1_name)
    ADD4SYS('m', uuid)  # for old sys, collected uuid into idx node!
    usr = KV.get(uuid)
    # 检查反向索引键对
    ppu = KV.get(passport)
    if not ppu:
        # inti.
        KV.add(passport, uuid)
    # 检查用户键值对
    if usr:
        #print usr
        return usr
    else:
        # inti.
        new_usr = deepcopy(CFG.objUSR)
        new_usr['his_id'] = GENID('his')
        new_usr['pp'] = passport
        new_usr['lasttm'] = time.time()
        new_usr['fsm'] = None
        KV.add(uuid, new_usr)
        #ADD4SYS('m', uuid)
        #print new_usr
        return new_usr






def __update_usr(objUsr):
    sha1_name = hashlib.sha1(objUsr['pp']).hexdigest()
    uuid = USRID(sha1_name)
    KV.replace(uuid, objUsr)
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
@transition('h', 'helpme')
@transition('H', 'helpme')
@transition('?', 'helpme')
@transition('help', 'helpme')
@transition('V', 'version')
@transition('v', 'version')
@transition('version', 'version')
@transition('log', 'version')
@transition('st', 'status')
@transition('stat', 'status')
@transition('nn', 'niuniu')
def setup(self, wxreq):
    print 'setup->{h V e re rc ir i ei s}|大妈信息'
    #print crt_usr['msg']
    #print wxreq.Content
    cmd = wxreq.Content
    if cmd not in CFG.CMD_ALIAS:
        #if 8 > len(crt_usr['msg']):
        #print cmd
        if cmd.isdigit():
            pass    #忽略过程中的数字输入
        #print len(cmd)
        if 8 > len(cmd):
            print "try march dama"
            uuid, dm = __chkDAMA(cmd)
            if uuid:
                #print dm
                msg = CFG.TXT_CRT_DM% (dm['nm'], dm['desc'])
                return WxTextResponse(msg, wxreq).as_xml()
        else:
            print type(cmd.decode('utf-8'))
            #return None
            access_token = _wx_token_get()
            wx_uri = 'wx/msg'
            host = CFG.CLI_URI[wx_uri][0]
            url = CFG.CLI_URI[wx_uri][1]    #"%s=%s"% (CFG.CLI_URI[wx_uri][1], access_token)

            openid = XCFG.WX_ZQ
            content = cmd.decode('utf-8') #_msg  #u'#细思恐极....'
            cc_msg = CFG.SRV_TXT_JSON% locals()
            print cc_msg
            data = _https_post(host
                , url
                , cc_msg  #bytearray(_msg.encode('utf-8'))
                , token = access_token
                )
            print data





@state('weknow')
def end(self, wxreq):
    print '...->end'
    crt_usr = wxreq.crt_usr
    crt_usr['fsm'] = "setup"
    __update_usr(crt_usr)
    return None





@state('weknow')
@transition('gb', 'papers')
@transition('dd', 'papers')
@transition('gt', 'papers')
@transition('dm', 'papers')
@transition('hd', 'papers')
@transition('et', 'papers')
@transition('ot', 'papers')
@transition('q', 'helpme')
@transition('Q', 'helpme')
@transition('h', 'helpme')
@transition('H', 'helpme')
def seek(self, wxreq):
    print 'setup->seek->{gb dd gt dm ot q h} '
    crt_usr = wxreq.crt_usr
    #print "G_CRT_USR", crt_usr
    if wxreq.Content in CFG.PAPER_TAGS:
        crt_usr['fsm'] = "papers"
        __update_usr(crt_usr)
        return WxTextResponse(CFG.TXT_PLS_TAG, wxreq).as_xml()
    else:
        crt_usr['fsm'] = "seek"
        __update_usr(crt_usr)
        return WxTextResponse(CFG.TXT_OUT_TAG, wxreq).as_xml()


@state('weknow')
@transition('no', 'no_paper')
@transition('q', 'helpme')
@transition('Q', 'helpme')
@transition('h', 'helpme')
@transition('H', 'helpme')
def papers(self, wxreq):
    print 'setup->seek->[papers]->no'
    crt_usr = wxreq.crt_usr
    tag = wxreq.Content
    count = 0
    papers4tag = []
    if tag in CFG.ESSAY_TAG.keys():
        # right tag switch
        uuid_all_paper = KV.get(CFG.K4D['p'])
        for uuid in uuid_all_paper:
            # sometime reg. uuid as None
            if uuid and uuid[:2] == tag:
                paper =  KV.get(uuid)
                if 0 == paper['del']:
                    count += 1
                    #print paper['title']
                    #papers4tag.append((str(paper['code']),paper['title']))
                    #print paper['title']
                    #print type(paper['title'])
                    if isinstance(paper['title'], unicode):
                        #print '%s is a unicode object'%paper['title']
                        crt_title = paper['title'].encode('utf-8')
                        #print type(crt_title)
                    else:
                        #print '%s is a str object'%paper['title']
                        crt_title = paper['title']
                    papers4tag.append((int(paper['code']), crt_title))
                    #print paper['title'].enconde('utf-8')
                    #AttributeError: 'str' object has no attribute 'encode'
        #return None
        #print "count ", count
        if 0 == count:
            # not paper in the tag yet
            crt_usr['fsm'] = "setup"
            crt_usr['buffer'] = ""
            __update_usr(crt_usr)
            return WxTextResponse(CFG.TXT_PUB_WAIT, wxreq).as_xml()
        else:
            # waiting paper Number code, jump into FSM:number_paper
            #for p in papers4tag: print p
            papers4tag.sort()
            #return None
            p_list = "    ".join(["%s: %s\n"%(p[0], p[1]) for p in papers4tag])
            crt_usr['fsm'] = "number_paper"
            crt_usr['buffer'] = tag
            __update_usr(crt_usr)
            return WxTextResponse(CFG.TXT_TAG_PAPERS% (CFG.ESSAY_TAG[tag]
                , p_list.decode('utf-8')), wxreq).as_xml()
            
    else:    
        crt_usr['fsm'] = "papers"
        __update_usr(crt_usr)
        return WxTextResponse(CFG.TXT_PLS_TAG, wxreq).as_xml()

    return None
    
    crt_usr['fsm'] = "setup"
    __update_usr(crt_usr)
    return WxTextResponse(CFG.TXT_PUB_WAIT, wxreq).as_xml()


@state('weknow')
@transition('end', 'end')
@transition('q', 'helpme')
@transition('Q', 'helpme')
@transition('h', 'helpme')
@transition('H', 'helpme')
def number_paper(self, wxreq):
    print 'setup->seek->...->no->end'
    crt_usr = wxreq.crt_usr
    code = wxreq.Content
    #print code, code.isdigit()
    if code.isdigit():
        print "exp URI xml..."
        #print code
        tag = crt_usr['buffer']
        resp = None
        for puuid in KV.get(CFG.K4D['p']):
            # 根据指定的类别,逐一从文章索引中过滤出指定代号的文章
            # 要求, del==0 && code==指定数
            if tag == puuid[:2]:
                p = KV.get(puuid)
                #print p['code'], "\n\t", p
                if 0 == p['del']:
                    if int(code) == int(p['code']):
                        #print p
                        resp = WxNewsResponse([WxArticle(p['title'],
                                    Description="",
                                    Url=p['url'],
                                    PicUrl=p['picurl'])], wxreq).as_xml()
                        #return resp
                        break


        #return None
        crt_usr['fsm'] = "setup"
        __update_usr(crt_usr)
        if resp:
            return resp
        else:
            return WxTextResponse("图文消息返回异常,议案吼 大妈!", wxreq).as_xml()
    else:
        crt_usr['fsm'] = "number_paper"
        __update_usr(crt_usr)
        return WxTextResponse(CFG.TXT_PLS_INT, wxreq).as_xml()
        
        return __echo_txt(crt_usr['fromUser']
            , crt_usr['toUser']
            , CFG.TXT_PLS_INT
            )

'''
resp = WxNewsResponse([WxArticle(Title="iPhone 6 is here!",
                        Description="It is not a joke",
                        Url="http://jeffkit.info",
                        PicUrl="http://jeffkit.info/avatar.jpg")], wxreq).as_xml()
                        
'''

'''
WxNewsResponse, WxArticle
resp = WxNewsResponse([WxArticle(Title="iPhone 6 is here!",
                        Description="It is not a joke",
                        Url="http://jeffkit.info",
                        PicUrl="http://jeffkit.info/avatar.jpg")], wxreq).as_xml()
'''

    
@state('weknow')
@transition('q', 'helpme')
@transition('Q', 'helpme')
@transition('h', 'helpme')
@transition('H', 'helpme')
def info_me(self, wxreq):
    print 'setup->info_me->end'
    crt_usr = wxreq.crt_usr
    #print "wxreq.crt_usr: ", crt_usr
    #print crt_usr['fsm']
    crt_usr['fsm'] = "setup"
    __update_usr(crt_usr)
    if "" == crt_usr['em']:
        # not set info. yet
        return WxTextResponse(CFG.TXT_NO_INIT, wxreq).as_xml()
        return __echo_txt(crt_usr['fromUser']
            , crt_usr['toUser']
            , CFG.TXT_NO_INIT
            )
    else:
        msg = CFG.TXT_CRT_ME% (crt_usr['nm'], crt_usr['em'])
        return WxTextResponse(msg, wxreq).as_xml()
        return __echo_txt(crt_usr['fromUser']
            , crt_usr['toUser']
            , CFG.TXT_CRT_ME% (crt_usr['nm'].encode('utf-8'), crt_usr['em'])
            )


@state('weknow')
@transition('ia', 'info_alias')
@transition('q', 'helpme')
@transition('Q', 'helpme')
@transition('h', 'helpme')
@transition('H', 'helpme')
def edit_info(self, wxreq):
    print 'setup->edit_info->info_alias 提醒输入妮称'
    crt_usr = wxreq.crt_usr
    print "edit_info::", wxreq.Content   #crt_usr['msg']
    crt_usr['fsm'] = "info_alias"
    __update_usr(crt_usr)
    return WxTextResponse(CFG.TXT_PLS_ALIAS, wxreq).as_xml()
        
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
@transition('im', 'info_mail')
@transition('q', 'helpme')
@transition('Q', 'helpme')
@transition('h', 'helpme')
@transition('H', 'helpme')
def info_alias(self, wxreq):
    print 'setup->edit_info->info_alias->info_mail 提醒输入邮箱'
    crt_usr = wxreq.crt_usr
    crt_usr['fsm'] = "info_mail"
    crt_usr['nm'] = wxreq.Content   #crt_usr['msg']
    __update_usr(crt_usr)
    return WxTextResponse(CFG.TXT_PLS_EM, wxreq).as_xml()
    
    return __echo_txt(crt_usr['fromUser']
        , crt_usr['toUser']
        , CFG.TXT_PLS_EM
        )

@state('weknow')
@transition('q', 'helpme')
@transition('Q', 'helpme')
@transition('h', 'helpme')
@transition('H', 'helpme')
def info_mail(self, wxreq):
    print 'setup->edit_info->info_alias->info_mail->end 回报收集的'
    crt_usr = wxreq.crt_usr
    print "info_mail::", wxreq.Content  #crt_usr['msg']
    #if "@" in crt_usr['msg']:
    if "@" in wxreq.Content.strip():
        print "get user em.."
        crt_usr['em'] = "+".join(wxreq.Content.strip().split())   #crt_usr['msg']
        crt_usr['fsm'] = "setup"
        __update_usr(crt_usr)
        
        msg = CFG.TXT_DONE_EI% (crt_usr['nm'], crt_usr['em'])
        return WxTextResponse(msg, wxreq).as_xml()
    
        return __echo_txt(crt_usr['fromUser']
            , crt_usr['toUser']
            , CFG.TXT_DONE_EI% (crt_usr['nm'].encode('utf-8'), crt_usr['em'])
            )
    else:
        print "error emil format?"
        crt_usr['fsm'] = "info_mail"
        __update_usr(crt_usr)
        #print WxTextResponse(CFG.TXT_REALY_EM, wxreq).as_xml()
        return WxTextResponse(CFG.TXT_REALY_EM, wxreq).as_xml()
    
        return __echo_txt(crt_usr['fromUser']
            , crt_usr['toUser']
            , CFG.TXT_REALY_EM
            )

'''
Traceback (most recent call last):
  File "/data1/www/htdocs/466/weknow/3/bottle.py", line 764, in _handle
    return route.call(**args)
  File "/data1/www/htdocs/466/weknow/3/bottle.py", line 1575, in wrapper
    rv = callback(*a, **ka)
  File "/data1/www/htdocs/466/weknow/3/web/mana4api.py", line 76, in wechat_post
    weknow.start2(G_CRT_USR['fsm'], wxreq)
  File "/data1/www/htdocs/466/weknow/3/3party/pyfsm.py", line 284, in start2
    return self.current_state.enter2(self, obj)
  File "/data1/www/htdocs/466/weknow/3/3party/pyfsm.py", line 444, in enter2
    return self.func(task, obj)
  File "/data1/www/htdocs/466/weknow/3/web/mana4api.py", line 357, in info_mail
    print WxTextResponse(CFG.TXT_REALY_EM, wxreq).as_xml()
UnicodeEncodeError: 'ascii' codec can't encode character u'\u4eb2' in position 236: ordinal not in range(128) yq30 
'''



@state('weknow')
@transition('end', 'end')
def niuniu(self, wxreq):
    print 'setup->niuniu->end'
    crt_usr = wxreq.crt_usr
    crt_usr['fsm'] = "setup"
    __update_usr(crt_usr)
    _today = datetime.now()
    return WxTextResponse(CFG.TXT_NN% (_today-CFG.NIUNIU).days, wxreq).as_xml()

@state('weknow')
@transition('end', 'end')
def events(self, wxreq):
    print 'setup->events->end'
    crt_usr = wxreq.crt_usr
    print "crt_usr['fsm']~~", crt_usr['fsm']
    crt_usr['fsm'] = "setup"
    __update_usr(crt_usr)
    return WxTextResponse(CFG.TXT_EVENT_NULL, wxreq).as_xml()


@state('weknow')
@transition('end', 'end')
def reg_event(self, crt_usr):
    print 'setup->reg_event->end'
    crt_usr = wxreq.crt_usr
    crt_usr['fsm'] = "setup"
    __update_usr(crt_usr)




@state('weknow')
@transition('end', 'end')
def reg_cancel(self, crt_usr):
    print 'setup->reg_cancel->end'
    crt_usr = wxreq.crt_usr
    crt_usr['fsm'] = "setup"
    __update_usr(crt_usr)



@state('weknow')
@transition('end', 'end')
def reg_info(self, crt_usr):
    print 'setup->info_reg->end'
    crt_usr = wxreq.crt_usr
    crt_usr['fsm'] = "setup"
    __update_usr(crt_usr)



@state('weknow')
@transition('end', 'end')
def helpme(self, wxreq):
    print 'setup->helpme->end'
    crt_usr = wxreq.crt_usr
    crt_usr['fsm'] = "setup"
    __update_usr(crt_usr)
    return WxTextResponse(CFG.TXT_HELP, wxreq).as_xml()
    
    return __echo_txt(crt_usr['fromUser']
        , crt_usr['toUser']
        , CFG.TXT_HELP
        )



@state('weknow')
@transition('end', 'end')
def status(self, wxreq):
    print 'setup->status->end'
    crt_usr = wxreq.crt_usr
    crt_usr['fsm'] = "setup"
    __update_usr(crt_usr)
    _msg = ""   #u"是也乎 "
    #_msg += "\nget_info()-> "+str(KV.get_info())
    _INX_KEYS = [CFG.K4D[k] for k in CFG.K4D.keys()]
    for k in _INX_KEYS:
        # 索引键处理
        if 'SYS_TOT' == k:
            _msg += u"SYS_TOT::"+str(KV.get(k))
        else :
            # 统一合并
            _msg += u"; %s :: %snodes"%(k, len(KV.get(k)))

    #print "pp2u-->", KV.get(KV.get('oFNShjiOhclfJ-CtOO81p2sPrBfs'))
    #_msg += "\n\t usr:: %s"% crt_usr
    #_msg += "\n\t FromUserName:: %s"% wxreq.FromUserName
    #_msg += "\n\t ToUserName:: %s"% wxreq.ToUserName
    #return WxTextResponse(_msg, wxreq).as_xml()
    #    access_token = _wx_token_get()
    wx_uri = 'wx/msg'
    host = CFG.CLI_URI[wx_uri][0]
    url = CFG.CLI_URI[wx_uri][1]    #"%s=%s"% (CFG.CLI_URI[wx_uri][1], access_token)

    openid = XCFG.WX_ZQ
    content = _msg  #u'#细思恐极....'
    cc_msg = CFG.SRV_TXT_JSON% locals()
    print cc_msg
    data = _https_post(host
        , url
        , cc_msg  #bytearray(_msg.encode('utf-8'))
        , token = access_token
        )
    print data


    
    return WxTextResponse(_msg, wxreq).as_xml()
    
    # 确认订阅号无法指向发送
    wxreq.FromUserName = XCFG.WX_ZQ
    print "rewrite as onoK2t_msg>>> %s"% wxreq.FromUserName
    print WxTextResponse(_msg, wxreq).as_xml()
    
    return __echo_txt(crt_usr['fromUser']
        , crt_usr['toUser']
        , KV.get_info()
        )





@state('weknow')
@transition('end', 'end')
def version(self, wxreq):
    print 'setup->version->end'
    crt_usr = wxreq.crt_usr
    crt_usr['fsm'] = "setup"
    __update_usr(crt_usr)
    return WxTextResponse(CFG.TXT_VER, wxreq).as_xml()

    return __echo_txt(crt_usr['fromUser']
        , crt_usr['toUser']
        , CFG.TXT_VER
        )

def _wx_token_get():
    data = _https_get(CFG.CLI_URI['wx/t'][0]
        , CFG.CLI_URI['wx/t'][1]
        , appid = XCFG.WX_APPID
        , secret = XCFG.WX_SECRET
        )
    #print data
    js = json.loads(data)
    print "access_token: ", js['access_token']
    return js['access_token']
def _https_post(uri, tpl, values, **args):
    c = httplib.HTTPSConnection(uri, 443)
    #print args
    print uri
    print tpl % args
    
    c.request("POST"
        , tpl % args
        , bytearray(values.encode('utf-8'))
        #values#.encode('utf-16be') #.decode("utf-8")
        , {'Content-Type': 'text/plain; charset=utf-8'}
        )
    #return None
    response = c.getresponse()
    print response.status, response.reason
    data = response.read()
    return data

'''
conn = httplib.HTTPSConnection(host='www.site.com', port=443, cert_file=_certfile)
   params  = urllib.urlencode({'cmd': 'token', 'device_id_st': 'AAAA-BBBB-CCCC',
                                'token_id_st':'DDDD-EEEE_FFFF', 'product_id':'Unit Test',
                                'product_ver':"1.6.3"})
    conn.request("POST", "servlet/datadownload", params)
    content = conn.getresponse().read()
    #print response.status, response.reason
    conn.close()
'''
def _https_get(uri, tpl, **args):
    c = httplib.HTTPSConnection(uri)
    #print args
    c.request("GET", tpl % args)
    response = c.getresponse()
    print response.status, response.reason
    data = response.read()
    return data
def __echo_txt(fromUsr, toUsr, text):
    '''zip xml exp.
    '''
    tStamp = int(time.time())    #TSTAMP()
    fromUser = fromUsr
    toUser = toUsr
    content = text
    print CFG.TPL_TEXT% locals()
    return CFG.TPL_TEXT% locals()

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
    return '''


\          SORRY            /
 \                         /
  \    This page does     /
   ]   not exist yet.    [    ,'|
   ]                     [   /  |
   ]___               ___[ ,'   |
   ]  ]\             /[  [ |:   |
   ]  ] \           / [  [ |:   |
   ]  ]  ]         [  [  [ |:   |
   ]  ]  ]__     __[  [  [ |:   |
   ]  ]  ] ]\ _ /[ [  [  [ |:   |
   ]  ]  ] ] (#) [ [  [  [ :===='
   ]  ]  ]_].nHn.[_[  [  [
   ]  ]  ]  HHHHH. [  [  [
   ]  ] /   `HH("N  \ [  [
   ]__]/     HHH  "  \[__[
   ]         NNN         [
   ]         N/"         [
   ]         N H         [
  /          N            \

/                           \

roaring zoomquiet+404@gmail.com
'''
#    return template('404.html')

@APP.route('/favicon.ico')
def favicon():
    abort(204)
    
@APP.route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static')
    






