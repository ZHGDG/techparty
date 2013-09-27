# -*- coding: utf-8 -*-
import sys
from os import uname

import os.path
app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, "3party/"))
sys.path.insert(0, os.path.join(app_root, "module/"))
sys.path.insert(0, os.path.join(app_root, "web/"))
#   指定的模板路径
JINJA2TPL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__)
        , "templates/")
    )

#import hashlib

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 全局值
class Borg():
    '''base http://blog.youxu.info/2010/04/29/borg
        - 单例式配置收集类
    '''
    __collective_mind = {}
    def __init__(self):
        self.__dict__ = self.__collective_mind
    
    VERSION = "weknow v13.09.26-24"
    #管理员邮箱列表
    ADMIN_EMAIL_LIST = ['zoomquiet+gdg@gmail.com']

    if 'SERVER_SOFTWARE' in os.environ:
        # SAE
        AS_SAE = True
    else:
        # Local
        AS_SAE = False
    from sae.storage import Bucket
    BK = Bucket('bkup')
    import sae.kvdb
    KV = sae.kvdb.KVClient()
    #   系统索引键-名字典
    K4D = {'incr':"SYS_TOT"         # int
        ,'member':"SYS_usrs_ALL"    # [] 所有用户  (包含已经 del 的)
        ,'dama':"SYS_dama_ALL"      # [] 所有 组委  (包含已经 del 的)
        ,'events':"SYS_eves_ALL"    # [] 所有活动索引 (包含已经 del 的)
        ,'papers':"SYS_pubs_ALL"    # [] 所有文章索引 (包含已经 del 的)
    }
    #KEY4_incr = K4D['incr']
    for k in K4D:
        if None == KV.get(K4D[k]):
            if 'incr' == k:
                KV.add(K4D[k], 0)
            else:
                KV.add(K4D[k], [])
        else:
            print K4D[k], KV.get(K4D[k])

    objUSR={"his_id":""   # 更新戮
        , "lasttm": ''  # time.time()
        , "del":0
        , "acl":1       # ban:0 usr:1 staff:10 api:42 admin:100
        , "desc":""     # 解释

        , "fsm":""      # 有限状态机 当前状态
        , "pp":''       # Passport 
        , "nm":""       # NickName "Zoom.Quiet"
        , 'em':''       #'zhouqi@ijinshan.com',
        }
        



    # 大妈们的联系方式
    K4DM = {"his_id":""   # 更新戮
        , "del":0
        , "nm":""       # NickName "Zoom.Quiet"
        , "desc":""     # 解释
        , "pp":''       # Passport "kswl662773786"
        , 'em':''       #'zhouqi@ijinshan.com',
        , 'mo':''       #Mobile
        }



    ESSAY_TAG = {'ot':u" ~ 其它 (其余文章,AT也很好;)"
        , 'gb':u" ~ G术图书 (推荐好书,书无中外)"
        , 'dd':u" ~ D码点评 (麻辣评点,善意满盈)"
        , 'gt':u" ~ G说公论 (时评杂文,新旧不拘)"
        , 'dm':u" ~ 珠的自白 (大妈自述,每周一篇)"
        , 'hd':u" ~ 海选文章 (得要相信,大妈法眼)"
        , 're':u" ~ 活动报道 (快乐大趴,给力小会)"
        }
        
    # 文章索引
    K4WD = {"his_id":""   # 更新戮
        , "del":0
        , "type":"txt"  # 信息类型 txt|uri|pic
        , "tag":"ot"
        , 'title':''
        , "desc":""     # 解释
        , "picurl":''
        , "url":""
        }
        



    #   历史操作 键-名字典
    K4H = {'C':"Create"
        ,'D':"Delete"
        ,'U':"Update"
        }
    #'uuid':""     # 历史版本扩展ID
    objHis = {'hisobj':""
        ,'actype':"..."     # 操作类型C|D|U~ Create|Delet|Update = 创建|删除|更新
        ,'dump':''        # 数据集
        }



    CMD_ALIAS=('h', 'H', 'help', '?'
        , 'v', 'V', 'version', 'log'
        , 'i', 'I', 'me', 'ei'
        , 'e', 'E'
        , 're', 'rc', 'ri'
        , 's', 'S'
        , 'st', 'stat'
        )

    DM_ALIAS = {"LXC": ['Bonnie', 'liuxinchen', 'lxc', 'LXC', u'刘星辰']
        , "ZQ": ['Zoom.Quiet','zq', 'zoomq', 'ZQ', u'ZQ大妈', u'大妈', u'周琦']
        , "LG": ['Spawnris','GJT', 'gaojunten', 'LG', 'lg', 'spawnris', u'老高', u'高骏腾']
        , "LQX": ['LQX', 'lqx', 'langqixu', u'小郎', u'郎启旭']
        }

    TXT_EVENT_NULL = u'''亲! 目测近期没有活动规划!

    更多细节,请惯性地输入 h 继续吧 :)
    '''
    TXT_VER = u'''珠海GDG 公众号应答系统当前版本:
    %s
    Changelog:
    - 130926 改造并使用 Jeff 的SDK,配合运营CLI 工具
    - 130923 完成初始可用, 并发布 42分钟乱入 wechat 手册!-)
    - 130918 启动开发

    更多细节,请惯性地输入 h 继续吧 :)'''% VERSION

    TXT_THANX = u'''亲! 感谢反馈信息, 大妈们得空就回复 ;-)
    '''
    TXT_HELP = u'''GDG珠海 公众号目前支持以下命令:
    h   ~ 使用帮助
    V   ~ 系统版本
    s   ~ 查阅文章
    i   ~ 查阅成员资料
    ei  ~ 修订成员资料

    e   ~ 活动查询
    '''
    '''
    re  ~ 活动报名
    rc  ~ 放弃报名
    ri  ~ 确认报名

    dm [组委的名字] 可了解TA更多
    '''
    TXT_WELCOME = u'''GDG珠海 公众号的应答范畴:
    - GDG活动报名、签到、直播
    - GDG大妈联系查询
    - GDG发表文章查阅
    功能正在完善中，欢迎反馈。
    更多细节,请惯性地输入 h 继续吧 :)
    '''


    TXT_CRT_DM = u'''亲! 知道嘛?
    %s : 
      %s

    更多细节,请惯性地输入 h 继续吧 :)
    '''

    TXT_CRT_ME = u'''亲! 你当前注册的成员信息如下:
    妮称: %s
    邮箱: %s

    更多细节,请惯性地输入 h 继续吧 :)
    '''

    TXT_NO_INIT = u'''亲! 目测首次使用 俺们的应答服务?
    请输入 ei 开始增补妮称以及邮箱卟!-) 

    更多细节,请输入 h 继续吧 :)
    '''

    TXT_PLS_ALIAS = u'''请输入亲想用的妮称:
    (成员信息增补流程 1/2)

    更多细节,请惯性地输入 h 继续吧 :)
    '''

    TXT_PLS_EN4NM = u'''亲! 为输入方便,使用E文作为妮称吧!
    (成员信息增补流程 1/2)

    更多细节,请惯性地输入 h 继续吧 :)
    '''

    TXT_PLS_EM = u'''请输入亲常用邮箱:
    (成员信息增补流程 2/2)

    更多细节,请惯性地输入 h 继续吧 :)
    '''
    TXT_REALY_EM = u'''亲! 得给邮箱哪!
    (成员信息增补流程 2/2)

    也可以输入 * 退出 ;-)

    更多细节,请惯性地输入 h 继续吧 :)
    '''

    CN_TXT_REALY_EM = u'''亲! 要请输入邮箱格式吼!
    (成员信息增补流程 2/2)

    也可以输入 * 退出成员信息增补流程;-)

    更多细节,请惯性地输入 h 继续吧 :)
    '''

    TXT_DONE_EI = u'''谢谢,亲! 成员信息增补完成:
    妮称: %s
    邮箱: %s

    (成员信息增补流程 完成!-)

    更多细节,请惯性地输入 h 继续吧 :)
    '''

    TXT_NEW_USR = u'''亲!信息还曾注册, 请输入邮箱先;
    形如:
    em:foo.bar@gmail.com

    更多细节,请惯性地输入 h 继续吧 :)
    '''


    PAPER_TAGS = ESSAY_TAG.keys()
    TXT_TAG_DEFINE = "\n".join([u"%s %s"%(k, ESSAY_TAG[k]) for k in ESSAY_TAG.keys()])

    TXT_PLS_TAG = u'''亲! 请输入文章类别编码(类似 dm 的2字母):
    然后,俺才能给出该类别的文章索引...
    %s
    也可以输入 * 退出文章查阅流程;-)

    更多细节,请惯性地输入 h 继续吧 :)
    '''% TXT_TAG_DEFINE

    TXT_OUT_TAG = u'''亲! 目测输错了类别编码,再试?
    (类似 dm 的2字母):

    %s

    也可以输入 * 退出文章查阅流程;-)

    更多细节,请惯性地输入 h 继续吧 :)
    '''% TXT_TAG_DEFINE

    TXT_PLS_INT = u'''亲! 请输入类型文章的编号,仅数字就好:

    也可以输入 * 退出文章查阅流程;-)

    更多细节,请惯性地输入 h 继续吧 :)
    '''

    TXT_PUB_LIST = u'''%s ::
    %s

    也可以输入 * 退出文章查阅流程;-)

    更多细节,请惯性地输入 h 继续吧 :)
    '''

    TXT_PUB_WAIT = u'''对不起亲!
    过往文章的信息,大妈们还没来的及增补进来,
    放轻松,等等先... (~.~)

    也可以输入 * 退出文章查阅流程;-)

    更多细节,请惯性地输入 h 继续吧 :)
    '''



    '''
    2013/09/23 12:13:56] -  <xml>
         <ToUserName><![CDATA[oFNShjiOhclfJ-CtOO81p2sPrBfs]]></ToUserName>
         <FromUserName><![CDATA[gh_5e32c47b5b23]]></FromUserName>
         <CreateTime>13092312135634476</CreateTime>
         <MsgType><![CDATA[text]]></MsgType>
         <Content><![CDATA[本公众号的自动回答范畴：
        - GDG活动报名、签到、直播
        - GDG大妈联系查询
        - GDG发表文章查阅
        功能正在完善中，欢迎反馈。
        更多请惯性地输入 h 继续吧 :)
        ]]></Content>
         </xml> yq34 
    '''
    TPL_TEXT='''<xml>
    <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
    <FromUserName><![CDATA[%(fromUser)s]]></FromUserName>
    <CreateTime>%(tStamp)s</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%(content)s]]></Content>
    </xml>'''

    TPL_URIS='''<xml>
    <ToUserName><![CDATA[%(toUser)s]]></ToUserName>
    <FromUserName><![CDATA[%(fromUser)s]]></FromUserName>
    <CreateTime>%(tStamp)s</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <ArticleCount>%(item_count)d</ArticleCount>
    <Articles>
    %(items)s
    </Articles>
    </xml> 
    '''

    TPL_ITEM='''<item>
    <Title><![CDATA[%(title)s]]></Title> 
    <Description><![CDATA[%(description)s]]></Description>
    <PicUrl><![CDATA[%(picurl)s]]></PicUrl>
    <Url><![CDATA[%(url)s]]></Url>
    </item>
    '''



    APIPRE = "/cli" #% _API_ROOT
    STLIMI = 4.2    # 请求安全时限(秒)
    SECURE_ARGS = ('appkey', 'ts', 'sign')
    CLI_MATTERS = {     # 命令行响应方式速查字典
        "sum/usr":"GET"             # 统计用户现状
        , "info/usr":   "GET"       # 查阅用户信息
        , "find/usr":   "GET"       # 搜索用户
        , "list/usr":   "GET"       # 列出指定级别用户
        , "del/usr":    "DELETE"    # 软删除所有用户 (包含tag 信息)
        , "reliv/usr":  "PUT"       # 恢复指定用户
        , "acl/usr":    "PUT"       # 设置用户权限

        , "fix/usr":    "PUT"       # 修订用户信息
        , "fix/dm":     "PUT"       # 修订 大妈 信息
        , "fix/pub":    "PUT"       # 增补 文章 信息

        , "echo":       "GET"       # 模拟wechat 问答
        
        , "st/kv":      "GET"       # 查阅 KVDB 信息

        , "sum/db":     "GET"       # 统计 整体 信息现状
        , "sum/dm":     "GET"       # 统计 大妈 信息现状
        , "sum/m":      "GET"       # 统计 成员 信息现状
        , "sum/e":      "GET"       # 统计 活动 信息现状
        , "sum/p":      "GET"       # 统计 文章 信息现状

        , "bkup/db":    "PUT"       # 备份整个 KVDB
        , "bkup/dm":    "PUT"       # 备份所有 大妈
        , "bkup/m":     "PUT"       # 备份所有 成员
        , "bkup/e":     "PUT"       # 备份所有 活动
        , "bkup/p":     "PUT"       # 备份所有 文章

        , "revert/db": "POST"       # 恢复整个 KVDB
        
        , "sum/his":   "GET"        # 节点(任意)修订次数
        , "his/last":  "GET"        # 最后一次节点(任意)修订
        }


    LEVEL4USR = {"mana":0
        , "up":1
        , "api":2
        }


    
CFG = Borg()

