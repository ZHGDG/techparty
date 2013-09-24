# -*- coding: utf-8 -*-
import os
import sys
import traceback
from copy import deepcopy
from time import time, gmtime, strftime, localtime
import hashlib

from config import CFG
_k4incr = CFG.TOT
#import sae.storage
#import sae.kvdb
KV = CFG.KV #sae.kvdb.KVClient()

# KVDB or Memcache global sys. event count KEY






def KV4CRX(uuid, action):
    '''.crx 状态 KV 列表统一切换器:
        - 对扩展的所有状态对应的组合映射到一批列表中
      act\KV|crx try out bak arch api4cx 
        新增  0   1   0   0    0   0   (请求上架)    
        回退  0   0   0   1    0   0    
        上架  1   0   0   0    0   1   
        下架  0   0   1   0    0   0   
        归档  0   0   0   0    1   0   
        回收  0   1   0   0    0   0   
    '''
    #print uuid
    #KV = sae.kvdb.KVClient()
    k4crx, crcrxs = INIobjSYS('crx')
    k4try, crtrys = INIobjSYS('try')
    k4out, crouts = INIobjSYS('out')
    k4bak, crbaks = INIobjSYS('bak')
    k4arc, crarch = INIobjSYS('arch')
    k4ctc, ctcapi = INIobjSYS('api4cx')
    try:
        if "ini" == action:
            POP4KV(uuid, k4crx, crcrxs)
            INS2KV(uuid, k4try, crtrys)
            POP4KV(uuid, k4out, crouts)
            POP4KV(uuid, k4bak, crbaks)
            POP4KV(uuid, k4arc, crarch)
            POP4KV(uuid, k4ctc, ctcapi)
        elif "bak" == action:
            POP4KV(uuid, k4crx, crcrxs)
            POP4KV(uuid, k4try, crtrys)
            POP4KV(uuid, k4out, crouts)
            INS2KV(uuid, k4bak, crbaks)
            POP4KV(uuid, k4arc, crarch)
            POP4KV(uuid, k4ctc, ctcapi)
        elif "recover" == action:
            POP4KV(uuid, k4crx, crcrxs)
            INS2KV(uuid, k4try, crtrys)
            POP4KV(uuid, k4out, crouts)
            POP4KV(uuid, k4bak, crbaks)
            POP4KV(uuid, k4arc, crarch)
            POP4KV(uuid, k4ctc, ctcapi)
        elif "pub" == action:
            INS2KV(uuid, k4crx, crcrxs)
            POP4KV(uuid, k4try, crtrys)
            POP4KV(uuid, k4out, crouts)
            POP4KV(uuid, k4bak, crbaks)
            POP4KV(uuid, k4arc, crarch)
            INS2KV(uuid, k4ctc, ctcapi)
        elif "out" == action:
            POP4KV(uuid, k4crx, crcrxs)
            POP4KV(uuid, k4try, crtrys)
            INS2KV(uuid, k4out, crouts)
            POP4KV(uuid, k4bak, crbaks)
            POP4KV(uuid, k4arc, crarch)
            POP4KV(uuid, k4ctc, ctcapi)
        elif "arch" == action:
            POP4KV(uuid, k4crx, crcrxs)
            POP4KV(uuid, k4try, crtrys)
            POP4KV(uuid, k4out, crouts)
            POP4KV(uuid, k4bak, crbaks)
            INS2KV(uuid, k4arc, crarch)
            POP4KV(uuid, k4ctc, ctcapi)
    except:
        print ">>>KV4CRX(uuid)\n\t", traceback.print_exc()
        #sys.exit(1)
        return None
    print "\t crcrxs:",crcrxs
    print "\t crtrys:",crtrys
    print "\t crouts:",crouts
    print "\t crbaks:",crbaks
    print "\t crarch:",crarch
    print "\t ctcapi:",ctcapi
    
    return crcrxs, crtrys, crouts, crbaks, crarch, ctcapi



def KV4GRP(uuid):
    '''.crx 状态对应 团队拥有 .crx 状态切换器:
        - 对扩展的所有状态对应的组合映射到一批列表中
      act\KV|crxs trys outs baks
        新增  0    1    0    0
        回退  0    0    0    1
        上架  1    0    0    0
        下架  0    0    1    0
        归档  0    0    0    0
        回收  0    1    0    0
    '''
    #print uuid
    grpid = KV.get(uuid)['grpid']
    if grpid:
        crtgrp = KV.get(grpid)
        incrx, intry, inout, inbak, inarch = ST4CRX(uuid)
        if incrx:
            crtgrp['crxs'], crtgrp = INS2DICT4LIST(uuid, crtgrp, 'crxs')
            POP4LIST(uuid, crtgrp['trys'])
            POP4LIST(uuid, crtgrp['outs'])
            POP4LIST(uuid, crtgrp['baks'])
        elif intry:
            POP4LIST(uuid, crtgrp['crxs'])
            crtgrp['trys'], crtgrp = INS2DICT4LIST(uuid, crtgrp, 'trys')
            POP4LIST(uuid, crtgrp['outs'])
            POP4LIST(uuid, crtgrp['baks'])
        elif inbak:
            POP4LIST(uuid, crtgrp['crxs'])
            POP4LIST(uuid, crtgrp['trys'])
            POP4LIST(uuid, crtgrp['outs'])
            crtgrp['baks'], crtgrp = INS2DICT4LIST(uuid, crtgrp, 'baks')
        elif inout:
            POP4LIST(uuid, crtgrp['crxs'])
            POP4LIST(uuid, crtgrp['trys'])
            crtgrp['outs'], crtgrp = INS2DICT4LIST(uuid, crtgrp, 'outs')
            POP4LIST(uuid, crtgrp['baks'])
        elif inarch:
            POP4LIST(uuid, crtgrp['crxs'])
            POP4LIST(uuid, crtgrp['trys'])
            POP4LIST(uuid, crtgrp['outs'])
            POP4LIST(uuid, crtgrp['baks'])
        KV.set(grpid, crtgrp)

        #print "\t crtgrp['crxs']:", crtgrp['crxs']
        #print "\t crtgrp['trys']:", crtgrp['trys']
        #print "\t crtgrp['outs']:", crtgrp['outs']

        return crtgrp['crxs'], crtgrp['trys'], crtgrp['outs'], crtgrp['baks']
    else:
        # grpid 为 None 时
        return None, None, None, None

    


def ST4CRX(uuid):
    '''.crx 目前状态 统一检测器:
        - 从系统扩展状态索引系列列表中
        - 抽取出当前扩展的状态,返回为一组状态值
      act\KV|crx try out bak arch api4cx 
        待发  0   1   0   0    0   0       
        回退  0   0   0   1    0   0   
        上架  1   0   0   0    0   1   
        下架  0   0   1   0    0   0   
        归档  0   0   0   0    1   0   
        回收  0   1   0   0    0   0   
    '''
    #print uuid
    #KV = sae.kvdb.KVClient()
    k4crx, crcrxs = INIobjSYS('crx')
    k4try, crtrys = INIobjSYS('try')
    k4out, crouts = INIobjSYS('out')
    k4bak, crbaks = INIobjSYS('bak')
    k4arc, crarch = INIobjSYS('arch')
    incrx = (uuid in crcrxs)
    intry = (uuid in crtrys)
    inout = (uuid in crouts)
    inbak = (uuid in crbaks)
    inarch = (uuid in crarch)
    #print "\t in SYS:crx? %s"% incrx
    #print "\t in SYS:try? %s"% intry
    #print "\t in SYS:out? %s"% inout
    #print "\t in SYS:arch? %s"% inarch
    
    return incrx, intry, inout, inbak, inarch



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



def PUT2SS(raw, fname, actype):
    '''put file into SAE.storage
        + return s:id
    '''
    if 'sae' == actype:
        sid = "%s.crx"% GENID('sae', fname)
        domain = CFG.D2X
    elif 'pic' == actype:
        sid = "%s.%s"% (GENID('pic'), fname.split(".")[-1])
        domain = CFG.D2P
    elif 'html' == actype:
        sid = "%s.html"% fname
        domain = CFG.D4P
        
    #print "\n PUT2SS:", sid
    #   初始化一个Storage客户端。
    ss = sae.storage.Client()
    ob = sae.storage.Object(raw)
    ss.put(domain, sid, ob)
    uri = ss.url(domain, sid)
    return sid, uri



def PUT_PIC4CRX(raw, fname, uuid):
    '''put pic into SAE.storage, REALY doing:
            + put into Storage
            + create new objPIC KV
            + append sid into SYS:pics
            + append sid into crx.pic
    #filename = picfile.filename
    if picfile is not None:
        raw = picfile.file.read() # This is dangerous for big files
        sid, uri = PUT2SS(raw, filename, 'pic')
        print uri
        picfile.file.close()
    '''
    sid, uri = PUT2SS(raw, fname, 'pic')
    #   + create new objPIC KV
    pic = deepcopy(CFG.objPIC)
    pic['note'] = sid
    KV.add(sid, pic)
    #   + append sid into SYS:pics
    #INS2KV(sid, k4pic, crpicss)
    k4pic, crpics = INIobjSYS('pic')
    crpics.append(sid)
    KV.set(k4pic, crpics)
    #print k4pic, crpics
    #   + append sid into crx.pic
    crcrx = KV.get(uuid)
    #   fixed 有可能的重复插入?
    crcrx['pic'].append(sid)
    crcrx['pic'] = list(set(crcrx['pic']))
    #KV.set(xid, crcrx)
    
    return sid, uri, crcrx



def INIobjSYS(key):
    '''try and init. all kinds of objSYS K/V
    '''    
    if key not in CFG.K4D.keys():
        return None
    else:
        #print CFG.K4D[key]
        if not KV.get(CFG.K4D[key]):
            KV.add(CFG.K4D[key],[])
        return CFG.K4D[key], KV.get(CFG.K4D[key])




def IDX4LIST(idx, KV):
    '''BASE idx list collection all Obj. into List
    '''
    #print "\tIDX4LIST(idx, KV):", idx
    #print "\t len(idx):", len(idx)
    if 0 == len(idx):
        return None
        
    exp = []
    for i in idx:
        exp.append(KV.get(i))
    if 0 == len(exp):
        return None
    else:
        return exp



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






def INS2LIST(cnt, listobj):
    '''try safty insert SOMETHING to list
    '''
    #print "\t>>>", cnt, listobj
    listobj.append(cnt)
    return list(set(listobj)) # 防止意外重复



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
    GOBJMAP = {'his':'h:%(timestamp)s:HIS%(tot)d'
        ,'tag':'t:%(timestamp)s:TAG%(tot)d'
        ,'event':'e:%(timestamp)s:EVE%(tot)d'
        ,'usr':'u:%(name)s'
        }
    if obj in GOBJMAP.keys():
        return GOBJMAP[obj]% locals()
    else:
        return None



def INCR4KV():
    '''BASE KVDB make GLOBAL increaser
    '''
    #print CFG.KEY4_incr
    #print None == CFG.KV.get(CFG.KEY4_incr)
    if None == KV.get(CFG.KEY4_incr):
        #print "\t EMPTY?!"
        KV.add(CFG.KEY4_incr, 0)
    else:
        #print "\t incr. BASE HISTORIC"
        KV.set(CFG.KEY4_incr, KV.get(CFG.KEY4_incr)+1)
    return KV.get(CFG.KEY4_incr)





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
        #MANIFEST4CRX(open('../../elf.crx', "rb").read())
        #print GENID('sae',"sdfsdfsd")
        #print GENID('crx')
        #print INIobjSYS('cc')
        #print 'increase by KVDB: %s' % INCR4KV()
        #print 'increase by Memcache: %s' % INCR4MM()
    
