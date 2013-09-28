# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""CLI for WeKnow.

Usage:
  CLI.py [--debug] <matter> [<sets>]
  CLI.py -h | --help
  CLI.py -D | --debug    向本地接口发送请求
  CLI.py -V | --version

Options:
  -h --help     Show this screen.
  -V --version  Show version.
  -D --debug    对本地系统测试时专用参数
  <matter>      事务URI
  <sets>        数据设定

e.g:
  一般形式::
  $ python lbTCLI.py 事务指令 [可能的值设定 set=** 形式]
  详细操作::
  echo set=i        模拟微信的消息交互

  info/usr/:UUID            查阅指定 用户 信息
  find/usr/<key word>       搜索用户 [对名称,描述 进行搜索]

  st/kv     查询 KVDB 整体现状
  sum/bk|db|dm|m|e|p
      综合 备份|整体|大妈|成员|活动|文章 信息现状
  fix/dm/:NM  nm=ZQ       修订/创建指定 大妈 的相关信息
  fix/m/:UUID nm=ZQ       修订指定 成员 的相关信息
  fix/e/:CODE pic=***     修订/创建指定 活动 的相关信息
  fix/p/:TAG/:UUID url=***     增补|指定 文章 信息
    TAG当前支持 ot|et|gt|dd|gb|dm|hd
    UUID 为 null 时,指创建文章信息

  !!! 小心:大规模数据I/O操作 !!!
  del/bk/:UUID          删除指定备份 dump
  bkup/db|dm|m|e|p
     备份 KVDB|大妈|成员|活动|文章 数据到Storage

  revert/db|dm|m|e|p    set=备份dump
     恢复 KVDB|大妈|成员|活动|文章 数据到Storage
益rz...
"""
import sys
import os
import base64
from subprocess import Popen
from time import time, gmtime, strftime, localtime

from docopt import docopt

from config import CFG
from xsettings import XCFG
from module.auth import _genQueryArgs, _genArgsStr
AS_LOCAL = "http://localhost:8080/api"

def _rest_main(method, uri, args, host=AS_LOCAL):
    '''接受事务指令+数据, 合理拼成 hhtp 命令行:
        - GET/DELETE 时将参数拼为统一间隔字串
        - PUT/POST 时提交唯一数据,同 GET 时的参数字串结构
        - 注意! 参数的次序必须固定: 
            - appkey->ts->[q]->sign
            - appkey=***&ts=***&sign=***
            - 整体作base64.urlsafe_b64encode()包裹
    '''
    if 'PUT' == method: 
        put_args = _genQueryArgs(uri, q=args, rest_method=method)
        if not put_args:
            print "参数错误,请先使用 -h 学习;-)"
            return None
        #print "put_args\n\t", put_args
        pur_vars = " ".join(["%s=%s"% (p[0], p[1]) for p in put_args])
        #print pur_vars
        uri = "%s%s/%s %s"% (host, CFG.APIPRE, uri, pur_vars)
        cmd = "http -f -b %s %s "% (method, uri)


    elif 'POST' == method:
        #print args
        put_args = _genQueryArgs(uri, q=args, rest_method=method)
        #print "put_args\n\t", put_args
        pur_vars = " ".join(["%s=%s"% (p[0], p[1]) for p in put_args])
        #print pur_vars
        uri = "%s%s/%s %s"% (host, CFG.APIPRE, uri, pur_vars)
        cmd = "http -f -b %s %s "% (method, uri)

    else:
        if "echo" == uri:
            toUser = XCFG.AS_SRV
            fromUser = XCFG.AS_USR
            tStamp = int(time())
            content = args.split("=")[-1].strip()
            xml = CFG.TPL_TEXT % locals()
            cmd = "curl -d '%s' %s/%s "% (xml, AS_LOCAL, uri)
            #print cmd

            #return None


        else:
            get_args = _genQueryArgs(uri, rest_method=method)
            #print "get_args\n\t", get_args
            get_str = "&".join(["%s=%s"% (g[0], g[1]) for g in get_args])
            #print get_str
            uri = "%s%s/%s/%s"% (host
                , CFG.APIPRE
                , uri
                , base64.urlsafe_b64encode(get_str)
                )
            cmd = "http -b %s %s "% (method, uri)




    #print cmd
    Popen(cmd, shell=True, close_fds=True)
    #print p.stderr

    
def smart_rest(matter, sets):
    '''确保所有操作元语为 两节,其它作为附加参数...
    '''
    if "echo" == matter:
        _rest_main(CFG.CLI_MATTERS[matter], matter, sets)
    else:
        cmd = matter
        mess = matter.split("/")
        if 2 < len(mess):
            matter = "/".join(mess[:-1])
        #print mess
        #print matter
        if matter in CFG.CLI_MATTERS.keys():  
            method = CFG.CLI_MATTERS[matter]      
            #print "smart_rest:", method
            if debug:
                _rest_main(method, cmd, sets)
            else:
                _rest_main(method, cmd, sets, host = XCFG.TO_SAE)
        else:
            print "参数错误,请使用 -h 参阅手册..."




if __name__ == '__main__':
    '''
    - 为了简化 后台控制的界面开发,快速实现远程控制
    - 通过 RESTful 接口,从本地使用工具脚本实施管理事务!
    '''
    arguments = docopt(__doc__, version='lbTCLI v13.09.03b')
    metter = arguments.get('<matter>')
    debug = arguments.get('--debug')
    sets = arguments.get('<sets>')
    #print arguments
    smart_rest(metter, sets)
    #_rest_main(method, uri, args)

