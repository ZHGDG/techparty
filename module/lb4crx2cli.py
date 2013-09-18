# -*- coding: utf-8 -*-
import sys
import time
import base64
import urllib2 as urilib
from hashlib import md5
from base64 import urlsafe_b64encode

from config import CFG
class Borg():
    '''base http://blog.youxu.info/2010/04/29/borg
        - 单例式配置收集类
    '''
    __collective_mind = {}
    def __init__(self):
        self.__dict__ = self.__collective_mind
    APPKEY = "5t4r3e2w1q"
    SECRET = "99fc9fdbc6761f7d898ad25762407373"
    APITYPE = "api/cli"
    PREUID = "usr:"







import pprint
pp = pprint.PrettyPrinter(indent=4)

# init all var
CFG = Borg()

def __genRESTargs(usract):
    args = "%s"% usract
    args += "/%s"% CFG.APPKEY       #"appkey=" + 
    args += "/%d"% time.time()      #"&timestamp=" + 
    sign_base_string = "%s/%s"% (CFG.APITYPE, args)
    args += "/%s"% __genRESTsign(sign_base_string)
    #md5(sign_base_string + CFG.SECRET).hexdigest() #"&sign=" + 
    return args
def __genRESTsign(args):
    sign_base_string = "%s/%s"% (CFG.APITYPE, args)
    return md5(sign_base_string + CFG.SECRET).hexdigest()
def call2sae(mod, act, uribase):
    todo = mod
    #uname, passwd = act.split(":")
    usract = act
    aimurl = "%s/%s/%s/%s"% (uribase
        , CFG.APITYPE
        , todo
        , __genRESTargs(usract)
        )
    print aimurl
    #print urilib.urlopen(aimurl).read()
    #return
    result = urilib.urlopen(aimurl).read()
    #print eval(result)
    pp.pprint(eval(result))
    

if __name__ == '__main__':
    if 4 != len(sys.argv) :
        print '''Usage:
    $ lb4crx2cli.py usr[add|del|mod|chk] 用户名:口令:级别 http://XX.XX.XX
    or
    $ lb4crx2cli.py crx[mod|chk|info] UUID:属性:值 http://XX.XX.XX
        '''
    else:
        mod = sys.argv[1]
        act = sys.argv[2]
        uribase = sys.argv[3]
        #print mod, act, uribase
        #print dir(CFG)
        call2sae(mod, act, uribase)



