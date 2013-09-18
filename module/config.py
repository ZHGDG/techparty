# -*- coding: utf-8 -*-
VERSION = "mana4lbcrx v12.10.15"

import sys
import os.path
#from os.path import abspath, dirname, join
#import logging
app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, "3party/"))
sys.path.insert(0, os.path.join(app_root, "module/"))
sys.path.insert(0, os.path.join(app_root, "web/"))

'''
sys.path.insert(0, abspath(dirname(__file__)))
sys.path.insert(0, abspath(join(dirname(__file__), "3party/")))
sys.path.insert(0, abspath(join(dirname(__file__), "module/")))
sys.path.insert(0, abspath(join(dirname(__file__), "web/")))
CUSTOM_TPL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__)
        , "views/")
    )
'''

#   指定的模板路径
JINJA2TPL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__)
        , "templates/")
    )
#   静态文件
#STATIC_FILE_PATH = abspath(join(dirname(__file__), "static/"))
#   网站根域名
#ROOT_DOMAIN = 'test.com'
#   session相关
#SECRET_KEY = 'secret_key_for_test'
#SESSION_MAX_AGE = 7200

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 全局值
class Borg():
    '''base http://blog.youxu.info/2010/04/29/borg
        - 单例式配置收集类
    '''
    __collective_mind = {}
    def __init__(self):
        self.__dict__ = self.__collective_mind
        
    #管理员邮箱列表
    ADMIN_EMAIL_LIST = ['zoomquiet+lb@gmail.com']
    APPKEY = "5t4r3e2w1q"
    SECRET = "99fc9fdbc6761f7d898ad25762407373"
    APITYPE = "api/cli"
    PREUID = "usr:"
    MSG4PW = {'add':"created new usr"
        , 'del':"deleted new usr"
        , 'mod':"modified usr info."
        , 'chk':"listing all usr"
        }
    MSG4CRX = {'mod':"fixed .crx info."
        , 'chk':"listing all .crx"
        , 'info':"all info. of one .crx"
        , 'err':"something is ERROR!"
        }

    LEVEL4USR = {"mana":0
        , "up":1
        , "api":2
        }

    #   Storage domain name 约定
    D2X = 'crx4lb'
    D2P = 'pic2lb'
    D4P = 'page4crx'
    #KVDB 对象模板
    #   系统索引键-名字典
    K4D = {'incr':"TOT"
        ,'his':"SYS:his"        # 指向被复制的过往各种对象
        ,'crx':"SYS:crxs"       # 所有己发布的CRX
        ,'try':"SYS:trys"       # 所有待审核的CRX 
        ,'bak':"SYS:bak"        # 所有被退回的CRX 
        ,'out':"SYS:outs"       # 所有己下架的CRX 
        ,'arch':"SYS:arch"      # 所有己归档的CRX 
        ,'api4cx':"SYS:ctcrx"   # API可请求下载统计的 uuid 
        ,'grp':"SYS:grps"
        ,'tag':"SYS:tags"
        ,'pic':"SYS:pics"
        ,'usr':"SYS:users"      # 所有用户(包含已经 del 的)
        ,'stuff':"SYS:stuff"
    }
    #   历史操作 键-名字典
    K4H = {'C':"Create"
        ,'D':"Delete"
        ,'U':"Update"
    }
    objHis = {'id':None     # 历史版本扩展ID
        ,'hisobj':None
        ,'hisact':"..."     # 操作类型C|D|U~ Create|Delet|Update = 创建|删除|更新
        ,'tstamp':''        # yymmddHHMMSS+5位微秒
    }
    #   所有扩展 uuid->x:id 值对 单独收集?
    objCRX = {'uuid':None    # 扩展ID 为唯一
        ,'id':None      # 上次 历史版本ID
        ,'hisid':[]     # 所有操作历史
        ,'sid':None     # 存储ID
        ,'tagid':[]     #   可以属于多种标签
        ,'grpid':None   # 只能有一个作者拥有!
        ,'pic':[]
        ,'icon':None    # only one icon?!
        ,'name':""
        ,'desc':"是也乎"
        ,'version':'0.1'
        ,'dlrank':1024  #   下载总数量
        ,'detail':"..."
        ,'reply':"..."  # 审发回执(不显示在外部页面)
        ,'ispub':0      # 是否审发
        ,'isdel':0      # 是否删除
        ,'isreco':0     # 是否推荐
        ,'isbd':0       # 是否商务
        ,'gsdl':9442
        ,'gsusr':9442
        ,'gsrank':3     # google web store abt.
    }
    #   'sid':None         # 存储ID
    objPIC = {'size':"M"         # XXXL|XXL|XL|L|M
        ,'icon':0           # 是否icon SIZE
        ,'reco':0           # 是否推荐
        ,'isdel':0          # 是否删除
        ,'note':"是也乎"
        ,'order':0
    }
    #'id':None
    objGRP = {'id':None
        ,'hisid':[]     # 所有操作历史
        ,'crxs':[]      # 已发布的
        ,'trys':[]      # 待发布的
        ,'outs':[]      # 被下架的
        ,'baks':[]      # 被回退的
        ,'pic':[]
        ,'name':""
        ,'weibo':""
        ,'mail':""
        ,'desc':"..."
        ,'lead':""
        ,'isdel':0      # 是否删除
        ,'icon':0       # 是否icon SIZE
        ,'reco':0       # 是否推荐
        ,'order':0
    }

    objTAG = {'id':None
        ,'hisid':[]     # 所有操作历史
        ,'crxs':[]
        ,'name':""
        ,'desc':"..."
        ,'isdel':0      # 是否删除
        ,'order':0
    }

    objUSR = {'id':None # "usr:"+unicode(sha256(用户名).hexdigest())
        ,'crxs':[]
        ,'name':""
        ,'passwd':""    # unicode(sha256(口令).hexdigest())
        ,'isdel':0      # 是否删除
        ,'level':9      # 0|1 管理|团队
    }




CFG = Borg()

