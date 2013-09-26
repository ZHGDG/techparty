# -*- coding: utf-8 -*-
import os
import sys
import traceback
from copy import deepcopy
from time import time, gmtime, strftime, localtime
import hashlib





from config import CFG
#from xsettings import XCFG
#_k4incr = CFG.TOT
KV = CFG.KV #sae.kvdb.KVClient()

def PUTHIS(crobjs, act):
    '''put any obj. into SYS:his
        + copy obj. as new h:id KV
        + return h:id
    '''
    his = deepcopy(CFG.objHis)
    hid = GENID('his')
    his['id'] = hid
    his['hisobj'] = deepcopy(crobjs)
    his['hisact'] = act
    his['tstamp'] = TSTAMP()
    #   appended into KVDB
    KV.add(his['id'],his)
    #   collected into SYS:his
    k4his, crthis = INIobjSYS("his")
    INS2KV(hid, k4his, crthis)
    #print "\tSYS:his:", KV.get(k4his)
    return hid



def INIobjSYS(key):
    '''try and init. all kinds of objSYS K/V
    '''    
    if key not in CFG.K4D.keys():
        return None
    else:
        #print CFG.K4D[key]
        if not KV.get(CFG.K4D[key]):
            KV.add(CFG.K4D[key],[])
        return (CFG.K4D[key], KV.get(CFG.K4D[key]))




def POP4KV(xid, k4obj, crobjs):
    try:
        #k4obj, crobjs = INIobjSYS(sysk)
        if xid in crobjs:
            crobjs.pop(crobjs.index(xid))
            KV.set(k4obj, crobjs)
        else:
            pass
    except:
        print ">>>POP2KV(xid, sysk)\n\t", traceback.print_exc()
        #sys.exit(1)
        return None
    return True



def INS2KV(xid, k4obj, crobjs):
    #k4obj, crobjs = INIobjSYS(sysk)
    try:
        if xid in crobjs:
            pass
        else:
            crobjs.append(xid)
            KV.set(k4obj, crobjs)
    except:
        print ">>>INS2KV(xid, sysk)\n\t", traceback.print_exc()
        #sys.exit(1)
        return None
    return True



def POP4LIST(cnt, listobj):
    '''try safty pop SOMETHING from list
    '''
    try:
        idxcnt = listobj.index(cnt)
    except:
        print ">>>POP4LIST(cnt, listobj)\n\t", traceback.print_exc()
        #sys.exit(1)
        return None
    listobj.pop(idxcnt)
    return True






def IDX4LIST(idx, KV):
    '''BASE idx list collection all Obj. into List
    '''
    if 0 == len(idx):
        return None
    exp = []
    for i in idx:
        exp.append(KV.get(i))
    if 0 == len(exp):
        return None
    else:
        return exp



def INS2LIST(cnt, listobj):
    '''try safty insert SOMETHING to list
    '''
    #print "\t>>>", cnt, listobj
    listobj.append(cnt)
    return list(set(listobj)) # 防止意外重复



def ADD4SYS(k4sys, cnt):
    '''try safty insert SOMETHING to SYS:** K/V
    only member|member|paper
    '''
    listobj = KV.get(CFG.K4D[k4sys])
    print "listobj:\t", listobj
    # 防止意外重复
    listobj.append(cnt)
    appended = list(set(listobj))
    #print "appended\n", appended
    KV.replace(k4sys,  appended)
    return (k4sys, appended)



def INS2DICT4LIST(cnt, dictobj, keyname):
    '''try safty insert SOMETHING to list
    '''
    #print "\t>>>", cnt, listobj
    if dictobj.has_key(keyname):
        listobj = dictobj[keyname]
        listobj.append(cnt)
        listobj  = list(set(listobj))
        #print "\t list(set(listobj))", listobj
    else:
        listobj = []
        listobj.append(cnt)
        dictobj[keyname] = listobj
        #print "\t dictobj[keyname]~", dictobj[keyname]
    return listobj, dictobj # 防止意外重复






def TSTAMP():
    '''通用时间戳生成器:
        yymmddHHMMSS+5位微秒
        e.g.
        12080110561431076
    '''
    date = strftime("%y%m%d%H%M%S", localtime())
    mms = "%.5f"% time()
    ms = mms[-5:]
    return "%s%s"% (date, ms)




def GENID(obj, name=""):
    '''通用ID生成器:
        yymmddHHMMSS+5位微秒+对象鍵3位+全局序号
        e.g.
        x:12080110561431076:CRX1111
    '''
    timestamp = TSTAMP()
    tot = INCR4KV()
    #sha1name = hashlib.sha1(name).hexdigest()
    GOBJMAP = {'his':'h_%(timestamp)s_HIS%(tot)d'
        ,'tag':'t_%(timestamp)s_TAG%(tot)d'
        ,'event':'e_%(timestamp)s_EVE%(tot)d'
        ,'paper':'p_%(timestamp)s_PUB%(tot)d'
        #,'dm':'m:%(timestamp)s:DM%(tot)d'
        }
    if obj in GOBJMAP.keys():
        return GOBJMAP[obj]% locals()
    else:
        return None



def USRID(name):
    return 'u_%s'% name



def DAMAID(name):
    return 'm_%s_DM'% name



def INCR4KV():
    '''BASE KVDB make GLOBAL increaser
    '''
    #print CFG.KEY4_incr
    #print None == CFG.KV.get(CFG.KEY4_incr)
    if None == KV.get(CFG.K4D['incr']):
        #print "\t EMPTY?!"
        KV.add(CFG.K4D['incr'], 0)
    else:
        #print "\t incr. BASE HISTORIC"
        KV.set(CFG.K4D['incr'], KV.get(CFG.K4D['incr'])+1)
    return KV.get(CFG.K4D['incr'])





def INCR4MM():
    '''BASE Memcache make GLOBAL increaser
    '''
    import pylibmc
    
    mc = pylibmc.Client()
    if not mc.get(_k4incr):
        mc.set(_k4incr, 1111)
    else:
        mc.incr(_k4incr)
    return mc.get(_k4incr)




if __name__ == '__main__':
    if 2 != len(sys.argv) :
        print '''Usage:
            utility.py test
        '''
    else:
        print "hand testing ..."

